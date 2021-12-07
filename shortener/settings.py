import os

from tomlkit import loads

APP_VERSION = "0.1.0"

APP_TITLE = "🗃️ inventory"
APP_NAME = "Short of Inventory"

APP_BASE_URL = "i.hsp.sh"

APP_HOME_URL = "//hsp.sh"
APP_WIKI_URL = "//wiki.hsp.sh/short-of-inventory"
APP_REPO_URL = "//github.com/hspsh/short-of-inventory"

SECRET_KEY = os.environ["SECRET_KEY"]
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")

with open("config.toml") as f:
    config = loads(f.read())
