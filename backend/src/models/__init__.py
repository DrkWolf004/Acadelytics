from sqlalchemy.orm import declarative_base

from config.configDb import engine, SessionLocal

Base = declarative_base()

from .user_model import UserModel, UserRole
from .classroom_model import ClassroomModel, ClassroomType
from .class_folder_model import ClassFolderModel
from .file_model import FileModel
from .classroom_student_model import ClassroomStudentModel
from .classroom_invitation_model import ClassroomInvitationModel, InvitationStatus

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "init_db",
    "UserModel",
    "UserRole",
    "ClassroomModel",
    "ClassroomType",
    "ClassFolderModel",
    "FileModel",
    "ClassroomStudentModel",
    "ClassroomInvitationModel",
    "InvitationStatus",
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
