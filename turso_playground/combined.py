# combined.py
from client import conn

def create_table():
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    );
    """)
    conn.commit()
    conn.sync()
    print("✅ Table 'users' created (if not already).")

def insert_one():
    try:
        uid = int(input("Enter id (integer): ").strip())
        name = input("Enter name: ").strip()
        email = input("Enter email: ").strip()
        conn.execute(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?);",
            (uid, name, email)
        )
        conn.commit()
        conn.sync()
        print(f"✅ Inserted: id={uid}, name={name}, email={email}")
    except Exception as e:
        print("❌ Insert failed:", e)

def insert_many():
    print("Enter multiple users. Leave name empty to finish.")
    rows = []
    while True:
        name = input("Name: ").strip()
        if not name:
            break
        try:
            uid = int(input("  ID (integer): ").strip())
        except ValueError:
            print("  ⚠️ ID must be an integer. Try again.")
            continue
        email = input("  Email: ").strip()
        rows.append((uid, name, email))

    if not rows:
        print("ℹ️ No rows to insert.")
        return

    try:
        conn.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?);",
            rows
        )
        conn.commit()
        conn.sync()
        print(f"✅ Inserted {len(rows)} users.")
    except Exception as e:
        print("❌ Bulk insert failed:", e)

def query_all():
    rows = conn.execute("SELECT id, name, email FROM users ORDER BY id;").fetchall()
    if not rows:
        print("ℹ️ No users found.")
        return
    print("✅ Users:")
    for r in rows:
        print(f"- id={r[0]} | name={r[1]} | email={r[2]}")

def query_one():
    print("Search by: 1) id  2) name")
    choice = input("Choose 1 or 2: ").strip()
    if choice == "1":
        try:
            uid = int(input("Enter id: ").strip())
        except ValueError:
            print("⚠️ ID must be an integer.")
            return
        row = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?;",
            (uid,)
        ).fetchone()
    elif choice == "2":
        name = input("Enter name: ").strip()
        row = conn.execute(
            "SELECT id, name, email FROM users WHERE name = ?;",
            (name,)
        ).fetchone()
    else:
        print("⚠️ Invalid choice.")
        return

    if row:
        print(f"✅ Found: id={row[0]} | name={row[1]} | email={row[2]}")
    else:
        print("❌ No matching user found.")

def update_email():
    try:
        uid = int(input("Enter user id to update: ").strip())
        new_email = input("Enter new email: ").strip()
        cur = conn.execute(
            "UPDATE users SET email = ? WHERE id = ?;",
            (new_email, uid)
        )
        conn.commit()
        conn.sync()
        if cur.rowcount == 0:
            print("❌ No user updated (check id).")
        else:
            print(f"✅ Updated id={uid} to email={new_email}")
    except Exception as e:
        print("❌ Update failed:", e)

def delete_user():
    try:
        uid = int(input("Enter user id to delete: ").strip())
        cur = conn.execute("DELETE FROM users WHERE id = ?;", (uid,))
        conn.commit()
        conn.sync()
        if cur.rowcount == 0:
            print("❌ No user deleted (check id).")
        else:
            print(f"✅ Deleted user with id={uid}")
    except Exception as e:
        print("❌ Delete failed:", e)

def verify_deleted():
    try:
        uid = int(input("Enter user id to verify deletion: ").strip())
        row = conn.execute(
            "SELECT id FROM users WHERE id = ?;",
            (uid,)
        ).fetchone()
        if row:
            print(f"❌ User still exists: id={row[0]}")
        else:
            print(f"✅ User with id={uid} was deleted.")
    except Exception as e:
        print("❌ Verification failed:", e)

def menu():
    actions = {
        "1": ("Create table", create_table),
        "2": ("Insert one user", insert_one),
        "3": ("Insert many users", insert_many),
        "4": ("Query all users", query_all),
        "5": ("Query one user (filter)", query_one),
        "6": ("Update user email", update_email),
        "7": ("Delete user", delete_user),
        "8": ("Verify deletion", verify_deleted),
        "0": ("Exit", None),
    }

    while True:
        print("\n=== Turso (libsql) Menu ===")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("👋 Bye!")
            break

        action = actions.get(choice)
        if not action:
            print("⚠️ Invalid choice. Try again.")
            continue

        _, fn = action
        try:
            fn()
        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    menu()
