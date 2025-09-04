#02_create_table.py
from client import conn

# Create a "users" table if it doesn't exist already
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);
""")
conn.commit()
conn.sync()

print("✅ Table 'users' created (if not already present).")
