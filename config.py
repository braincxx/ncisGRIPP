from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

env_path = os.path.join(basedir, ".env")
if os.path.exists(env_path):
    load_dotenv(verbose=True, dotenv_path=env_path)

TOKEN = os.environ.get("BOT_TOKEN", None)
