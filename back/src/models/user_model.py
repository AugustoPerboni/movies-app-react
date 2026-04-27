from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint


class User(SQLModel, table=True):
    # Enforce unique email in the database
    __table__arg__ = (
        UniqueConstraint("email", "uq_users_email")
    )

    id: int | None = Field(default=None, primary_key=True)
    
    email: str = Field(
        index=True,
        nullable=False,
        max_length=255
    )
    hashed_password: str = Field(
        nullable=False,
        max_length=255
    )

    is_active : bool = Field(
        default=True,
        nullable=False
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )