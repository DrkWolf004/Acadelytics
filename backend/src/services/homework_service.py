import os
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename

from models import SessionLocal
from models.homework_model import HomeworkModel
from models.homework_response_model import HomeworkResponseModel
from models.class_folder_model import ClassFolderModel
from models.classroom_student_model import ClassroomStudentModel


UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", "homework"))


def ensure_homework_uploads_dir(homework_id: int, student_id: int) -> str:
    folder_path = os.path.abspath(os.path.join(UPLOADS_DIR, str(homework_id), str(student_id)))
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_homework_response_file(file_obj, homework_id: int, student_id: int) -> tuple[str, str]:
    if not hasattr(file_obj, "filename"):
        raise ValueError("Invalid file object")

    original_filename = secure_filename(file_obj.filename)
    if not original_filename:
        raise ValueError("Invalid filename")

    name_parts = os.path.splitext(original_filename)
    secure_name = f"{uuid.uuid4().hex}_{name_parts[0]}{name_parts[1]}"

    folder_path = ensure_homework_uploads_dir(homework_id, student_id)
    filepath = os.path.abspath(os.path.join(folder_path, secure_name))
    file_obj.save(filepath)


    if not os.path.exists(filepath):
        raise ValueError(f"File was not saved at {filepath}")

    return secure_name, filepath


def create_homework(payload: dict, created_by_id: int | None = None, attached_file_id: int | None = None) -> HomeworkModel:
    session = SessionLocal()
    try:
        homework = HomeworkModel(
            classroom_id=int(payload["classroom_id"]),
            created_by_id=created_by_id,
            title=str(payload["title"]).strip(),
            description=str(payload.get("description") or "").strip(),
            deadline_at=datetime.fromisoformat(str(payload["deadline_at"]).replace("Z", "+00:00")),
            attached_file_id=attached_file_id,
        )
        session.add(homework)
        session.commit()
        session.refresh(homework)
        return homework
    finally:
        session.close()


def get_homeworks_by_classroom_id(classroom_id: int) -> list[HomeworkModel]:
    session = SessionLocal()
    try:
        return (
            session.query(HomeworkModel)
            .filter(HomeworkModel.classroom_id == classroom_id)
            .order_by(HomeworkModel.deadline_at.asc(), HomeworkModel.id.asc())
            .all()
        )
    finally:
        session.close()


def get_homework_by_id(homework_id: int) -> HomeworkModel | None:
    session = SessionLocal()
    try:
        return session.query(HomeworkModel).filter(HomeworkModel.id == homework_id).first()
    finally:
        session.close()


def update_homework(homework_id: int, payload: dict, attached_file_id: int | None = None) -> HomeworkModel | None:
    session = SessionLocal()
    try:
        homework = session.query(HomeworkModel).filter(HomeworkModel.id == homework_id).first()
        if homework is None:
            return None

        if "title" in payload:
            homework.title = str(payload["title"]).strip()
        if "description" in payload:
            homework.description = str(payload.get("description") or "").strip()
        if "deadline_at" in payload and payload.get("deadline_at"):
            homework.deadline_at = datetime.fromisoformat(str(payload["deadline_at"]).replace("Z", "+00:00"))
        if attached_file_id is not None:
            homework.attached_file_id = attached_file_id

        session.commit()
        session.refresh(homework)
        return homework
    finally:
        session.close()


def delete_homework(homework_id: int) -> bool:
    session = SessionLocal()
    try:
        homework = session.query(HomeworkModel).filter(HomeworkModel.id == homework_id).first()
        if homework is None:
            return False
        session.delete(homework)
        session.commit()
        return True
    finally:
        session.close()


def create_or_update_homework_response(homework_id: int, student_id: int, payload: dict, file_obj=None) -> HomeworkResponseModel:
    session = SessionLocal()
    try:
        response = session.query(HomeworkResponseModel).filter(
            HomeworkResponseModel.homework_id == homework_id,
            HomeworkResponseModel.student_id == student_id,
        ).first()

        if response is None:
            response = HomeworkResponseModel(homework_id=homework_id, student_id=student_id, submitted_at=datetime.utcnow())
            session.add(response)

        if file_obj is not None:
            if response.filepath and os.path.exists(response.filepath):
                try:
                    os.remove(response.filepath)
                except OSError:
                    pass
            secure_name, filepath = save_homework_response_file(file_obj, homework_id, student_id)
            response.filename = file_obj.filename
            response.secure_name = secure_name
            response.filepath = filepath

        response.explanation = payload.get("explanation") and str(payload.get("explanation")).strip() or None
        response.submitted_at = datetime.utcnow()
        session.commit()
        session.refresh(response)
        return response
    finally:
        session.close()


def get_homework_response(homework_id: int, student_id: int) -> HomeworkResponseModel | None:
    session = SessionLocal()
    try:
        return (
            session.query(HomeworkResponseModel)
            .filter(
                HomeworkResponseModel.homework_id == homework_id,
                HomeworkResponseModel.student_id == student_id,
            )
            .first()
        )
    finally:
        session.close()


def get_homework_responses(homework_id: int) -> list[HomeworkResponseModel]:
    session = SessionLocal()
    try:
        return (
            session.query(HomeworkResponseModel)
            .filter(HomeworkResponseModel.homework_id == homework_id)
            .order_by(HomeworkResponseModel.submitted_at.asc())
            .all()
        )
    finally:
        session.close()


def grade_homework_response(response_id: int, grade: str) -> HomeworkResponseModel | None:
    session = SessionLocal()
    try:
        response = session.query(HomeworkResponseModel).filter(HomeworkResponseModel.id == response_id).first()
        if response is None:
            return None
        response.grade = str(grade).strip()
        session.commit()
        session.refresh(response)
        return response
    finally:
        session.close()


def auto_grade_missing_responses(homework_id: int) -> int:
    session = SessionLocal()
    try:
        homework = session.query(HomeworkModel).filter(HomeworkModel.id == homework_id).first()
        if homework is None:
            return 0

        from models.classroom_student_model import ClassroomStudentModel
        from models.user_model import UserModel

        members = (
            session.query(UserModel)
            .join(ClassroomStudentModel, ClassroomStudentModel.student_id == UserModel.id)
            .filter(
                ClassroomStudentModel.classroom_id == homework.classroom_id,
                UserModel.rol.astext != "Profesor",
            )
            .all()
        )

        responses_by_student = {r.student_id: r for r in session.query(HomeworkResponseModel).filter(
            HomeworkResponseModel.homework_id == homework_id
        ).all()}

        graded_count = 0
        for member in members:
            if member.id not in responses_by_student:
                new_response = HomeworkResponseModel(
                    homework_id=homework_id,
                    student_id=member.id,
                    grade="1",
                )
                session.add(new_response)
                graded_count += 1
            else:
                response = responses_by_student[member.id]
                if not response.grade:
                    response.grade = "1"
                    graded_count += 1

        session.commit()
        return graded_count
    finally:
        session.close()
