from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    roles = relationship("Role", secondary="user_role", backref="users")
