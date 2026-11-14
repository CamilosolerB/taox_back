"""Import the supported business data from ``ultima bd.xlsx``.

Run without ``--apply`` to validate and preview. Applying requires explicit
company details and a database connection configured through the app settings.
"""
from __future__ import annotations

import argparse
import re
import unicodedata
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from openpyxl import load_workbook


WAREHOUSE_NAMES = {
    "TABLA_0_LAB": "Laboratorio",
    "TABLA_1_INV": "Inventario general",
    "TABLA_4_BODEGA": "Bodega física",
}
UNSUPPORTED_SHEETS = (
    "TABLA_6_PRODUCTO TERMINADO",
    "TABLA_7_MANO DE OBRA",
    "TABLA_8_DEPRECIACION EQUIPOS ",
    "CALCULO_FCA",
    "FORMATO_ORDEN DE PRODUCCION",
    "TABLA_CIF",
)


def _normalize(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", text.strip().lower())


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return text


def _first(row: dict[str, Any], *names: str) -> str | None:
    for name in names:
        value = _text(row.get(_normalize(name)))
        if value is not None:
            return value
    return None


def _number(value: Any) -> float | None:
    text = _text(value)
    if text is None:
        return None
    try:
        number = Decimal(text.replace(",", "."))
    except InvalidOperation as error:
        raise ValueError(f"Invalid numeric value in workbook: {text}") from error
    if not number.is_finite() or number < 0:
        raise ValueError(f"Inventory/price must be a non-negative number: {text}")
    return float(number)


def _read_sheet(workbook, name: str) -> list[dict[str, Any]]:
    if name not in workbook.sheetnames:
        return []
    sheet = workbook[name]
    rows = sheet.iter_rows(values_only=True)
    headers = [_normalize(value) for value in next(rows, ())]
    result = []
    for values in rows:
        if not any(value is not None for value in values):
            continue
        result.append(dict(zip(headers, values)))
    return result


def build_plan(workbook_path: Path) -> dict[str, Any]:
    if not workbook_path.is_file():
        raise FileNotFoundError(f"Workbook not found: {workbook_path}")

    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    try:
        products: dict[str, dict[str, Any]] = {}
        product_name_variants = 0
        warehouse_quantities: dict[str, float] = {}
        inventory_rows_without_quantity = 0
        primary_provider_names: dict[str, str] = {}
        location_rows: list[dict[str, Any]] = []
        location_stock: dict[tuple[tuple[str, ...], str], float] = defaultdict(float)
        provider_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
        provider_product_rows: list[dict[str, Any]] = []
        client_rows: list[dict[str, Any]] = []

        def add_product(
            code: str | None,
            name: str | None,
            source: str | None,
            generic_name: str | None = None,
            unit_measure: str | None = None,
            fds: str | None = None,
        ) -> None:
            nonlocal product_name_variants
            if not code or not name:
                return
            product = products.get(code)
            if product is None:
                product = {
                    "id_product": code,
                    "name": name,
                    "generic_name": generic_name or "",
                    "unit_measure": unit_measure or "UNIDAD",
                    "fds": fds,
                    "warehouse_sources": set(),
                }
                products[code] = product
            elif _normalize(product["name"]) != _normalize(name):
                product_name_variants += 1
            if not product["generic_name"] and generic_name:
                product["generic_name"] = generic_name
            if product["unit_measure"] == "UNIDAD" and unit_measure:
                product["unit_measure"] = unit_measure
            if not product["fds"] and fds:
                product["fds"] = fds
            warehouse_name = WAREHOUSE_NAMES.get(source or "")
            if warehouse_name:
                product["warehouse_sources"].add(warehouse_name)

        for row in _read_sheet(workbook, "TABLA_0_LAB"):
            code = _first(row, "codigo")
            add_product(
                code,
                _first(row, "nombre del producto"),
                "TABLA_0_LAB",
                _first(row, "uso de la sustancia"),
                _first(row, "unid"),
                _first(row, "fds"),
            )
            quantity = _number(_first(row, "total inven"))
            if quantity is None:
                inventory_rows_without_quantity += 1
            elif code:
                warehouse_quantities[code] = quantity

        for row in _read_sheet(workbook, "TABLA_1_INV"):
            code = _first(row, "codigo")
            add_product(
                code,
                _first(row, "nombre del producto"),
                "TABLA_1_INV",
                _first(row, "nombre generico"),
                _first(row, "unidad de medida"),
            )
            primary = _first(row, "proveedor principal")
            if code and primary:
                primary_provider_names[code] = primary
            quantity = _number(_first(row, "total invent", "total inventario"))
            if quantity is None:
                inventory_rows_without_quantity += 1
            elif code:
                if code in warehouse_quantities:
                    warehouse_quantities[code] += quantity
                else:
                    warehouse_quantities[code] = quantity

        for row in _read_sheet(workbook, "TABLA_4_BODEGA"):
            code = _first(row, "codigo")
            add_product(
                code,
                _first(row, "descripcion"),
                "TABLA_4_BODEGA",
                unit_measure=_first(row, "unidad"),
            )
            dimensions = (
                _first(row, "ubicacion"),
                _first(row, "nivel"),
                _first(row, "posicion"),
                _first(row, "localizador"),
            )
            if code and all(dimensions):
                location_key = tuple(dimensions)
                location_rows.append(
                    {
                        "key": location_key,
                        "ubicacion": dimensions[0],
                        "nivel": dimensions[1],
                        "posicion": dimensions[2],
                        "localizador": dimensions[3],
                        "tipo_ubicacion": "bodega",
                        "codigo_producto": code,
                    }
                )
                quantity = _number(_first(row, "cantidad"))
                if quantity is not None:
                    location_stock[(location_key, code)] += quantity
                    if code not in warehouse_quantities:
                        warehouse_quantities[code] = quantity
                    else:
                        warehouse_quantities[code] += quantity
                else:
                    inventory_rows_without_quantity += 1

        for row in _read_sheet(workbook, "TABLA_3_ALMACEN"):
            add_product(
                _first(row, "codigo"),
                _first(row, "item"),
                None,
            )

        for row in _read_sheet(workbook, "TABLA_2_MASTER"):
            provider_code = _first(row, "cod proveedor")
            product_code = _first(row, "codigo mat")
            add_product(
                product_code,
                _first(row, "nombre del producto"),
                None,
                unit_measure=_first(row, "unidad medida"),
            )
            if provider_code:
                provider_rows[provider_code].append(row)
            provider_product_rows.append(
                {
                    "provider_code": provider_code,
                    "product_code": product_code,
                    "price": _number(_first(row, "precio")),
                    "provider_name": _first(row, "nombre proveedor"),
                }
            )

        valid_providers: dict[str, dict[str, str]] = {}
        providers_skipped = 0
        for code, rows in provider_rows.items():
            def first_value(*names: str) -> str | None:
                return next(
                    (value for row in rows if (value := _first(row, *names))),
                    None,
                )

            phone = first_value("telefono")
            mobile = first_value("celular")
            values = {
                "cad_proveedor": code,
                "nombre": first_value("nombre proveedor"),
                "contacto": first_value("contacto"),
                "direccion": first_value("direccion"),
                "telefono": phone,
                "celular": mobile,
                "web": first_value("web"),
                "correo": first_value("correo"),
            }
            required = ("nombre", "contacto", "direccion", "telefono", "celular", "correo")
            if any(not values[field] for field in required):
                providers_skipped += 1
            else:
                valid_providers[code] = values

        for row in _read_sheet(workbook, "TABLA_5_CLIENTES"):
            code = _first(row, "codigo")
            name = _first(row, "cliente")
            if not code or not name:
                continue
            quantity = _number(_first(row, "cantidad promedio kg"))
            client_rows.append(
                {
                    "codigo_cliente": code,
                    "cliente": name,
                    "razon_social": _first(row, "razon social"),
                    "telefono1": _first(row, "telefono 1"),
                    "telefono2": _first(row, "telefono 2"),
                    "contacto": _first(row, "contacto"),
                    "correo": _first(row, "correo"),
                    "ciudad": _first(row, "ciudad"),
                    "tipo_agua": _first(row, "tipo de agua"),
                    "cantidad_promedio_kg": quantity,
                }
            )

        for product in products.values():
            sources = product["warehouse_sources"]
            product["warehouse_name"] = (
                next(iter(sources)) if len(sources) == 1 else None
            )

        valid_product_codes = set(products)
        location_rows = [
            row for row in location_rows
            if row["codigo_producto"] in valid_product_codes
        ]
        location_stock = {
            key: quantity
            for key, quantity in location_stock.items()
            if key[1] in valid_product_codes
        }

        provider_products = {}
        for row in provider_product_rows:
            provider_code = row["provider_code"]
            product_code = row["product_code"]
            if (
                not provider_code
                or not product_code
                or provider_code not in valid_providers
                or product_code not in products
            ):
                continue
            pair = (product_code, provider_code)
            provider_name = valid_providers[provider_code]["nombre"]
            primary_name = primary_provider_names.get(product_code, "")
            provider_products[pair] = {
                **row,
                "is_primary": bool(primary_name)
                and _normalize(primary_name)
                in {_normalize(provider_code), _normalize(provider_name)},
            }

        unsupported = [name for name in UNSUPPORTED_SHEETS if name in workbook.sheetnames]
        return {
            "products": products,
            "providers": valid_providers,
            "providers_skipped": providers_skipped,
            "provider_products": provider_products,
            "clients": client_rows,
            "locations": location_rows,
            "location_stock": location_stock,
            "warehouse_quantities": warehouse_quantities,
            "inventory_rows_without_quantity": inventory_rows_without_quantity,
            "warehouse_names": sorted(
                {
                    warehouse_name
                    for product in products.values()
                    for warehouse_name in product["warehouse_sources"]
                }
            ),
            "product_name_variants": product_name_variants,
            "unsupported_sheets": unsupported,
        }
    finally:
        workbook.close()


def _print_preview(plan: dict[str, Any]) -> None:
    print("Validated workbook import preview:")
    print(f"  Products: {len(plan['products'])}")
    print(f"  Suppliers: {len(plan['providers'])} usable; {plan['providers_skipped']} skipped")
    print(f"  Supplier-product links: {len(plan['provider_products'])}")
    print(f"  Clients: {len(plan['clients'])}")
    print(f"  Physical location rows: {len(plan['locations'])}")
    print(f"  Product/location stock rows: {len(plan['location_stock'])}")
    print(f"  Aggregate stock rows: {len(plan['warehouse_quantities'])}")
    print(f"  Rows without a quantity: {plan['inventory_rows_without_quantity']}")
    print(
        "  Product name variants across sheets "
        f"(first source name retained): {plan['product_name_variants']}"
    )
    print(f"  Warehouse/process groups: {', '.join(plan['warehouse_names']) or 'none'}")
    print(
        "  Unsupported sheets (kept in the original workbook): "
        + (", ".join(plan["unsupported_sheets"]) or "none")
    )


def _apply_plan(plan: dict[str, Any], args: argparse.Namespace) -> None:
    from app.infrastructure.db.models.client_orm import ClientORM
    from app.infrastructure.db.models.company_orm import Company
    from app.infrastructure.db.models.location_orm import LocationORM
    from app.infrastructure.db.models.process_orm import ProcessORM
    from app.infrastructure.db.models.product_provider_orm import ProductProviderORM
    from app.infrastructure.db.models.products_orm import Product
    from app.infrastructure.db.models.provider_orm import ProviderORM
    from app.infrastructure.db.models.stock_orm import StockLocationORM, StockWarehouseORM
    from app.infrastructure.db.session import SessionLocal
    import uuid

    company_values = {
        "name": args.company_name,
        "nit": args.company_nit,
        "address": args.company_address,
        "phone": args.company_phone,
        "email": args.company_email,
    }

    with SessionLocal.begin() as session:
        company = session.query(Company).filter(Company.nit == args.company_nit).first()
        if company is None:
            company = session.query(Company).filter(
                Company.email == args.company_email
            ).first()
        if company is None:
            company = Company(**company_values)
            session.add(company)
            session.flush()
        elif any(getattr(company, key) != value for key, value in company_values.items()):
            raise ValueError(
                "An existing company matches the supplied NIT or email but has "
                "different identity fields; refusing to overwrite it."
            )

        company_id = company.id_company
        processes = {}
        for name in plan["warehouse_names"]:
            process = session.query(ProcessORM).filter(
                ProcessORM.id_empresa == company_id,
                ProcessORM.nombre == name,
                ProcessORM.tipo_proceso == "almacenamiento",
            ).first()
            if process is None:
                process = ProcessORM(
                    id_proceso=uuid.uuid4(),
                    nombre=name,
                    descripcion=f"Importado desde {args.workbook.name}",
                    tipo_proceso="almacenamiento",
                    id_empresa=company_id,
                    is_active=True,
                )
                session.add(process)
                session.flush()
            processes[name] = process

        for code, values in plan["providers"].items():
            provider = session.query(ProviderORM).filter(
                ProviderORM.cad_proveedor == code
            ).first()
            if provider is not None and provider.id_empresa != company_id:
                raise ValueError(f"Supplier code {code} already belongs to another company.")
            if provider is None:
                provider = ProviderORM(cad_proveedor=code, **{
                    key: value for key, value in values.items() if key != "cad_proveedor"
                }, id_empresa=company_id)
                session.add(provider)
            else:
                for key, value in values.items():
                    if key != "cad_proveedor":
                        setattr(provider, key, value)

        for code, values in plan["products"].items():
            product = session.query(Product).filter(Product.id_product == code).first()
            if product is not None and product.company_id != company_id:
                raise ValueError(f"Product code {code} already belongs to another company.")
            warehouse_name = values["warehouse_name"]
            fields = {
                "name": values["name"],
                "generic_name": values["generic_name"],
                "price": "0",
                "unit_measure": values["unit_measure"],
                "unit_price": "0",
                "min_unit_price": "0",
                "lead_time_days": "0",
                "restorage": "",
                "warehouse_id": processes[warehouse_name].id_proceso if warehouse_name else None,
                "company_id": company_id,
                "fds": values["fds"],
                "fds_url": None,
            }
            if product is None:
                product = Product(id_product=code, **fields)
                session.add(product)
            else:
                for key, value in fields.items():
                    setattr(product, key, value)

        session.flush()

        for pair, values in plan["provider_products"].items():
            product_code, provider_code = pair
            relation = session.query(ProductProviderORM).filter(
                ProductProviderORM.codigo_producto == product_code,
                ProductProviderORM.cad_proveedor == provider_code,
            ).first()
            relation_values = {
                "es_principal": values["is_primary"],
                "precio": values["price"],
            }
            if relation is None:
                session.add(
                    ProductProviderORM(
                        codigo_producto=product_code,
                        cad_proveedor=provider_code,
                        **relation_values,
                    )
                )
            else:
                for key, value in relation_values.items():
                    setattr(relation, key, value)

        location_ids = {}
        for row in plan["locations"]:
            key = row["key"]
            location = session.query(LocationORM).filter(
                LocationORM.id_empresa == company_id,
                LocationORM.ubicacion == row["ubicacion"],
                LocationORM.nivel == row["nivel"],
                LocationORM.posicion == row["posicion"],
                LocationORM.localizador == row["localizador"],
            ).first()
            if location is None:
                location = LocationORM(
                    ubicacion=row["ubicacion"],
                    nivel=row["nivel"],
                    posicion=row["posicion"],
                    localizador=row["localizador"],
                    tipo_ubicacion=row["tipo_ubicacion"],
                    id_empresa=company_id,
                )
                session.add(location)
                session.flush()
            location_ids[key] = location.id_ubicacion

        for (location_key, product_code), quantity in plan["location_stock"].items():
            stock = session.query(StockLocationORM).filter(
                StockLocationORM.id_ubicacion == location_ids[location_key],
                StockLocationORM.codigo_producto == product_code,
            ).first()
            if stock is None:
                session.add(
                    StockLocationORM(
                        id_ubicacion=location_ids[location_key],
                        codigo_producto=product_code,
                        cantidad=quantity,
                        id_empresa=company_id,
                    )
                )
            else:
                stock.cantidad = quantity

        for product_code, quantity in plan["warehouse_quantities"].items():
            stock = session.query(StockWarehouseORM).filter(
                StockWarehouseORM.codigo_producto == product_code
            ).first()
            if stock is not None and stock.id_empresa != company_id:
                raise ValueError(
                    f"Stock code {product_code} already belongs to another company."
                )
            if stock is None:
                session.add(
                    StockWarehouseORM(
                        codigo_producto=product_code,
                        cantidad=quantity,
                        id_empresa=company_id,
                    )
                )
            else:
                stock.cantidad = quantity

        for values in plan["clients"]:
            client = session.query(ClientORM).filter(
                ClientORM.codigo_cliente == values["codigo_cliente"]
            ).first()
            if client is not None and client.id_empresa != company_id:
                raise ValueError(
                    f"Client code {values['codigo_cliente']} already belongs to another company."
                )
            fields = {
                **values,
                "id_empresa": company_id,
                "is_active": True,
            }
            if client is None:
                session.add(ClientORM(**fields))
            else:
                for key, value in fields.items():
                    setattr(client, key, value)

    print(f"Imported workbook data for company {args.company_name!r}.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workbook",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "ultima bd.xlsx",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the validated data to the database; preview is the default.",
    )
    parser.add_argument(
        "--accept-name-priority",
        action="store_true",
        help="Accept the first source name when workbook sheets disagree.",
    )
    parser.add_argument("--company-name")
    parser.add_argument("--company-nit")
    parser.add_argument("--company-address")
    parser.add_argument("--company-phone")
    parser.add_argument("--company-email")
    args = parser.parse_args()

    plan = build_plan(args.workbook)
    _print_preview(plan)
    if not args.apply:
        print("Preview only; no database connection or writes were made.")
        return

    if plan["product_name_variants"] and not args.accept_name_priority:
        parser.error(
            "The workbook contains product name variants. Review the preview "
            "and add --accept-name-priority to retain the first source name."
        )

    required = (
        "company_name",
        "company_nit",
        "company_address",
        "company_phone",
        "company_email",
    )
    missing = [field for field in required if not getattr(args, field)]
    if missing:
        parser.error(
            "Applying requires company details: " + ", ".join("--" + name.replace("_", "-") for name in missing)
        )
    _apply_plan(plan, args)


if __name__ == "__main__":
    main()
