# Pydantic models
# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -------- Books --------
class BookCreate(BaseModel):
    id: int = Field(..., ge=1)
    title: str
    author: str
    year: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None

# -------- Students --------
class StudentCreate(BaseModel):
    id: int = Field(..., ge=1)
    name: str
    email: EmailStr

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
