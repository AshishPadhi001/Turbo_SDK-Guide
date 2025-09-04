# 🚀 Turso SDK Guide - Python Integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Turso](https://img.shields.io/badge/Turso-SQLite%20Cloud-green.svg)](https://turso.tech)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com)

> **Complete Turso SDK guide for Python developers** - Learn how to integrate Turso (SQLite Cloud) with Python using libsql, FastAPI, and modern development practices.

## 📋 Table of Contents

- [What is Turso?](#what-is-turso)
- [Quick Start](#quick-start)
- [Playground Examples](#playground-examples)
- [FastAPI Integration](#fastapi-integration)
- [Environment Setup](#environment-setup)
- [Contributing](#contributing)

## What is Turso?

[Turso](https://turso.tech) is a **SQLite-compatible cloud database** that provides:

- 🌐 **Global Edge Replication** - Deploy your database close to your users
- ⚡ **Lightning Fast** - Sub-millisecond query response times
- 🔒 **Secure by Default** - Built-in authentication and encryption
- 💰 **Cost Effective** - Pay only for what you use
- 🔄 **Real-time Sync** - Automatic data synchronization across regions

This guide demonstrates how to integrate Turso with Python applications using the official `libsql` Python SDK.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Turso account ([Sign up](https://turso.tech))
- A Turso database (create in the [Turso Dashboard](https://app.turso.tech))
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/turso-sdk-guide.git
cd turso-sdk-guide
```

2. **Create a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Get your database URL and token (no CLI needed)**
- Go to the [Turso Dashboard](https://app.turso.tech)
- Create a database (if you don’t already have one)
- Open the database and copy:
  - Database URL (e.g., `libsql://your-db-name.turso.io`)
  - Auth Token (generate one if needed)

5. **Set up environment variables**
```bash
# Create .env file in turso_playground/ or project root as you prefer
DB_URL=libsql://your-database-name.turso.io
DB_AUTH_TOKEN=your-auth-token-here
```

6. **Run the playground**
```bash
cd turso_playground
python combined.py
```

## Playground Examples

The playground includes 8 comprehensive examples that teach you everything about Turso:

### 1. Connection & Sync
```python
# 01_connect.py
from client import conn
conn.sync()
print("✅ Connected & synced successfully!")
```

### 2. Table Creation
```python
# 02_create_table.py
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);
""")
conn.commit()
conn.sync()
```

### 3. Single Record Insert
```python
# 03_insert.py
conn.execute(
    "INSERT INTO users (id, name, email) VALUES (?, ?, ?);",
    (1, "Alice", "alice@example.com")
)
conn.commit()
conn.sync()
```

### 4. Bulk Insert
```python
# 04_insert_many.py
users = [
    (2, "Bob", "bob@example.com"),
    (3, "Charlie", "charlie@example.com"),
    (4, "Diana", "diana@example.com"),
]
conn.executemany(
    "INSERT INTO users (id, name, email) VALUES (?, ?, ?);",
    users
)
conn.commit()
conn.sync()
```

### 5. Query All Records
```python
# 05_query_all.py
rows = conn.execute("SELECT id, name, email FROM users ORDER BY id;").fetchall()
for row in rows:
    print(f"id={row[0]} | name={row[1]} | email={row[2]}")
```

### 6. Query Single Record
```python
# 06_query_one.py
row = conn.execute(
    "SELECT id, name, email FROM users WHERE name = ?;",
    ("Alice",)
).fetchone()
```

### 7. Update Records
```python
# 07_update_user.py
conn.execute(
    "UPDATE users SET email = ? WHERE id = ?;",
    ("alice.new@example.com", 1)
)
conn.commit()
conn.sync()
```

### 8. Delete Records
```python
# 08_delete_user.py
conn.execute("DELETE FROM users WHERE id = ?;", (2,))
conn.commit()
conn.sync()
```

## FastAPI Integration

### Project Structure
```
turso_fastapi_books/
├── app/
│   ├── __init__.py
│   ├── db.py              # Database connection
│   ├── schemas.py         # Pydantic models
│   └── routers/
│       ├── books.py       # Books CRUD API
│       └── students.py    # Students CRUD API
├── main.py               # FastAPI application
└── requirements.txt
```

### Database Connection
```python
# app/db.py
import os
from dotenv import load_dotenv
import libsql

load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_TOKEN = os.getenv("DB_AUTH_TOKEN")

# Direct remote connection
conn = libsql.connect(DB_URL, auth_token=DB_TOKEN)
```

### Run FastAPI Application
```bash
cd turso_fastapi_books
python main.py
# Visit: http://127.0.0.1:8007/docs
```

## Environment Setup

### 1. Create Turso Account and Database
- Visit the [Turso website](https://turso.tech) and sign up
- Create a database in the [Turso Dashboard](https://app.turso.tech)

### 2. Get Database Credentials (Dashboard)
- Open your database in the dashboard
- Copy the `DB_URL` (e.g., `libsql://your-db-name.turso.io`)
- Generate and copy an `DB_AUTH_TOKEN`

### 3. Environment Variables
Create a `.env` file in your project directory:

```env
# Database Configuration
DB_URL=libsql://your-database-name.turso.io
DB_AUTH_TOKEN=your-auth-token-here
```

## Dependencies

- **libsql** - Official Turso Python SDK
- **fastapi** - Modern web framework for APIs
- **uvicorn** - ASGI server for FastAPI
- **pydantic** - Data validation using Python type hints
- **python-dotenv** - Environment variable management

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ If this guide helped you, please give it a star! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/turso-sdk-guide?style=social)](https://github.com/yourusername/turso-sdk-guide)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/turso-sdk-guide?style=social)](https://github.com/yourusername/turso-sdk-guide)

Made with ❤️ by the Turso Community

</div>