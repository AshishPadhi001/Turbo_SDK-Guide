# 04_insert_many.py
from client import conn

# Sample users
users = [
    (2, "Bob", "bob@example.com"),
    (3, "Charlie", "charlie@example.com"),
    (4, "Diana", "diana@example.com"),
]

# Insert multiple rows using executemany
conn.executemany(
    "INSERT INTO users (id, name, email) VALUES (?, ?, ?);",
    users
)
conn.commit()
conn.sync()

print(f"✅ Inserted {len(users)} users successfully!")
