# 03_insert.py
from client import conn

# Insert one user
conn.execute(
    "INSERT INTO users (id, name, email) VALUES (?, ?, ?);",
    (1, "Alice", "alice@example.com")
)
conn.commit()
conn.sync()

print("✅ Inserted user: Alice <alice@example.com>")
