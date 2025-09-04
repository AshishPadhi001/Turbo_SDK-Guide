# 08_delete_user.py
from client import conn

# Example: delete user with id = 2 (Bob)
user_id = 2

conn.execute("DELETE FROM users WHERE id = ?;", (user_id,))
conn.commit()
conn.sync()

print(f"✅ Deleted user with id={user_id}")
