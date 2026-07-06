from sqlalchemy.exc import IntegrityError

from models import SessionLocal
from models.professor_validation_model import ProfessorValidationRequestModel
from models.user_model import UserModel, UserRole


def create_user(payload: dict) -> UserModel:
    session = SessionLocal()
    try:
        new_user = UserModel(
            nombre=payload["nombre"].strip(),
            apellido=payload["apellido"].strip(),
            correo=payload["correo"].strip().lower(),
            rol=UserRole(payload.get("rol", "Alumno")),
            role_changes_remaining=payload.get("role_changes_remaining", 3),
        )
        new_user.set_password(payload["password"])

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        session.rollback()
        raise ValueError("Ya existe un usuario con ese correo electrónico.")
    finally:
        session.close()


def get_user_by_id(user_id: int) -> UserModel | None:
    session = SessionLocal()
    try:
        return session.query(UserModel).filter(UserModel.id == user_id).first()
    finally:
        session.close()


def get_user_by_email(correo: str) -> UserModel | None:
    session = SessionLocal()
    try:
        return session.query(UserModel).filter(UserModel.correo == correo.strip().lower()).first()
    finally:
        session.close()


def get_all_users() -> list[UserModel]:
    session = SessionLocal()
    try:
        return session.query(UserModel).order_by(UserModel.id).all()
    finally:
        session.close()


def update_user(user_id: int, payload: dict) -> UserModel | None:
    session = SessionLocal()
    try:
        user = session.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            return None

        if "nombre" in payload:
            user.nombre = payload["nombre"].strip()
        if "apellido" in payload:
            user.apellido = payload["apellido"].strip()
        if "correo" in payload:
            user.correo = payload["correo"].strip().lower()
        if "rol" in payload:
            user.rol = UserRole(payload["rol"])
        if "role_changes_remaining" in payload:
            user.role_changes_remaining = payload["role_changes_remaining"]
        if payload.get("newPassword"):
            user.set_password(payload["newPassword"])
        elif payload.get("password"):
            user.set_password(payload["password"])

        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise ValueError("Ya existe un usuario con ese correo electrónico.")
    finally:
        session.close()


def delete_user(user_id: int) -> bool:
    session = SessionLocal()
    try:
        user = session.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            return False

        session.query(ProfessorValidationRequestModel).filter(
            ProfessorValidationRequestModel.user_id == user_id
        ).delete(synchronize_session=False)
        session.delete(user)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        raise ValueError("No se pudo eliminar el usuario porque tiene datos asociados.")
    finally:
        session.close()


def authenticate_user(correo: str, password: str) -> UserModel | None:
    user = get_user_by_email(correo)
    if user is None:
        return None
    return user if user.verify_password(password) else None
