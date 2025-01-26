<<<<<<< HEAD
# connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHAMY_DATABASE_URL = "postgresql://postgres:mahi-h82@localhost:5432/DRYAR1"

engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
=======
# connection
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

SQLALCHAMY_DATABASE_URL = "postgresql+asyncpg://postgres:mahi-h82@localhost/DrYar"


engine = create_async_engine(SQLALCHAMY_DATABASE_URL,echo=0)

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase, MappedAsDataclass):
    pass


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
>>>>>>> c654aed5cb4e471277e496815c6912edc203b038
