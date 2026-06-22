from flask import g
from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from models import SessionLocal
from models.class_folder_model import ClassFolderModel
from services.classroom_service import (
    create_classroom,
    delete_classroom,
    get_all_classrooms,
    get_classroom_by_id,
    get_classroom_members,
    get_classrooms_with_folder_ids,
    is_user_in_classroom,
    update_classroom,
)
from services.user_service import get_user_by_email
from services.classroom_invitation_service import create_invitation

from validations.classroom_validation import (
    validate_classroom_data,
    validate_classroom_update_data,
)


def create_classroom_controller(request_data: dict):
    current_user = getattr(g, "current_user", {})
    current_role = current_user.get("rol")
    valid, errors = validate_classroom_data(request_data, current_role=current_role)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        classroom = create_classroom(request_data, creator_id=current_user.get("id"))
        
        session = SessionLocal()
        try:
            folder = session.query(ClassFolderModel).filter(
                ClassFolderModel.classroom_id == classroom.id
            ).first()
            folder_id = folder.id if folder else None
        finally:
            session.close()
        
        return handle_success(201, "Classroom creada correctamente.", {
            "id": classroom.id,
            "nombre": classroom.nombre,
            "type": classroom.type.value,
            "class_folder_id": folder_id,
            "create_at": classroom.create_at.isoformat(),
            "update_at": classroom.update_at.isoformat(),
        })
    except Exception as e:
        return handle_error_server(500, "No se pudo crear la classroom.")


def edit_classroom_controller(classroom_id: int, request_data: dict):
    current_user = getattr(g, "current_user", {})
    current_role = current_user.get("rol")
    current_user_id = current_user.get("id")

    valid, errors = validate_classroom_update_data(request_data, current_role=current_role)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    classroom = get_classroom_by_id(classroom_id)
    if classroom is None:
        return handle_error_client(404, "Classroom no encontrada.")

    if current_role == "Admin":
        pass
    elif current_role == "Profesor":
        pass
    elif current_role == "Alumno":
        if classroom.type.value != "Solitario":
            return handle_error_client(403, "No tienes permiso para editar este classroom.")
        if not is_user_in_classroom(classroom_id, current_user_id):
            return handle_error_client(403, "No estás autorizado para editar esta classroom.")
        if "type" in request_data and request_data.get("type") != "Solitario":
            return handle_error_client(403, "No puedes cambiar el tipo de un classroom solitario.")
    else:
        return handle_error_client(403, "No tienes permiso para editar este classroom.")

    try:
        classroom = update_classroom(classroom_id, request_data)
        if classroom is None:
            return handle_error_client(404, "Classroom no encontrada.")

        return handle_success(200, "Classroom actualizada correctamente.", {
            "id": classroom.id,
            "nombre": classroom.nombre,
            "type": classroom.type.value,
            "create_at": classroom.create_at.isoformat(),
            "update_at": classroom.update_at.isoformat(),
        })
    except Exception:
        return handle_error_server(500, "No se pudo actualizar la classroom.")


def delete_classroom_controller(classroom_id: int):
    current_user = getattr(g, "current_user", {})
    current_role = current_user.get("rol")
    current_user_id = current_user.get("id")

    classroom = get_classroom_by_id(classroom_id)
    if classroom is None:
        return handle_error_client(404, "Classroom no encontrada.")

    if current_role == "Admin":
        pass
    elif current_role == "Profesor":
        pass
    elif current_role == "Alumno":
        if classroom.type.value != "Solitario":
            return handle_error_client(403, "No tienes permiso para eliminar este classroom.")
        if not is_user_in_classroom(classroom_id, current_user_id):
            return handle_error_client(403, "No estás autorizado para eliminar esta classroom.")
    else:
        return handle_error_client(403, "No tienes permiso para eliminar este classroom.")

    try:
        deleted = delete_classroom(classroom_id)
        if not deleted:
            return handle_error_client(404, "Classroom no encontrada.")

        return handle_success(200, "Classroom eliminada correctamente.")
    except Exception:
        return handle_error_server(500, "No se pudo eliminar la classroom.")


def get_classroom_by_id_controller(classroom_id: int):
    try:
        classroom = get_classroom_by_id(classroom_id)
        if classroom is None:
            return handle_error_client(404, "Classroom no encontrada.")

        return handle_success(200, "Classroom encontrada.", {
            "id": classroom.id,
            "nombre": classroom.nombre,
            "type": classroom.type.value,
            "create_at": classroom.create_at.isoformat(),
            "update_at": classroom.update_at.isoformat(),
        })
    except Exception:
        return handle_error_server(500, "No se pudo obtener la classroom.")


def get_user_classrooms_controller():
    current_user = getattr(g, "current_user", {})
    user_id = current_user.get("id")
    if user_id is None:
        return handle_error_client(401, "No tienes permiso para acceder a este recurso.", {"info": "Usuario no autenticado."})

    try:
        classrooms = get_classrooms_with_folder_ids(user_id)
        payload = [
            {
                "id": classroom.id,
                "nombre": classroom.nombre,
                "type": classroom.type.value,
                "class_folder_id": folder_id,
                "create_at": classroom.create_at.isoformat(),
                "update_at": classroom.update_at.isoformat(),
            }
            for classroom, folder_id in classrooms
        ]
        return handle_success(200, "Classrooms obtenidas correctamente.", payload)
    except Exception:
        return handle_error_server(500, "No se pudieron obtener las classrooms.")


def get_classroom_members_controller(classroom_id: int):
    current_user = getattr(g, "current_user", {})
    classroom = get_classroom_by_id(classroom_id)
    if classroom is None:
        return handle_error_client(404, "Classroom no encontrada.")

    if current_user.get("rol") != "Admin" and not is_user_in_classroom(classroom_id, current_user.get("id")):
        return handle_error_client(403, "Acceso denegado.", {"info": "Solo los integrantes pueden ver los miembros de esta classroom."})

    try:
        members = get_classroom_members(classroom_id)
        payload = [
            {
                "id": member.id,
                "nombre": member.nombre,
                "apellido": member.apellido,
                "correo": member.correo,
                "rol": member.rol.value,
            }
            for member in members
        ]
        return handle_success(200, "Miembros obtenidos correctamente.", payload)
    except Exception:
        return handle_error_server(500, "No se pudieron obtener los integrantes.")


def add_classroom_member_controller(classroom_id: int, request_data: dict):
    correo = request_data.get("correo")
    if not isinstance(correo, str) or not correo.strip():
        return handle_error_client(400, "Validación fallida.", {"correo": "El correo es obligatorio."})

    classroom = get_classroom_by_id(classroom_id)
    if classroom is None:
        return handle_error_client(404, "Classroom no encontrada.")
    try:
        user = get_user_by_email(correo)
        if user is None:
            return handle_error_client(404, "El usuario especificado no existe.")

        sender_id = getattr(g, "current_user", {}).get("id")
        invitation = create_invitation(sender_id, {"classroom_id": classroom_id, "receiver_id": user.id})
        return handle_success(201, "Invitación enviada correctamente.", {
            "id": invitation.id,
            "classroom_id": invitation.classroom_id,
            "sender_id": invitation.sender_id,
            "receiver_id": invitation.receiver_id,
            "status": invitation.status.value,
            "create_at": invitation.create_at.isoformat(),
            "update_at": invitation.update_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo enviar la invitación al classroom.")
