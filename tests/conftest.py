import os

os.environ["VAULT_WEB_AUTH_ONLY"] = "false"
os.environ.setdefault("DEBUG", "false")

pytest_plugins = ["nicegui.testing.plugin"]
