from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from . import Base


class ClassFolderModel(Base):
    __tablename__ = "class_folders"

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False, index=True)
    create_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    classroom = relationship("ClassroomModel", back_populates="class_folders")
    files = relationship(
        "FileModel",
        back_populates="class_folder",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<ClassFolderModel id={self.id} classroom_id={self.classroom_id}>"
