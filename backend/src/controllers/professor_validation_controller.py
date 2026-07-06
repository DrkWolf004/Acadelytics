import os
from flask import g, send_file

from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from services.professor_validation_service import (
    create_professor_validation_request,
    delete_professor_validation_request,
    get_professor_validation_request_by_id,
    get_professor_validation_requests,
    review_professor_validation_request,
)
from models.professor_validation_model import ValidationStatus


def _serialize_request(request) -> dict:
    return {
        "id": request.id,
        "user_id": request.user_id,
        "requested_role": request.requested_role,
        "status": request.status,
        "filename": request.filename,
        "secure_name": request.secure_name,
        "filepath": request.filepath,
        "review_comment": request.review_comment,
        "create_at": request.create_at.isoformat() if request.create_at else None,
        "reviewed_at": request.reviewed_at.isoformat() if request.reviewed_at else None,
        "user": {
            "id": request.user.id,
            "nombre": request.user.nombre,
            "apellido": request.user.apellido,
            "correo": request.user.correo,
            "rol": request.user.rol.value,
        } if request.user else None,
    }


def create_professor_validation_request_controller(file_obj, current_user: dict):
    try:
        if not current_user:
            return handle_error_client(401, "No autorizado.")
        request = create_professor_validation_request(current_user["id"], file_obj)
        return handle_success(201, "Solicitud de validación enviada correctamente.", _serialize_request(request))
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception as error:
        return handle_error_server(500, f"No se pudo crear la solicitud. {str(error)}")


def list_professor_validation_requests_controller(current_user: dict, status: str | None = None):
    try:
        if current_user.get("rol") == "Admin":
            requests = get_professor_validation_requests(status=status)
        else:
            requests = get_professor_validation_requests(status=status, user_id=current_user.get("id"))
        return handle_success(200, "Solicitudes obtenidas correctamente.", [_serialize_request(item) for item in requests])
    except Exception:
        return handle_error_server(500, "No se pudieron obtener las solicitudes.")


def review_professor_validation_request_controller(request_id: int, payload: dict, current_user: dict):
    if current_user.get("rol") != "Admin":
        return handle_error_client(403, "Acceso denegado.", {"info": "Solo los administradores pueden revisar solicitudes."})

    status = payload.get("status")
    if status not in {ValidationStatus.ACEPTADA, ValidationStatus.RECHAZADA}:
        return handle_error_client(400, "El estado debe ser aceptada o rechazada.")

    try:
        request = review_professor_validation_request(request_id, status, payload.get("comment"))
        if request is None:
            return handle_error_client(404, "Solicitud no encontrada.")
        return handle_success(200, "Solicitud revisada correctamente.", _serialize_request(request))
    except Exception:
        return handle_error_server(500, "No se pudo revisar la solicitud.")


def get_professor_validation_file_controller(request_id: int, current_user: dict):
    try:
        request = get_professor_validation_request_by_id(request_id)
        if request is None:
            return handle_error_client(404, "Solicitud no encontrada.")

        if current_user.get("rol") != "Admin" and request.user_id != current_user.get("id"):
            return handle_error_client(403, "Acceso denegado.", {"info": "Solo los administradores o el propietario pueden ver el archivo de la solicitud."})

        if not os.path.exists(request.filepath):
            return handle_error_client(404, "El archivo no existe.")
        return send_file(request.filepath, as_attachment=False)
    except Exception:
        return handle_error_server(500, "No se pudo obtener el archivo.")


def get_professor_validation_request_controller(request_id: int, current_user: dict):
    try:
        request = get_professor_validation_request_by_id(request_id)
        if request is None:
            return handle_error_client(404, "Solicitud no encontrada.")

        if current_user.get("rol") != "Admin" and request.user_id != current_user.get("id"):
            return handle_error_client(403, "Acceso denegado.", {"info": "Solo los administradores o el propietario pueden ver la solicitud."})

        return handle_success(200, "Solicitud encontrada.", _serialize_request(request))
    except Exception:
        return handle_error_server(500, "No se pudo obtener la solicitud.")


def delete_professor_validation_request_controller(request_id: int, current_user: dict):
    if current_user.get("rol") != "Admin":
        return handle_error_client(403, "Acceso denegado.", {"info": "Solo los administradores pueden eliminar solicitudes."})

    try:
        deleted = delete_professor_validation_request(request_id)
        if not deleted:
            return handle_error_client(404, "Solicitud no encontrada.")
        return handle_success(200, "Solicitud eliminada correctamente.")
    except Exception:
        return handle_error_server(500, "No se pudo eliminar la solicitud.")
