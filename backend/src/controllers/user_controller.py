from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from services.auth_service import create_access_token
from services.user_service import (
    authenticate_user,
    create_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    update_user,
)
from validations.user_validation import (
    validate_admin_create_data,
    validate_login_data,
    validate_register_data,
    validate_update_data,
    validate_query_params,
)


def _build_user_payload(user):
    return {
        "id": user.id,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "correo": user.correo,
        "rol": user.rol.value,
        "role_changes_remaining": user.role_changes_remaining,
        "create_at": user.create_at.isoformat(),
        "update_at": user.update_at.isoformat(),
    }


def register_user_controller(request_data: dict):
    valid, errors = validate_register_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        user = create_user(request_data)
        token = create_access_token({
            "id": user.id,
            "correo": user.correo,
            "rol": user.rol.value,
        })
        return handle_success(201, "Usuario registrado correctamente.", {
            "id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "correo": user.correo,
            "rol": user.rol.value,
            "role_changes_remaining": user.role_changes_remaining,
            "token": token,
            "create_at": user.create_at.isoformat(),
            "update_at": user.update_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo registrar el usuario.")


def login_user_controller(request_data: dict):
    valid, errors = validate_login_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        user = authenticate_user(request_data["correo"], request_data["password"])
        if user is None:
            return handle_error_client(401, "Credenciales inválidas.")

        token = create_access_token({
            "id": user.id,
            "correo": user.correo,
            "rol": user.rol.value,
        })

        return handle_success(200, "Inicio de sesión exitoso.", {
            "id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "correo": user.correo,
            "rol": user.rol.value,
            "role_changes_remaining": user.role_changes_remaining,
            "token": token,
        })
    except Exception:
        return handle_error_server(500, "No se pudo iniciar sesión.")


def create_user_controller(request_data: dict):
    valid, errors = validate_admin_create_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        user = create_user(request_data)
        return handle_success(201, "Usuario creado correctamente.", _build_user_payload(user))
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo crear el usuario.")


def edit_user_controller(user_id: int, request_data: dict, current_user: dict):
    valid, errors = validate_update_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        target_user = get_user_by_id(user_id)
        if target_user is None:
            return handle_error_client(404, "Usuario no encontrado.")

        if "rol" in request_data and request_data["rol"] != target_user.rol.value:
            if current_user.get("rol") != "Admin":
                if target_user.role_changes_remaining <= 0:
                    return handle_error_client(400, "No quedan cambios de rol disponibles.")
                request_data["role_changes_remaining"] = target_user.role_changes_remaining - 1

        if current_user.get("rol") == "Admin" and "role_changes_remaining" in request_data:
            try:
                new_changes = int(request_data["role_changes_remaining"])
            except (TypeError, ValueError):
                return handle_error_client(400, "Los cambios de rol deben ser un número entero entre 0 y 3.")
            if new_changes < 0 or new_changes > 3:
                return handle_error_client(400, "Los cambios de rol deben ser un número entero entre 0 y 3.")
            request_data["role_changes_remaining"] = new_changes

        user = update_user(user_id, request_data)
        if user is None:
            return handle_error_client(404, "Usuario no encontrado.")

        return handle_success(200, "Usuario actualizado correctamente.", _build_user_payload(user))
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo actualizar el usuario.")


def delete_user_controller(user_id: int):
    try:
        deleted = delete_user(user_id)
        if not deleted:
            return handle_error_client(404, "Usuario no encontrado.")

        return handle_success(200, "Usuario eliminado correctamente.")
    except Exception:
        return handle_error_server(500, "No se pudo eliminar el usuario.")


def get_user_by_id_controller(user_id: int):
    try:
        user = get_user_by_id(user_id)
        if user is None:
            return handle_error_client(404, "Usuario no encontrado.")

        return handle_success(200, "Usuario encontrado.", _build_user_payload(user))
    except Exception:
        return handle_error_server(500, "No se pudo obtener el usuario.")


def get_user_by_email_controller(correo: str):
    try:
        user = get_user_by_email(correo)
        if user is None:
            return handle_error_client(404, "Usuario no encontrado.")

        return handle_success(200, "Usuario encontrado.", _build_user_payload(user))
    except Exception:
        return handle_error_server(500, "No se pudo obtener el usuario.")


def get_all_users_controller(current_user: dict):
    if current_user.get("rol") != "Admin":
        return handle_error_client(403, "Acceso denegado.", {"info": "Solo los administradores pueden listar todos los usuarios."})

    try:
        users = get_all_users()
        payload = [
            _build_user_payload(user)
            for user in users
        ]
        return handle_success(200, "Usuarios obtenidos correctamente.", payload)
    except Exception:
        return handle_error_server(500, "No se pudieron obtener los usuarios.")


def get_user_query_controller(payload: dict):
    valid, errors = validate_query_params(payload)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        if "id" in payload:
            return get_user_by_id_controller(payload["id"])
        if "correo" in payload:
            return get_user_by_email_controller(payload["correo"])
        return handle_error_client(400, "No se proporcionó un parámetro de búsqueda válido.")
    except Exception:
        return handle_error_server(500, "No se pudo obtener el usuario.")
