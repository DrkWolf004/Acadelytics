import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from . import Base


class InvitationStatus(enum.Enum):
    pendiente = "pendiente"
    aceptada = "aceptada"
    rechazada = "rechazada"


class ClassroomInvitationModel(Base):
    __tablename__ = "classroom_invitations"

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.pendiente, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    classroom = relationship("ClassroomModel", back_populates="invitations")
    sender = relationship("UserModel", foreign_keys=[sender_id], back_populates="sent_invitations")
    receiver = relationship("UserModel", foreign_keys=[receiver_id], back_populates="received_invitations")

    def __repr__(self) -> str:
        return (
            f"<ClassroomInvitationModel id={self.id} classroom_id={self.classroom_id} "
            f"sender_id={self.sender_id} receiver_id={self.receiver_id} status={self.status.value}>"
        )
