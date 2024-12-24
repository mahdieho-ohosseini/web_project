# models of db
from sqlalchemy.orm import Mapped, mapped_column
from .engine import Base


class User(Base):
    __tablename__ = "users"

    password: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
