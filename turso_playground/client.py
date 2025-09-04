# client.py
import os
from dotenv import load_dotenv
import libsql

# Load DB connection details from a .env in this directory (or project root)
load_dotenv()
DB_URL = os.getenv("DB_URL")
DB_TOKEN = os.getenv("DB_AUTH_TOKEN")

if not DB_URL or not DB_TOKEN:
    raise RuntimeError("DB_URL and DB_AUTH_TOKEN must be set in your .env file")

# Direct remote connection (no local replica file)
conn = libsql.connect(DB_URL, auth_token=DB_TOKEN)