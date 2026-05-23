import hashlib
from typing import Any

import jwt

from beaverhabits import views
from beaverhabits.app import crud
from beaverhabits.app.auth import user_get_by_email
from beaverhabits.app.db import User
from beaverhabits.configs import settings


def _subject_email(payload: dict[str, Any]) -> str:
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("Vault Web token has no username subject")

    user_id = payload.get("userId")
    if isinstance(user_id, (int, str)) and str(user_id).strip():
        identity = str(user_id).strip()
    else:
        identity = hashlib.sha256(subject.encode()).hexdigest()[:24]

    domain = settings.VAULT_WEB_USER_EMAIL_DOMAIN.strip()
    if not domain:
        raise ValueError("Vault Web user email domain is not configured")

    return f"vault-web-{identity}@{domain}"


def _decode_vault_web_payload(token: str) -> dict[str, Any]:
    if not settings.VAULT_WEB_JWT_SECRET:
        raise ValueError("Vault Web JWT login is not configured")

    try:
        return jwt.decode(
            token,
            settings.VAULT_WEB_JWT_SECRET,
            algorithms=["HS256", "HS384", "HS512"],
            options={"require": ["exp", "sub"]},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("Vault Web token is invalid or expired") from exc


def decode_vault_web_subject_email(token: str) -> str:
    return _subject_email(_decode_vault_web_payload(token))


async def user_from_vault_web_token(token: str) -> User:
    payload = _decode_vault_web_payload(token)
    email = _subject_email(payload)
    user = await user_get_by_email(email)
    if not user:
        await views.validate_max_user_count()
        user = await views.register_user(email)

    # Keep the public ranking readable without sharing Vault Web credentials or
    # reaching into its database from Habits.
    await crud.update_user_configs(user, {"vault_web_username": payload["sub"]})
    return user
