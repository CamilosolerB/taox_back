import os
import secrets
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.security import hash_password
from app.infrastructure.db.models.role_orm import Role
from app.infrastructure.db.models.user_orm import User
from app.infrastructure.db.session import SessionLocal
from app.settings import settings


def _append_credentials(email: str, password: str) -> tuple[Path, bytes | None]:
    credentials_path = Path(__file__).with_name("CREDENTIALS.local.md")
    previous_contents = (
        credentials_path.read_bytes() if credentials_path.exists() else None
    )

    safe_email = email.replace("`", "").replace("|", "")
    entry = (
        "\n## TAOX administrator\n\n"
        f"- Email: `{safe_email}`\n"
        f"- Temporary password: `{password}`\n"
        "- Change this password after the first login.\n"
    )
    if previous_contents is None:
        credentials_path.write_text(
            "# Local credentials (do not commit)\n" + entry,
            encoding="utf-8",
        )
    else:
        with credentials_path.open("a", encoding="utf-8") as credentials_file:
            credentials_file.write(entry)

    return credentials_path, previous_contents


def main() -> None:
    admin_email = os.getenv("TAOX_ADMIN_EMAIL", "").strip()
    if not admin_email:
        raise ValueError("Set TAOX_ADMIN_EMAIL before creating the administrator.")

    username = os.getenv("TAOX_ADMIN_USERNAME", "Super Admin")
    generated_password = secrets.token_urlsafe(24)

    with SessionLocal() as db:
        admin_role = (
            db.query(Role)
            .filter(Role.id_role == settings.ADMIN_ROLE_ID)
            .first()
        )
        if not admin_role:
            db.add(Role(id_role=settings.ADMIN_ROLE_ID, name="SuperAdmin"))
            db.flush()

        existing_user = db.query(User).filter(User.email == admin_email).first()
        if existing_user:
            db.commit()
            print(
                f"Administrator '{admin_email}' already exists; "
                "no password was changed."
            )
            return

        credentials_path, previous_contents = _append_credentials(
            admin_email, generated_password
        )
        try:
            db.add(
                User(
                    username=username,
                    email=admin_email,
                    password=hash_password(generated_password),
                    is_active=True,
                    role_id=settings.ADMIN_ROLE_ID,
                    company_id=None,
                )
            )
            db.commit()
        except Exception:
            db.rollback()
            if previous_contents is None:
                credentials_path.unlink(missing_ok=True)
            else:
                credentials_path.write_bytes(previous_contents)
            raise

    print(
        "Administrator created. Credentials were written to "
        "CREDENTIALS.local.md; the file is excluded by .gitignore."
    )


if __name__ == "__main__":
    main()
