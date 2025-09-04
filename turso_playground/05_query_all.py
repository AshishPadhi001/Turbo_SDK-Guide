# 05_query_all.py
from client import conn

rows = conn.execute("SELECT id, name, email FROM users ORDER BY id;").fetchall()

print("✅ Users:")
for r in rows:
    print(f"- id={r[0]} | name={r[1]} | email={r[2]}")
