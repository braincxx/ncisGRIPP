from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

env_path = os.path.join(basedir, ".env")
if os.path.exists(env_path):
    load_dotenv(verbose=True, dotenv_path=env_path)

TOKEN = os.environ.get("BOT_TOKEN", None)
SQL_USER = os.environ.get("SQL_USER", None)
SQL_PASS = os.environ.get("SQL_PASS", None)
SQL_HOST = os.environ.get("SQL_HOST", None)
SQL_TABLE = os.environ.get("SQL_TABLE", None)
