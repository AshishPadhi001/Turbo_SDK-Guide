# main.py
import uvicorn
from fastapi import FastAPI
from app.db import init_tables
from app.routers.books import router as books_router
from app.routers.students import router as students_router

app = FastAPI(title="Turso FastAPI Book System", version="0.1.0")

# Auto-create tables on startup
@app.on_event("startup")
def startup():
    init_tables()

# Routers
app.include_router(books_router)
app.include_router(students_router)

@app.get("/")
def root():
    return {"ok": True, "msg": "Turso FastAPI Book System (CRUD only)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007, reload=True)
