"""
Database connection
"""
import os


from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from alembic.config import Config
from alembic import command


# REVIEW: this is fine for now but would rather do lru cache
load_dotenv(".env")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db(db_engine=engine):
    Base.metadata.create_all(db_engine)

    # then, load the Alembic configuration and generate the
    # version table, "stamping" it with the most recent rev:
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")


def get_db():
    """Yeilds databse session then closes session when done"""
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
