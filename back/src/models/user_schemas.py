from sqlmodel import SQLModel
from datetime import datetime


class UserCreate(SQLModel):
    email: str
    password: str


class UserPublic(SQLModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime