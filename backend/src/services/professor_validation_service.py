import os
import uuid
from datetime import datetime

from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from models import SessionLocal
from models.professor_validation_model import ProfessorValidationRequestModel, ValidationStatus
from models.user_model import UserModel, UserRole

PROF_VALIDATION_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", "ProfValidation")


def ensure_prof_validation_dir_exists() -> str:
    os.makedirs(PROF_VALIDATION_DIR, exist_ok=True)
    return PROF_VALIDATION_DIR


def normalize_validation_comment(comment: str | None) -> str:
    if comment is None:
        return "No es un documento valido"
    normalized = comment.strip()
    return normalized or "No es un documento valido"


def save_professor_validation_file(file_obj, user_id: int) -> tuple[str, str]:
    if not hasattr(file_obj, "filename") or not file_obj.filename:
        raise ValueError("No se proporcionó ningún archivo.")

    original_filename = secure_filename(file_obj.filename)
    if not original_filename:
        raise ValueError("Nombre de archivo inválido.")

    ensure_prof_validation_dir_exists()
    name_parts = os.path.splitext(original_filename)
    secure_name = f"{user_id}_{uuid.uuid4().hex}{name_parts[1]}"
    filepath = os.path.join(PROF_VALIDATION_DIR, secure_name)
    file_obj.save(filepath)
    return original_filename, filepath


def create_professor_validation_request(user_id: int, file_obj, requested_role: str = "Profesor") -> ProfessorValidationRequestModel:
    session = SessionLocal()
    try:
        user = session.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            raise ValueError("Usuario no encontrado.")

        pending_request = session.query(ProfessorValidationRequestModel).filter(
            ProfessorValidationRequestModel.user_id == user_id,
            ProfessorValidationRequestModel.status == ValidationStatus.PENDIENTE,
        ).first()
        if pending_request is not None:
            raise ValueError("Ya existe una solicitud pendiente para este usuario.")

        filename, filepath = save_professor_validation_file(file_obj, user_id)
        request = ProfessorValidationRequestModel(
            user_id=user_id,
            requested_role=requested_role,
            filename=filename,
            secure_name=os.path.basename(filepath),
            filepath=filepath,
        )
        session.add(request)
        session.commit()
        session.refresh(request)
        request = (
            session.query(ProfessorValidationRequestModel)
            .options(joinedload(ProfessorValidationRequestModel.user))
            .filter(ProfessorValidationRequestModel.id == request.id)
            .first()
        )
        return request
    finally:
        session.close()


def get_professor_validation_request_by_id(request_id: int) -> ProfessorValidationRequestModel | None:
    session = SessionLocal()
    try:
        return (
            session.query(ProfessorValidationRequestModel)
            .options(joinedload(ProfessorValidationRequestModel.user))
            .filter(ProfessorValidationRequestModel.id == request_id)
            .first()
        )
    finally:
        session.close()


def get_professor_validation_requests(status: str | None = None, user_id: int | None = None) -> list[ProfessorValidationRequestModel]:
    session = SessionLocal()
    try:
        query = session.query(ProfessorValidationRequestModel).options(joinedload(ProfessorValidationRequestModel.user))
        if status:
            query = query.filter(ProfessorValidationRequestModel.status == status)
        if user_id is not None:
            query = query.filter(ProfessorValidationRequestModel.user_id == user_id)
        return query.order_by(ProfessorValidationRequestModel.create_at.desc()).all()
    finally:
        session.close()


def review_professor_validation_request(request_id: int, status: str, comment: str | None = None) -> ProfessorValidationRequestModel | None:
    session = SessionLocal()
    try:
        request = (
            session.query(ProfessorValidationRequestModel)
            .options(joinedload(ProfessorValidationRequestModel.user))
            .filter(ProfessorValidationRequestModel.id == request_id)
            .first()
        )
        if request is None:
            return None

        request.status = status
        request.review_comment = normalize_validation_comment(comment) if status == ValidationStatus.RECHAZADA else None
        request.reviewed_at = datetime.utcnow()
        if status == ValidationStatus.ACEPTADA:
            user = session.query(UserModel).filter(UserModel.id == request.user_id).first()
            if user is not None:
                user.rol = UserRole.Profesor
                user.role_changes_remaining = max(0, user.role_changes_remaining)
        session.commit()
        session.refresh(request)
        return request
    finally:
        session.close()


def delete_professor_validation_request(request_id: int) -> bool:
    session = SessionLocal()
    try:
        request = session.query(ProfessorValidationRequestModel).filter(ProfessorValidationRequestModel.id == request_id).first()
        if request is None:
            return False
        if os.path.exists(request.filepath):
            os.remove(request.filepath)
        session.delete(request)
        session.commit()
        return True
    finally:
        session.close()
