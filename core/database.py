import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. Create a .env file or export DATABASE_URL in your environment."
    )

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_user_role_column():
    with engine.begin() as connection:
        dialect_name = connection.dialect.name

        if dialect_name == "postgresql":
            connection.execute(
                text(
                    "ALTER TABLE IF EXISTS users "
                    "ADD COLUMN IF NOT EXISTS role VARCHAR NOT NULL DEFAULT 'seller'"
                )
            )
            return

        if dialect_name == "sqlite":
            table_exists = connection.execute(
                text(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='users'"
                )
            ).first()

            if table_exists is None:
                return

            columns = connection.execute(text("PRAGMA table_info(users)")).fetchall()
            has_role_column = any(column[1] == "role" for column in columns)

            if not has_role_column:
                connection.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN role VARCHAR NOT NULL DEFAULT 'seller'"
                    )
                )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
