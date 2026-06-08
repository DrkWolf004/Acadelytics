from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from . import Base


class ClassroomStudentModel(Base):
    __tablename__ = "classroom_students"

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    classroom = relationship("ClassroomModel", back_populates="student_links")
    student = relationship("UserModel", back_populates="classroom_links")

    def __repr__(self) -> str:
        return f"<ClassroomStudentModel id={self.id} classroom_id={self.classroom_id} student_id={self.student_id}>"
