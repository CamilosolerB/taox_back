from app.settings import Settings


def test_settings_ignores_extra_env_keys(monkeypatch):
    monkeypatch.setenv("STAGE", "test")
    monkeypatch.setenv("DB_URL", "postgresql://localhost/test_db")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("ADMIN_ROLE_ID", "admin-role")
    monkeypatch.setenv("OBSERVER_ROLE_ID", "observer-role")
    monkeypatch.setenv("db_url_railway", "postgresql://railway/test_db")
    monkeypatch.setenv("COMPANY_ID", "company-1")

    settings = Settings()

    assert settings.STAGE == "test"
    assert settings.DB_URL == "postgresql://localhost/test_db"
    assert settings.JWT_SECRET_KEY == "test-secret"
    assert settings.ADMIN_ROLE_ID == "admin-role"
    assert settings.OBSERVER_ROLE_ID == "observer-role"
