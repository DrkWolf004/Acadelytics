from flask import g
from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from services.classroom_service import (
    create_classroom,
    delete_classroom,
    get_all_classrooms,
    get_classroom_by_id,
    update_classroom,
)
from validations.classroom_validation import (
    validate_classroom_data,
    validate_classroom_update_data,
)


def create_classroom_controller(request_data: dict):
    current_role = getattr(g, "current_user", {}).get("rol")
    valid, errors = validate_classroom_data(request_data, current_role=current_role)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        classroom = create_classroom(request_data)
        return handle_success(201, "Classroom creada correctamente.", {
            "id": classroom.id,
            "nombre": classroom.nombre,
            "type": classroom.type.value,
            "create_at": classroom.create_at.isoformat(),
            "update_at": classroom.update_at.isoformat(),
        })
    except Exception:
        return handle_error_server(500, "No se pudo crear la classroom.")


def edit_classroom_controller(classroom_id: int, request_data: dict):
    current_role = getattr(g, "current_user", {}).get("rol")
    valid, errors = validate_classroom_update_data(request_data, current_role=current_role)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

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


def get_all_classrooms_controller():
    try:
        classrooms = get_all_classrooms()
        payload = [
            {
                "id": classroom.id,
                "nombre": classroom.nombre,
                "type": classroom.type.value,
                "create_at": classroom.create_at.isoformat(),
                "update_at": classroom.update_at.isoformat(),
            }
            for classroom in classrooms
        ]
        return handle_success(200, "Classrooms obtenidas correctamente.", payload)
    except Exception:
        return handle_error_server(500, "No se pudieron obtener las classrooms.")
