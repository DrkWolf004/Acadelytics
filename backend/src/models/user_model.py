import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from . import Base


class UserRole(enum.Enum):
    Alumno = "Alumno"
    Profesor = "Profesor"
    Admin = "Admin"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    rol = Column(Enum(UserRole), nullable=False, default=UserRole.Alumno)
    create_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<UserModel id={self.id} correo={self.correo} rol={self.rol.value}>"

    def set_password(self, raw_password: str) -> None:
        
        self.password = generate_password_hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        
        return check_password_hash(self.password, raw_password)
