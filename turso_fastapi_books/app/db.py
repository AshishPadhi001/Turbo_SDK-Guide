# app/db.py
import os
from dotenv import load_dotenv
import libsql

# Load environment variables
load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_TOKEN = os.getenv("DB_AUTH_TOKEN")

if not DB_URL or not DB_TOKEN:
    raise RuntimeError("DB_URL and DB_AUTH_TOKEN must be set in your .env file")

# Direct remote connection (no local replica file)
conn = libsql.connect(DB_URL, auth_token=DB_TOKEN)

def init_tables() -> None:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """)
    conn.commit()
