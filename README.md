# 🚀 Turso + Python (libsql) with FastAPI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Turso](https://img.shields.io/badge/Turso-SQLite%20Cloud-green.svg)](https://turso.tech)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com)

Build and deploy FastAPI apps backed by Turso (SQLite in the cloud) using the official Python `libsql` client. This guide shows how to connect to your Turso database, run queries, and structure a small API—without using the CLI.

- Works anywhere Python runs
- Direct remote connection via `libsql`
- No Turso CLI needed (use Dashboard for URL and token)

> Why this matters: Turso gives you globally replicated, serverless SQLite with token-based auth. Combined with FastAPI, you get a modern API stack that’s fast, simple, and cost‑efficient.

## 📚 Overview

This repository contains:
- A minimal FastAPI service in `turso_fastapi_books/` that demonstrates CRUD with Turso via `libsql`.
- A practical playground in `turso_playground/` showing connection, DDL, DML, and queries.
- Documentation for setup, configuration, and best practices.

If you are evaluating “Turso with Python and FastAPI”, this repo gives you a working reference implementation and scripts you can copy.

## 📋 Table of Contents

- [What is Turso?](#what-is-turso)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Playground Examples](#playground-examples)
- [FastAPI Integration](#fastapi-integration)
- [API Reference](#api-reference)
- [Environment Setup](#environment-setup)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQs](#faqs)
- [Dependencies](#dependencies)
- [Repository and Docs](#repository-and-docs)
- [Contributing](#contributing)
- [License](#license)

## What is Turso?

[Turso](https://turso.tech) is a **SQLite-compatible cloud database** with:
- 🌐 Global edge replicas close to your users
- ⚡ Low-latency reads/writes
- 🔒 Secure, token-based access
- 🔄 Automatic sync

Perfect for Python + FastAPI apps that need a globally distributed, serverless database.

Typical use cases: API backends, dashboards, edge apps, prototypes, hackathons, and low‑ops microservices.

## Quick Start

### Prerequisites
- Python 3.8+
- A Turso account and database in the [Turso Dashboard](https://app.turso.tech)

### Setup

1) Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Get your database URL and token (no CLI)
- Open the [Turso Dashboard](https://app.turso.tech)
- Create/select your database
- Copy:
  - DB URL (e.g., `libsql://your-db-name.turso.io`)
  - Auth token (generate if needed)

4) Add credentials to `.env`
```env
DB_URL=libsql://your-db-name.turso.io
DB_AUTH_TOKEN=your-auth-token
```

5) Run the playground
```bash
cd turso_playground
python combined.py
```

## Configuration

Environment variables (from `.env` or host env):

- `DB_URL` — Turso libsql URL, e.g. `libsql://your-db-name.turso.io`
- `DB_AUTH_TOKEN` — Auth token generated in the Turso Dashboard

Loading and connecting (excerpt):
```python
from dotenv import load_dotenv
import os, libsql

load_dotenv()
url = os.getenv("DB_URL")
token = os.getenv("DB_AUTH_TOKEN")
conn = libsql.connect(url, auth_token=token)
```

Security note: never commit `.env`. Use a secrets manager or environment variables in production.

## Playground Examples

The `turso_playground/` folder includes step-by-step scripts:
- Connect and sync
- Create tables
- Insert single/bulk rows
- Query all/one
- Update and delete

Each example uses the same `libsql` connection configured from `.env`.

## FastAPI Integration

Project layout:
```
turso_fastapi_books/
├── app/
│   ├── __init__.py
│   ├── db.py              # libsql connection via DB_URL + token
│   ├── schemas.py         # Pydantic models
│   └── routers/
│       ├── books.py       # Books CRUD API
│       └── students.py    # Students CRUD API
├── main.py                # FastAPI app entrypoint
└── requirements.txt
```

Connection (`app/db.py`):
```python
import os
from dotenv import load_dotenv
import libsql

load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_TOKEN = os.getenv("DB_AUTH_TOKEN")

if not DB_URL or not DB_TOKEN:
    raise RuntimeError("DB_URL and DB_AUTH_TOKEN must be set in your .env file")

conn = libsql.connect(DB_URL, auth_token=DB_TOKEN)
```

Run the API:
```bash
cd turso_fastapi_books
python main.py
# Docs: http://127.0.0.1:8007/docs
```

## API Reference

Base URL (local): `http://127.0.0.1:8007`

### Books

- GET `/books` — list books
```bash
curl http://127.0.0.1:8007/books
```

- POST `/books` — create a book
```bash
curl -X POST http://127.0.0.1:8007/books \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Clean Code","author":"Robert C. Martin","year":2008}'
```

- GET `/books/{id}` — get by id
```bash
curl http://127.0.0.1:8007/books/1
```

- PUT `/books/{id}` — update
```bash
curl -X PUT http://127.0.0.1:8007/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Clean Code (2nd)","author":"Robert C. Martin","year":2025}'
```

- DELETE `/books/{id}` — delete
```bash
curl -X DELETE http://127.0.0.1:8007/books/1
```

### Students

- GET `/students` — list students
```bash
curl http://127.0.0.1:8007/students
```

- POST `/students` — create a student
```bash
curl -X POST http://127.0.0.1:8007/students \
  -H "Content-Type: application/json" \
  -d '{"id":1,"name":"Alice","email":"alice@example.com"}'
```

- GET `/students/{id}` — get by id
```bash
curl http://127.0.0.1:8007/students/1
```

- PUT `/students/{id}` — update
```bash
curl -X PUT http://127.0.0.1:8007/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Johnson","email":"alice.j@example.com"}'
```

- DELETE `/students/{id}` — delete
```bash
curl -X DELETE http://127.0.0.1:8007/students/1
```

## Environment Setup

- Create a Turso account at the [website](https://turso.tech)
- Use the [Dashboard](https://app.turso.tech) to create a database
- Copy the database URL and an auth token into your `.env`

Tip: never commit `.env` files. This repo’s `.gitignore` already excludes them.

## Best Practices

- **Secrets management**: Store `DB_AUTH_TOKEN` in environment variables or a secrets manager in production.
- **Least privilege**: Use scoped tokens; rotate them regularly.
- **Connection usage**: Prefer one connection per worker process; reuse across requests where possible.
- **Transactions**: Group related writes in transactions to maintain consistency and reduce round trips.
- **Pagination**: Use `LIMIT/OFFSET` or keyset pagination for large lists.
- **Validation**: Leverage Pydantic models for input/output schemas.
- **Error handling**: Return consistent error shapes; log server-side details, not secrets.

## Troubleshooting

- **Auth errors (401/403)**: Verify `DB_AUTH_TOKEN` is valid and not expired. Generate a new token in the Turso Dashboard.
- **Invalid URL**: Make sure `DB_URL` starts with `libsql://` and matches your database name.
- **Firewall/Proxy**: Ensure outbound connections to Turso are allowed from your environment.
- **.env not loading**: Confirm the `.env` file exists where the app runs and that `python-dotenv` is installed.

## FAQs

- **Do I need the Turso CLI?** No. This guide uses the Dashboard for URL/token, and the Python `libsql` client for connectivity.
- **Can I run locally without the internet?** Turso is a cloud service; direct remote connections require network access.
- **Is SQLite fully compatible?** Turso is SQLite‑compatible with additional cloud features; most SQLite syntax works.
- **How do I migrate schemas?** Manage DDL with versioned scripts and run them at app startup (see `init_tables()`), or through a deployment step.

## Dependencies

- libsql: Official Turso Python client
- fastapi: Modern, type-hinted web framework
- uvicorn: ASGI server for FastAPI
- pydantic: Validation and settings management
- python-dotenv: Load environment variables from `.env`

## Repository and Docs

- Repository: [`Turbo_SDK-Guide`](https://github.com/AshishPadhi001/Turbo_SDK-Guide.git)
- Project Docs (comment/view access): [`Google Doc`](https://docs.google.com/document/d/1Bn9tiRwED_4paN0r90-zfh2dvS-szP1_3T7-XkPD8Ag/edit?tab=t.0#heading=h.smg2chjtk0fu)
- Need edit access? Email: `padhiashish001@gmail.com`

## Contributing

We welcome contributions! To propose changes:
- Open an issue describing the improvement or bug
- Or submit a pull request with a clear description and minimal diff
- For edit access to the Google Doc, email `padhiashish001@gmail.com`

## License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for details.

---

Need more? We can add examples for pagination, transactions, and connection pooling best practices with `libsql` and FastAPI.

<!-- SEO Keywords: Turso, libsql, FastAPI, Python, SQLite cloud, edge database, serverless SQLite, connect to Turso from Python, Turso FastAPI guide, libsql tutorial, Turso dashboard URL token, global SQLite replicas, low latency database for FastAPI, Python .env database config -->