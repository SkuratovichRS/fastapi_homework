import uuid
from datetime import datetime

from sqlalchemy import (UUID, Boolean, CheckConstraint, Column, DateTime,
                        ForeignKey, Integer, String, Table, UniqueConstraint,
                        func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import BaseModel
from app.users.models import User


class Token(BaseModel):
    __tablename__ = "tokens"

    token: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", backref="tokens")


class Role(BaseModel):
    __tablename__ = "roles"
    ROLES = ["admin", "user"]

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    rights = relationship("Right", secondary="role_right", backref="roles")

    __table_args__ = (CheckConstraint(name.in_(ROLES), name="valid_role_name"),)


class Right(BaseModel):
    __tablename__ = "rights"

    write: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    only_owner: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)

    __table_args__ = (UniqueConstraint("write", "read", "only_owner", "model", name="unique_right_combination"),)


user_role = Table(
    "user_role",
    BaseModel.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

role_right = Table(
    "role_right",
    BaseModel.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("right_id", Integer, ForeignKey("rights.id")),
)
