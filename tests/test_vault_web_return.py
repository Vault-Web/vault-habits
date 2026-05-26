from beaverhabits.configs import settings
from beaverhabits.frontend.layout import get_vault_web_home_url


def test_vault_web_home_url_prefers_explicit_setting(monkeypatch):
    monkeypatch.setattr(settings, "VAULT_WEB_HOME_URL", "https://vault.example/app")
    monkeypatch.setattr(
        settings,
        "VAULT_WEB_LOGIN_URL",
        "http://localhost:4200/login?externalLink=Habits",
    )

    assert get_vault_web_home_url() == "https://vault.example/app"


def test_vault_web_home_url_uses_login_origin(monkeypatch):
    monkeypatch.setattr(settings, "VAULT_WEB_HOME_URL", "")
    monkeypatch.setattr(
        settings,
        "VAULT_WEB_LOGIN_URL",
        "http://localhost:4200/login?externalLink=Habits",
    )

    assert get_vault_web_home_url() == "http://localhost:4200"


def test_vault_web_home_url_ignores_relative_login_url(monkeypatch):
    monkeypatch.setattr(settings, "VAULT_WEB_HOME_URL", "")
    monkeypatch.setattr(settings, "VAULT_WEB_LOGIN_URL", "/login?externalLink=Habits")

    assert get_vault_web_home_url() == ""
