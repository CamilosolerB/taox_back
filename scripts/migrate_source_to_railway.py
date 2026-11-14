"""Copy the existing PostgreSQL database to an empty Railway database.

The source is read from ``.env`` and the destination from ``.env.production``.
This script never deletes or modifies source rows. It creates the destination
schema with Alembic and copies every source table except ``alembic_version``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

from dotenv import dotenv_values
from psycopg2.extras import execute_values
from sqlalchemy import MetaData, create_engine, inspect, select, text
from sqlalchemy.engine import Engine, URL, make_url
from sqlalchemy.sql.schema import Table


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REVISION = "c33156a66ff2"
TARGET_REVISION = "9c4d2e7a1b6f"
BATCH_SIZE = 500


def _read_url(filename: str) -> URL:
    raw_url = dotenv_values(ROOT / filename).get("DB_URL")
    if not raw_url:
        raise ValueError(f"DB_URL is missing in {filename}.")
    url = make_url(raw_url.strip())
    if url.drivername == "postgres":
        url = url.set(drivername="postgresql")
    return url.update_query_dict({"connect_timeout": "10"})


def _identity(url: URL) -> tuple[str | None, int | None, str | None]:
    return (url.host, url.port or 5432, url.database)


def _revision(connection) -> str | None:
    tables = set(inspect(connection).get_table_names())
    if "alembic_version" not in tables:
        return None
    revisions = [
        str(row[0])
        for row in connection.execute(text("SELECT version_num FROM alembic_version"))
    ]
    if len(revisions) != 1:
        raise ValueError("Expected exactly one Alembic revision in the database.")
    return revisions[0]


def _row_count(connection, table_name: str) -> int:
    return int(connection.execute(text(f'SELECT count(*) FROM "{table_name}"')).scalar_one())


def _canonical(value: Any) -> Any:
    if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool):
        return format(Decimal(str(value)).normalize(), "f")
    if isinstance(value, (UUID,)):
        return str(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.hex()
    return value


def _digest_rows(connection, table: Table, columns: list[str], primary_key: list[str]) -> tuple[int, str]:
    selected = [table.c[name] for name in columns]
    query = select(*selected).order_by(*(table.c[name] for name in primary_key))
    digest = hashlib.sha256()
    count = 0
    result = connection.execution_options(stream_results=True).execute(query)
    while batch := result.fetchmany(BATCH_SIZE):
        for row in batch:
            values = [_canonical(row._mapping[name]) for name in columns]
            digest.update(
                json.dumps(values, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            )
            digest.update(b"\n")
            count += 1
    return count, digest.hexdigest()


def _load_metadata(connection) -> MetaData:
    metadata = MetaData()
    metadata.reflect(bind=connection)
    return metadata


def _inspect_source(engine: Engine) -> tuple[str, dict[str, int]]:
    with engine.connect() as connection:
        revision = _revision(connection)
        if revision != SOURCE_REVISION:
            raise ValueError(
                f"Source revision is {revision!r}; expected {SOURCE_REVISION!r}."
            )
        metadata = _load_metadata(connection)
        names = sorted(name for name in metadata.tables if name != "alembic_version")
        counts = {name: _row_count(connection, name) for name in names}
        return connection.execute(text("SELECT current_database()")).scalar_one(), counts


def _inspect_destination(engine: Engine) -> tuple[str, str | None, set[str], dict[str, int]]:
    with engine.connect() as connection:
        database = connection.execute(text("SELECT current_database()")).scalar_one()
        metadata = _load_metadata(connection)
        tables = set(metadata.tables)
        revision = _revision(connection)
        counts = {
            name: _row_count(connection, name)
            for name in sorted(tables)
        }
        return database, revision, tables, counts


def _upgrade_destination(destination_url: URL) -> None:
    previous_url = os.environ.get("DB_URL")
    os.environ["DB_URL"] = destination_url.render_as_string(hide_password=False)
    try:
        from alembic import command
        from alembic.config import Config

        config = Config(str(ROOT / "alembic.ini"))
        command.upgrade(config, "head")
    finally:
        if previous_url is None:
            os.environ.pop("DB_URL", None)
        else:
            os.environ["DB_URL"] = previous_url


def _copy_rows(source_engine: Engine, destination_engine: Engine) -> dict[str, int]:
    with source_engine.connect() as source_connection:
        source_metadata = _load_metadata(source_connection)
        with destination_engine.begin() as destination_connection:
            destination_metadata = _load_metadata(destination_connection)
            source_names = set(source_metadata.tables) - {"alembic_version"}
            destination_names = set(destination_metadata.tables) - {"alembic_version"}
            missing_tables = source_names - destination_names
            if missing_tables:
                raise ValueError(
                    "Destination schema is missing source tables: "
                    + ", ".join(sorted(missing_tables))
                )

            order = [
                table.name
                for table in destination_metadata.sorted_tables
                if table.name in source_names
            ]
            copied_counts: dict[str, int] = {}
            for name in order:
                source_table = source_metadata.tables[name]
                destination_table = destination_metadata.tables[name]
                source_columns = [column.name for column in source_table.columns]
                destination_columns = {column.name for column in destination_table.columns}
                missing_columns = set(source_columns) - destination_columns
                if missing_columns:
                    raise ValueError(
                        f"Destination table {name!r} is missing source columns: "
                        + ", ".join(sorted(missing_columns))
                    )

                primary_key = [
                    column.name for column in source_table.primary_key.columns
                ]
                if not primary_key:
                    raise ValueError(f"Source table {name!r} has no primary key.")

                expected_count, expected_digest = _digest_rows(
                    source_connection, source_table, source_columns, primary_key
                )
                query = select(source_table).order_by(
                    *(source_table.c[column] for column in primary_key)
                )
                result = source_connection.execution_options(stream_results=True).execute(query)
                copied = 0
                while batch := result.fetchmany(BATCH_SIZE):
                    rows = [
                        {
                            column: row._mapping[column]
                            for column in source_columns
                        }
                        for row in batch
                    ]
                    row_values = [tuple(row.get(column) for column in source_columns) for row in rows]
                    if row_values:
                        insert_columns = [destination_table.c[column].name for column in source_columns]
                        insert_sql = (
                            f"INSERT INTO \"{name}\" ({', '.join(f'\"{c}\"' for c in insert_columns)}) "
                            f"VALUES %s"
                        )
                        with destination_connection.connection.cursor() as cursor:
                            execute_values(cursor, insert_sql, row_values, page_size=min(len(row_values), 1000))
                    copied += len(rows)
                if copied != expected_count:
                    raise RuntimeError(f"Row count changed while copying table {name!r}.")

                actual_count, actual_digest = _digest_rows(
                    destination_connection,
                    destination_table,
                    source_columns,
                    primary_key,
                )
                if actual_count != expected_count or actual_digest != expected_digest:
                    raise RuntimeError(
                        f"Data verification failed for table {name!r}; "
                        "the destination transaction will be rolled back."
                    )
                copied_counts[name] = copied

            _reset_sequences(destination_connection, destination_metadata)
    return copied_counts


def _reset_sequences(connection, metadata: MetaData) -> None:
    for table in metadata.sorted_tables:
        for column in table.columns:
            if not column.primary_key or not column.autoincrement:
                continue
            sequence_name = connection.execute(
                text("SELECT pg_get_serial_sequence(:table_name, :column_name)"),
                {"table_name": table.name, "column_name": column.name},
            ).scalar_one_or_none()
            if not sequence_name:
                continue
            max_value = connection.execute(
                select(column).select_from(table).order_by(column.desc()).limit(1)
            ).scalar_one_or_none()
            if max_value is None:
                connection.execute(
                    text("SELECT setval(CAST(:sequence_name AS regclass), 1, false)"),
                    {"sequence_name": sequence_name},
                )
            else:
                connection.execute(
                    text("SELECT setval(CAST(:sequence_name AS regclass), :value, true)"),
                    {"sequence_name": sequence_name, "value": max_value},
                )


def _print_report(
    source_name: str,
    source_counts: dict[str, int],
    destination_name: str,
    destination_counts: dict[str, int],
) -> None:
    print(f"Source database: {source_name} (revision {SOURCE_REVISION})")
    print("Source rows: " + ", ".join(f"{name}={count}" for name, count in source_counts.items()))
    print(f"Destination database: {destination_name} (Railway config)")
    print("Destination tables/rows: " + (", ".join(
        f"{name}={count}" for name, count in destination_counts.items()
    ) or "none"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create the destination schema and copy data; otherwise only inspect.",
    )
    args = parser.parse_args()

    source_url = _read_url(".env")
    destination_url = _read_url(".env.production")
    if _identity(source_url) == _identity(destination_url):
        raise ValueError("Source and destination resolve to the same database.")

    source_engine = create_engine(source_url, pool_pre_ping=True)
    destination_engine = create_engine(destination_url, pool_pre_ping=True)
    try:
        source_name, source_counts = _inspect_source(source_engine)
        destination_name, destination_revision, destination_tables, destination_counts = (
            _inspect_destination(destination_engine)
        )
        _print_report(
            source_name, source_counts, destination_name, destination_counts
        )

        if destination_tables:
            if destination_revision != TARGET_REVISION:
                raise ValueError(
                    "Destination is not empty and is not at the expected schema "
                    f"revision {TARGET_REVISION}; refusing to migrate."
                )
            populated = [
                name for name, count in destination_counts.items()
                if name != "alembic_version" and count
            ]
            if populated:
                raise ValueError(
                    "Destination contains data; refusing to overwrite: "
                    + ", ".join(populated)
                )

        if not args.apply:
            print("Inspection only; no migrations or data writes were performed.")
            return

        if not destination_tables:
            _upgrade_destination(destination_url)

        destination_name, destination_revision, destination_tables, destination_counts = (
            _inspect_destination(destination_engine)
        )
        if destination_revision != TARGET_REVISION:
            raise ValueError(
                f"Destination schema revision is {destination_revision!r}; "
                f"expected {TARGET_REVISION!r}."
            )
        populated = [
            name for name, count in destination_counts.items()
            if name != "alembic_version" and count
        ]
        if populated:
            raise ValueError(
                "Destination contains data after schema creation; refusing to copy: "
                + ", ".join(populated)
            )

        copied_counts = _copy_rows(source_engine, destination_engine)
        _, final_revision, _, final_counts = _inspect_destination(destination_engine)
        if final_revision != TARGET_REVISION:
            raise RuntimeError("Destination migration revision changed unexpectedly.")
        for table_name, expected_count in source_counts.items():
            if final_counts.get(table_name) != expected_count:
                raise RuntimeError(
                    f"Final row count differs for table {table_name!r}."
                )

        print(f"Copy verified; destination revision is {final_revision}.")
        print("Copied rows: " + ", ".join(
            f"{name}={count}" for name, count in copied_counts.items()
        ))
    finally:
        source_engine.dispose()
        destination_engine.dispose()


if __name__ == "__main__":
    main()
