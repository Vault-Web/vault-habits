# Vault Habits

**Vault Habits** is the habit-tracking service for the **Vault Web ecosystem**.
It provides a focused, self-hosted habit dashboard that can run standalone or
behind Vault Web authentication.

<img src='https://github.com/daya0576/beaverhabits/assets/6239652/0418fa41-8985-46ef-b623-333b62b2f92e' width='250'>

## Overview

Vault Habits helps users track daily routines, streaks, and long-term progress
without adding goal complexity. The service is based on a NiceGUI/FastAPI
application and stores habit data per user.

Within Vault Web, Habits can accept a Vault Web JWT handoff from an external
link. This keeps Vault Web responsible for authentication while Habits owns its
local habit records and progress views.

## Local Development

Vault Habits uses [uv](https://docs.astral.sh/uv/getting-started/) for Python
environment and dependency management.

```sh
uv venv
uv sync
uv run ./start.sh dev
```

The development server runs at:

```text
http://localhost:9001
```

## Vault Web Login Handoff

Set the Vault Web JWT secret to the same access-token secret used by Vault Web.
`VAULT_WEB_LOGIN_URL` sends unauthenticated Habits visits back to Vault Web, and
`VAULT_WEB_HOME_URL` powers the in-app return button. `VAULT_WEB_AUTH_ONLY`
disables BeaverHabits local auth endpoints for this mode.

```sh
export VAULT_WEB_JWT_SECRET=replace_with_vault_web_jwt_secret
export VAULT_WEB_LOGIN_URL='http://localhost:4200/login?externalLink=Habits'
export VAULT_WEB_HOME_URL='http://localhost:4200'
export VAULT_WEB_AUTH_ONLY=true
uv run ./start.sh dev
```

The Vault Web external link should point to `/vault-web-login` and opt in to
token forwarding:

```js
{
  name: "Habits",
  url: "http://localhost:9001/vault-web-login",
  forwardVaultWebToken: true,
}
```

Habits derives an internal email-like identifier from the Vault Web `userId`.
Set `VAULT_WEB_USER_EMAIL_DOMAIN` only if the default `vaultweb.app` mapping
domain does not fit your installation.

## Configuration

For local Vault Web integration, `.env` can provide:

```sh
VAULT_WEB_JWT_SECRET=replace_with_vault_web_jwt_secret
VAULT_WEB_LOGIN_URL=http://localhost:4200/login?externalLink=Habits
VAULT_WEB_HOME_URL=http://localhost:4200
VAULT_WEB_AUTH_ONLY=true
VAULT_WEB_USER_EMAIL_DOMAIN=vaultweb.app

HABITS_STORAGE=DATABASE
DATABASE_URL=sqlite+aiosqlite:///./.user/habits.db
NICEGUI_STORAGE_SECRET=dev
```

## Testing

Run the test suite with:

```sh
DATABASE_URL="sqlite+aiosqlite:///:memory:" \
HABITS_STORAGE="USER_DISK" \
VAULT_WEB_AUTH_ONLY="false" \
DEBUG="false" \
uv run pytest
```

For focused stats tests:

```sh
env DEBUG=false uv run pytest tests/test_stats_page.py
```

## Notes

Vault Habits is maintained as part of the Vault Web self-hosted service stack.
The project keeps the original habit-tracking foundation while aligning local
authentication, progress reporting, and deployment workflows with Vault Web.
