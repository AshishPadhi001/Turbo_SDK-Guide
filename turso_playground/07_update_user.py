# 07_update_user.py
from client import conn

# Example: update Alice's email
user_id = 1
new_email = "alice.new@example.com"

conn.execute(
    "UPDATE users SET email = ? WHERE id = ?;",
    (new_email, user_id)
)
conn.commit()
conn.sync()

print(f"✅ Updated user with id={user_id} to email={new_email}")
