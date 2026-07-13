from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from . import Base


class HomeworkResponseModel(Base):
    __tablename__ = "homework_responses"

    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer, ForeignKey("homeworks.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=True)
    secure_name = Column(String(255), nullable=True)
    filepath = Column(String(1024), nullable=True)
    explanation = Column(Text, nullable=True)
    grade = Column(String(10), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    homework = relationship("HomeworkModel", back_populates="responses")
    student = relationship("UserModel")

    def __repr__(self) -> str:
        return f"<HomeworkResponseModel id={self.id} homework_id={self.homework_id}>"
