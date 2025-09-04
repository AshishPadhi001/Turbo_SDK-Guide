# 06_query_one.py
from client import conn

# Example: fetch by name
name_to_find = "Hero"

row = conn.execute(
    "SELECT id, name, email FROM users WHERE name = ?;",
    (name_to_find,)
).fetchone()

if row:
    print(f"✅ Found user: id={row[0]} | name={row[1]} | email={row[2]}")
else:
    print(f"❌ No user found with name = {name_to_find}")
