from sqlalchemy.orm import declarative_base

from config.configDb import engine, SessionLocal

Base = declarative_base()

from .user_model import UserModel, UserRole

__all__ = ["Base", "engine", "SessionLocal", "init_db", "UserModel", "UserRole"]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
