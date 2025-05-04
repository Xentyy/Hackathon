from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")
engine = create_engine(DB_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
