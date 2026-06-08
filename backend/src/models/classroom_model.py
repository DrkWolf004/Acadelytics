from datetime import datetime
import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class ClassroomType(enum.Enum):
    Solitario = "Solitario"
    Grupal = "Grupal"


class ClassroomModel(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    type = Column(Enum(ClassroomType), nullable=False, default=ClassroomType.Solitario)
    create_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    class_folders = relationship(
        "ClassFolderModel",
        back_populates="classroom",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    student_links = relationship(
        "ClassroomStudentModel",
        back_populates="classroom",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    students = relationship(
        "UserModel",
        secondary="classroom_students",
        back_populates="classrooms",
    )
    invitations = relationship(
        "ClassroomInvitationModel",
        back_populates="classroom",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<ClassroomModel id={self.id} nombre={self.nombre} type={self.type.value}>"
