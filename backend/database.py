"""
Database connection
"""
import os


from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# REVIEW: this is fine for now but would rather do lru cache
load_dotenv('.env')
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yeilds databse session then closes session when done"""
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
