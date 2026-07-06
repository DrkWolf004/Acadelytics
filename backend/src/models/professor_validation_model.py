from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base


class ValidationStatus:
    PENDIENTE = "pendiente"
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"


class ProfessorValidationRequestModel(Base):
    __tablename__ = "professor_validation_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    requested_role = Column(String(50), nullable=False, default="Profesor")
    status = Column(String(20), nullable=False, default=ValidationStatus.PENDIENTE)
    filename = Column(String(255), nullable=False)
    secure_name = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    review_comment = Column(String(500), nullable=True)
    create_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)

    user = relationship(
        "UserModel",
        backref=backref(
            "professor_validation_requests",
            cascade="all, delete-orphan",
            passive_deletes=True,
        ),
    )

    def __repr__(self) -> str:
        return f"<ProfessorValidationRequestModel id={self.id} user_id={self.user_id} status={self.status}>"
