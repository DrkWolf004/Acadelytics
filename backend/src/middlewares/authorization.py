from functools import wraps

from flask import g

from handlers.response_handlers import handle_error_client


def _normalize_role(value):
    if value is None:
        return ""
    return str(value).strip().capitalize()


def _require_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if user is None:
                return handle_error_client(
                    401,
                    "No tienes permiso para acceder a este recurso",
                    {"info": "Usuario no autenticado."},
                )

            rol = _normalize_role(user.get("rol"))
            if rol != required_role:
                return handle_error_client(
                    403,
                    "Error al acceder al recurso",
                    {"info": f"Se requiere un rol de {required_role}."},
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_admin(func):
    return _require_role("Admin")(func)


def is_profesor(func):
    return _require_role("Profesor")(func)


def is_profesor_or_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getattr(g, "current_user", None)
        if user is None:
            return handle_error_client(
                401,
                "No tienes permiso para acceder a este recurso",
                {"info": "Usuario no autenticado."},
            )

        rol = _normalize_role(user.get("rol"))
        if rol not in ("Profesor", "Admin"):
            return handle_error_client(
                403,
                "Error al acceder al recurso",
                {"info": "Se requiere un rol de Profesor o Admin."},
            )

        return func(*args, **kwargs)

    return wrapper


def is_alumno(func):
    return _require_role("Alumno")(func)
