import os
from datetime import datetime, timezone

from flask import g, send_file
from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from models import SessionLocal
from models.class_folder_model import ClassFolderModel
from models.classroom_student_model import ClassroomStudentModel
from models.homework_response_model import HomeworkResponseModel
from services.classroom_service import get_classroom_by_id, is_user_in_classroom
from services.file_service import create_file_from_upload
from services.homework_service import (
    create_homework,
    create_or_update_homework_response,
    delete_homework,
    get_homework_by_id,
    get_homework_response,
    get_homework_responses,
    get_homeworks_by_classroom_id,
    update_homework,
)
from validations.homework_validation import validate_homework_payload, validate_homework_grade


def _serialize_homework(homework, current_user: dict | None = None) -> dict:
    response = get_homework_response(homework.id, current_user["id"]) if current_user and current_user.get("id") is not None else None
    response_count = len(get_homework_responses(homework.id))
    user_role = str(current_user.get("rol", "")).strip().capitalize() if current_user else ""

    if current_user and user_role == "Alumno":
        if response is None:
            student_status = "pending"
        elif response.grade:
            student_status = "qualified"
        else:
            student_status = "received"
    else:
        if response_count > 0:
            student_status = "received"
        else:
            student_status = "pending"

    return {
        "id": homework.id,
        "classroom_id": homework.classroom_id,
        "title": homework.title,
        "description": homework.description,
        "deadline_at": homework.deadline_at.isoformat(),
        "attached_file_id": homework.attached_file_id,
        "created_by_id": homework.created_by_id,
        "create_at": homework.create_at.isoformat(),
        "update_at": homework.update_at.isoformat(),
        "response_count": response_count,
        "student_status": student_status,
        "response": {
            "id": response.id,
            "homework_id": response.homework_id,
            "student_id": response.student_id,
            "explanation": response.explanation,
            "filename": response.filename,
            "grade": response.grade,
            "submitted_at": response.submitted_at.isoformat(),
        } if response else None,
    }


def _ensure_classroom_access(classroom_id: int, current_user: dict | None) -> tuple[bool, str | None]:
    if current_user is None:
        return False, "Usuario no autenticado."

    user_id = current_user.get("id")
    role = str(current_user.get("rol", "")).strip().capitalize()
    if role == "Admin":
        return True, None
    if user_id is None:
        return False, "Usuario no autenticado."
    if role == "Profesor":
        return is_user_in_classroom(classroom_id, user_id), None
    if role == "Alumno":
        return is_user_in_classroom(classroom_id, user_id), None
    return False, "Rol no autorizado."


def create_homework_controller(request_data: dict, file_obj=None):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    role = str(current_user.get("rol", "")).strip().capitalize()
    if role != "Profesor":
        return handle_error_client(403, "Solo los profesores pueden publicar tareas.")

    classroom_id = request_data.get("classroom_id")
    classroom = get_classroom_by_id(int(classroom_id)) if classroom_id is not None else None
    if classroom is None:
        return handle_error_client(404, "Classroom no encontrado.")

    allowed, error_message = _ensure_classroom_access(classroom.id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a este classroom.")

    valid, errors = validate_homework_payload(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    attached_file_id = None
    if file_obj is not None and getattr(file_obj, "filename", None):
        session = SessionLocal()
        try:
            class_folder = session.query(ClassFolderModel).filter(ClassFolderModel.classroom_id == classroom.id).first()
            if class_folder is None:
                raise ValueError("Esta classroom no tiene carpeta asociada.")
            created_file = create_file_from_upload(class_folder.id, file_obj, uploaded_by_id=current_user.get("id"))
            attached_file_id = created_file.id
        except Exception as error:
            return handle_error_client(400, "No se pudo adjuntar el archivo de la tarea.", {"file": str(error)})
        finally:
            session.close()

    try:
        homework = create_homework(request_data, created_by_id=current_user.get("id"), attached_file_id=attached_file_id)
        return handle_success(201, "Tarea creada correctamente.", _serialize_homework(homework, current_user))
    except Exception as error:
        return handle_error_server(500, f"No se pudo crear la tarea: {error}")


def get_homeworks_controller(classroom_id: int | None = None):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    if classroom_id is None:
        return handle_error_client(400, "Debes indicar el classroom.")

    classroom = get_classroom_by_id(classroom_id)
    if classroom is None:
        return handle_error_client(404, "Classroom no encontrado.")

    allowed, error_message = _ensure_classroom_access(classroom.id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a este classroom.")

    try:
        homeworks = get_homeworks_by_classroom_id(classroom_id)
        payload = [_serialize_homework(homework, current_user) for homework in homeworks]
        return handle_success(200, "Tareas obtenidas correctamente.", payload)
    except Exception as error:
        return handle_error_server(500, f"No se pudieron obtener las tareas: {error}")


def get_homework_by_id_controller(homework_id: int):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")

    allowed, error_message = _ensure_classroom_access(homework.classroom_id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a esta tarea.")

    return handle_success(200, "Tarea obtenida correctamente.", _serialize_homework(homework, current_user))


def update_homework_controller(homework_id: int, request_data: dict, file_obj=None):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    role = str(current_user.get("rol", "")).strip().capitalize()
    if role != "Profesor":
        return handle_error_client(403, "Solo los profesores pueden modificar tareas.")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")

    allowed, error_message = _ensure_classroom_access(homework.classroom_id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a esta tarea.")

    if request_data:
        valid, errors = validate_homework_payload({**request_data, "classroom_id": homework.classroom_id})
        if not valid:
            return handle_error_client(400, "Validación fallida.", errors)

    attached_file_id = None
    if file_obj is not None and getattr(file_obj, "filename", None):
        session = SessionLocal()
        try:
            class_folder = session.query(ClassFolderModel).filter(ClassFolderModel.classroom_id == homework.classroom_id).first()
            if class_folder is None:
                raise ValueError("Esta classroom no tiene carpeta asociada.")
            created_file = create_file_from_upload(class_folder.id, file_obj, uploaded_by_id=current_user.get("id"))
            attached_file_id = created_file.id
        except Exception as error:
            return handle_error_client(400, "No se pudo adjuntar el archivo de la tarea.", {"file": str(error)})
        finally:
            session.close()

    try:
        updated = update_homework(homework_id, request_data, attached_file_id=attached_file_id)
        if updated is None:
            return handle_error_client(404, "Tarea no encontrada.")
        return handle_success(200, "Tarea actualizada correctamente.", _serialize_homework(updated, current_user))
    except Exception as error:
        return handle_error_server(500, f"No se pudo actualizar la tarea: {error}")


def delete_homework_controller(homework_id: int):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    role = str(current_user.get("rol", "")).strip().capitalize()
    if role != "Profesor":
        return handle_error_client(403, "Solo los profesores pueden eliminar tareas.")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")

    allowed, error_message = _ensure_classroom_access(homework.classroom_id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a esta tarea.")

    try:
        deleted = delete_homework(homework_id)
        if not deleted:
            return handle_error_client(404, "Tarea no encontrada.")
        return handle_success(200, "Tarea eliminada correctamente.")
    except Exception as error:
        return handle_error_server(500, f"No se pudo eliminar la tarea: {error}")


def submit_homework_response_controller(homework_id: int, request_data: dict, file_obj=None):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    role = str(current_user.get("rol", "")).strip().capitalize()
    if role != "Alumno":
        return handle_error_client(403, "Solo los alumnos pueden responder tareas.")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")


    deadline = homework.deadline_at
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    if deadline <= now:
        return handle_error_client(400, "La fecha límite para responder ya ha pasado.")

    allowed, error_message = _ensure_classroom_access(homework.classroom_id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a esta tarea.")

    if not request_data.get("explanation") and file_obj is None:
        return handle_error_client(400, "Debes enviar una explicación o un archivo de respuesta.")

    try:
        response = create_or_update_homework_response(homework_id, current_user.get("id"), request_data, file_obj=file_obj)
        return handle_success(201, "Respuesta enviada correctamente.", {
            "id": response.id,
            "homework_id": response.homework_id,
            "student_id": response.student_id,
            "explanation": response.explanation,
            "filename": response.filename,
            "grade": response.grade,
            "submitted_at": response.submitted_at.isoformat(),
        })
    except Exception as error:
        return handle_error_server(500, f"No se pudo guardar la respuesta: {error}")


def get_homework_responses_controller(homework_id: int):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    role = str(current_user.get("rol", "")).strip().capitalize()
    if role != "Profesor":
        return handle_error_client(403, "Solo los profesores pueden ver las respuestas.")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")

    allowed, error_message = _ensure_classroom_access(homework.classroom_id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a esta tarea.")

    try:
        from services.classroom_service import get_classroom_members
        members = get_classroom_members(homework.classroom_id)
        responses = get_homework_responses(homework_id)
        response_by_student = {r.student_id: r for r in responses}

        payload = []
        for member in members:
            if member.rol.value == "Profesor":
                continue
            response = response_by_student.get(member.id)

            is_submitted = response is not None and (response.explanation or response.filepath)
            payload.append({
                "student_id": member.id,
                "student_name": f"{member.nombre} {member.apellido}",
                "student_email": member.correo,
                "submitted": is_submitted,
                "grade": response.grade if response else None,
                "response_id": response.id if response else None,
                "explanation": response.explanation if response else None,
                "filename": response.filename if response else None,
                "submitted_at": response.submitted_at.isoformat() if response else None,
            })
        return handle_success(200, "Respuestas obtenidas correctamente.", payload)
    except Exception as error:
        return handle_error_server(500, f"No se pudieron obtener las respuestas: {error}")


def grade_homework_response_controller(homework_id: int, response_id: int, request_data: dict):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    role = str(current_user.get("rol", "")).strip().capitalize()
    if role != "Profesor":
        return handle_error_client(403, "Solo los profesores pueden calificar.")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")

    allowed, error_message = _ensure_classroom_access(homework.classroom_id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a esta tarea.")

    grade_value = request_data.get("grade")
    if grade_value in (None, ""):
        return handle_error_client(400, "Debes indicar una nota.")

    valid_grade, grade_error = validate_homework_grade(grade_value)
    if not valid_grade:
        return handle_error_client(400, grade_error)

    try:
        from services.homework_service import grade_homework_response
        response = grade_homework_response(response_id, grade_value)
        if response is None:
            return handle_error_client(404, "Respuesta no encontrada.")
        return handle_success(200, "Tarea calificada correctamente.", {
            "id": response.id,
            "homework_id": response.homework_id,
            "student_id": response.student_id,
            "grade": response.grade,
        })
    except Exception as error:
        return handle_error_server(500, f"No se pudo calificar: {error}")


def auto_grade_missing_responses_controller(homework_id: int):
    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    role = str(current_user.get("rol", "")).strip().capitalize()
    if role != "Profesor":
        return handle_error_client(403, "Solo los profesores pueden realizar esta acción.")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")

    allowed, error_message = _ensure_classroom_access(homework.classroom_id, current_user)
    if not allowed:
        return handle_error_client(403, error_message or "No tienes acceso a esta tarea.")


    deadline = homework.deadline_at
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    if deadline > now:
        return handle_error_client(400, "Solo se puede calificar automáticamente después del plazo.")

    try:
        from services.homework_service import auto_grade_missing_responses
        count = auto_grade_missing_responses(homework_id)
        return handle_success(200, f"{count} respuestas calificadas automáticamente con nota 1.")
    except Exception as error:
        return handle_error_server(500, f"No se pudo calificar automáticamente: {error}")


def download_homework_attachment_controller(homework_id: int):
    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")

    if homework.attached_file_id is None:
        return handle_error_client(404, "Esta tarea no tiene archivo adjunto.")

    from services.file_service import get_file_by_id
    file_record = get_file_by_id(homework.attached_file_id)
    if file_record is None or not os.path.exists(file_record.filepath):
        return handle_error_client(404, "No se encontró el archivo adjunto.")

    return send_file(file_record.filepath, as_attachment=True, download_name=file_record.filename)


def download_homework_response_file_controller(homework_id: int, response_id: int):
    from services.homework_service import get_homework_response as get_response_by_id

    current_user = getattr(g, "current_user", None)
    if not current_user:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso")

    homework = get_homework_by_id(homework_id)
    if homework is None:
        return handle_error_client(404, "Tarea no encontrada.")


    session = SessionLocal()
    try:
        response_record = session.query(HomeworkResponseModel).filter(
            HomeworkResponseModel.id == response_id,
            HomeworkResponseModel.homework_id == homework_id
        ).first()

        if response_record is None:
            return handle_error_client(404, "Respuesta no encontrada.")


        filepath = response_record.filepath
        filename = response_record.filename
        student_id = response_record.student_id
    finally:
        session.close()

    if not filepath or filepath.strip() == "":
        return handle_error_client(404, "Esta respuesta no tiene archivo adjunto.")

    if not os.path.exists(filepath):
        return handle_error_client(404, "El archivo de respuesta no está disponible.")


    user_id = current_user.get("id")
    role = str(current_user.get("rol", "")).strip().capitalize()

    if role == "Profesor":
        if homework.created_by_id != user_id:
            return handle_error_client(403, "No tienes acceso a esta respuesta.")
    elif role == "Alumno":
        if student_id != user_id:
            return handle_error_client(403, "No tienes acceso a esta respuesta.")
    else:
        return handle_error_client(403, "No tienes permiso para acceder a este recurso")

    return send_file(filepath, as_attachment=True, download_name=filename or f"respuesta_{response_id}")


