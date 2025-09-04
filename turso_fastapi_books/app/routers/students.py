# CRUD for students
# app/routers/students.py
from fastapi import APIRouter, HTTPException
from app.db import conn
from app.schemas import StudentCreate, StudentUpdate, StudentOut

router = APIRouter(prefix="/students", tags=["students"])

def row_to_student(row) -> StudentOut:
    return StudentOut(id=row[0], name=row[1], email=row[2])

@router.post("", response_model=StudentOut, status_code=201)
def create_student(payload: StudentCreate):
    # Ensure unique id
    exists = conn.execute("SELECT id FROM students WHERE id = ?;", (payload.id,)).fetchone()
    if exists:
        raise HTTPException(status_code=409, detail="Student with this id already exists.")

    # Ensure unique email
    email_exists = conn.execute("SELECT id FROM students WHERE email = ?;", (payload.email,)).fetchone()
    if email_exists:
        raise HTTPException(status_code=409, detail="Student with this email already exists.")

    conn.execute(
        "INSERT INTO students (id, name, email) VALUES (?, ?, ?);",
        (payload.id, payload.name, payload.email)
    )
    conn.commit()
    return payload  # matches StudentOut

@router.get("", response_model=list[StudentOut])
def list_students():
    rows = conn.execute("SELECT id, name, email FROM students ORDER BY id;").fetchall()
    return [row_to_student(r) for r in rows]

@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int):
    row = conn.execute("SELECT id, name, email FROM students WHERE id = ?;", (student_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Student not found.")
    return row_to_student(row)

@router.put("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, payload: StudentUpdate):
    # Fetch current
    row = conn.execute(
        "SELECT id, name, email FROM students WHERE id = ?;",
        (student_id,)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Student not found.")
    current = row_to_student(row)

    # Patch fields
    new_name  = payload.name  if payload.name  is not None else current.name
    new_email = payload.email if payload.email is not None else current.email

    # Check email uniqueness if changed
    if new_email != current.email:
        email_exists = conn.execute("SELECT id FROM students WHERE email = ?;", (new_email,)).fetchone()
        if email_exists:
            raise HTTPException(status_code=409, detail="Another student already uses this email.")

    conn.execute(
        "UPDATE students SET name = ?, email = ? WHERE id = ?;",
        (new_name, new_email, student_id)
    )
    conn.commit()

    return StudentOut(id=student_id, name=new_name, email=new_email)

@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int):
    cur = conn.execute("DELETE FROM students WHERE id = ?;", (student_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found.")
    return
