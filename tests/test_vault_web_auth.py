import time

import jwt
import pytest

from beaverhabits.app.vault_web_auth import (
    _decode_vault_web_payload,
    decode_vault_web_subject_email,
)
from beaverhabits.configs import settings


@pytest.fixture(autouse=True)
def vault_web_settings():
    old_secret = settings.VAULT_WEB_JWT_SECRET
    old_domain = settings.VAULT_WEB_USER_EMAIL_DOMAIN
    settings.VAULT_WEB_JWT_SECRET = "vault-web-test-secret-at-least-32-bytes"
    settings.VAULT_WEB_USER_EMAIL_DOMAIN = "vaultweb.app"
    yield
    settings.VAULT_WEB_JWT_SECRET = old_secret
    settings.VAULT_WEB_USER_EMAIL_DOMAIN = old_domain


def test_vault_web_token_maps_user_id_to_habits_email():
    token = jwt.encode(
        {"sub": "deniz", "userId": 42, "exp": int(time.time()) + 60},
        settings.VAULT_WEB_JWT_SECRET,
        algorithm="HS512",
    )

    assert decode_vault_web_subject_email(token) == "vault-web-42@vaultweb.app"
    assert _decode_vault_web_payload(token)["sub"] == "deniz"


def test_vault_web_token_rejects_expired_token():
    token = jwt.encode(
        {"sub": "deniz", "userId": 42, "exp": int(time.time()) - 60},
        settings.VAULT_WEB_JWT_SECRET,
        algorithm="HS256",
    )

    with pytest.raises(ValueError, match="invalid or expired"):
        decode_vault_web_subject_email(token)
