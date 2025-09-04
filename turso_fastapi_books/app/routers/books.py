# CRUD for books
# app/routers/books.py
from fastapi import APIRouter, HTTPException
from app.db import conn
from app.schemas import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/books", tags=["books"])

def row_to_book(row) -> BookOut:
    return BookOut(id=row[0], title=row[1], author=row[2], year=row[3])

@router.post("", response_model=BookOut, status_code=201)
def create_book(payload: BookCreate):
    # Ensure unique id
    exists = conn.execute("SELECT id FROM books WHERE id = ?;", (payload.id,)).fetchone()
    if exists:
        raise HTTPException(status_code=409, detail="Book with this id already exists.")

    conn.execute(
        "INSERT INTO books (id, title, author, year) VALUES (?, ?, ?, ?);",
        (payload.id, payload.title, payload.author, payload.year)
    )
    conn.commit()
    
    return payload  # matches BookOut

@router.get("", response_model=list[BookOut])
def list_books():
    rows = conn.execute("SELECT id, title, author, year FROM books ORDER BY id;").fetchall()
    return [row_to_book(r) for r in rows]

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int):
    row = conn.execute("SELECT id, title, author, year FROM books WHERE id = ?;", (book_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Book not found.")
    return row_to_book(row)

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate):
    # Fetch current
    row = conn.execute(
        "SELECT id, title, author, year FROM books WHERE id = ?;",
        (book_id,)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Book not found.")

    current = row_to_book(row)

    # Patch fields
    new_title  = payload.title  if payload.title  is not None else current.title
    new_author = payload.author if payload.author is not None else current.author
    new_year   = payload.year   if payload.year   is not None else current.year

    conn.execute(
        "UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?;",
        (new_title, new_author, new_year, book_id)
    )
    conn.commit()

    return BookOut(id=book_id, title=new_title, author=new_author, year=new_year)

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int):
    cur = conn.execute("DELETE FROM books WHERE id = ?;", (book_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found.")
    return
