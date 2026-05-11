import re

ALLOWED_USER_ROLES = {"Alumno", "Profesor", "Admin"}
REGISTER_USER_ROLES = {"Alumno", "Profesor"}
VALID_EMAIL_DOMAINS = ["@gmail.cl", "@gmail.com", "@hotmail.cl", "@hotmail.com", "@acadelytics.com"]
NAME_PATTERN = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$")
PASSWORD_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")


def _validate_email_domain(email: str) -> str | None:
    if not isinstance(email, str) or "@" not in email:
        return "El correo electrónico debe ser una cadena válida."

    lower_email = email.lower()
    if not any(lower_email.endswith(domain) for domain in VALID_EMAIL_DOMAINS):
        return "El correo debe finalizar en @gmail.cl, @gmail.com, @hotmail.cl o @hotmail.com."

    return None


def _validate_name(field: str, value: str, required: bool) -> str | None:
    if value is None:
        return f"El campo {field} es obligatorio." if required else None
    if not isinstance(value, str) or not value.strip():
        return f"El {field} no puede estar vacío."
    if len(value.strip()) < 2:
        return f"El {field} debe tener al menos 2 caracteres."
    if len(value.strip()) > 25:
        return f"El {field} debe tener como máximo 25 caracteres."
    if not NAME_PATTERN.match(value):
        return f"El {field} solo puede contener letras y espacios."
    return None


def _validate_password(field: str, value: str, required: bool) -> str | None:
    if value is None:
        return f"La contraseña no puede estar vacía." if required else None
    if not isinstance(value, str) or not value:
        return f"La contraseña no puede estar vacía."
    if len(value) < 8:
        return f"La contraseña debe tener al menos 8 caracteres."
    if len(value) > 26:
        return f"La contraseña debe tener como máximo 26 caracteres."
    if not PASSWORD_PATTERN.match(value):
        return f"La contraseña solo puede contener letras y números."
    return None


def _validate_role(value: str, required: bool, allowed_roles: set[str] = ALLOWED_USER_ROLES) -> str | None:
    if value is None:
        return "El rol no puede estar vacío." if required else None
    if not isinstance(value, str) or not value.strip():
        return "El rol no puede estar vacío." if required else None
    if value not in allowed_roles:
        if allowed_roles is REGISTER_USER_ROLES:
            return "El rol debe ser 'Alumno' o 'Profesor'."
        return "El rol debe ser 'Alumno', 'Profesor' o 'Admin'."
    return None


def validate_register_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    nombre_error = _validate_name("nombre", payload.get("nombre"), required=True)
    if nombre_error:
        errors["nombre"] = nombre_error

    apellido_error = _validate_name("apellido", payload.get("apellido"), required=True)
    if apellido_error:
        errors["apellido"] = apellido_error

    correo_error = _validate_email_domain(payload.get("correo"))
    if correo_error:
        errors["correo"] = correo_error

    password_error = _validate_password("password", payload.get("password"), required=True)
    if password_error:
        errors["password"] = password_error

    rol_error = _validate_role(payload.get("rol"), required=True, allowed_roles=REGISTER_USER_ROLES)
    if rol_error:
        errors["rol"] = rol_error

    return (len(errors) == 0, errors)


def validate_login_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    correo_error = _validate_email_domain(payload.get("correo"))
    if correo_error:
        errors["correo"] = correo_error

    password_error = _validate_password("password", payload.get("password"), required=True)
    if password_error:
        errors["password"] = password_error

    return (len(errors) == 0, errors)


def validate_update_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    if "nombre" in payload:
        nombre_error = _validate_name("nombre", payload.get("nombre"), required=False)
        if nombre_error:
            errors["nombre"] = nombre_error

    if "apellido" in payload:
        apellido_error = _validate_name("apellido", payload.get("apellido"), required=False)
        if apellido_error:
            errors["apellido"] = apellido_error

    if "correo" in payload:
        correo_error = _validate_email_domain(payload.get("correo"))
        if correo_error:
            errors["correo"] = correo_error

    if "password" in payload and payload.get("password") is not None:
        password_error = _validate_password("password", payload.get("password"), required=False)
        if password_error:
            errors["password"] = password_error

    if "newPassword" in payload and payload.get("newPassword") is not None:
        new_password_error = _validate_password("newPassword", payload.get("newPassword"), required=False)
        if new_password_error:
            errors["newPassword"] = new_password_error

    if "rol" in payload:
        rol_error = _validate_role(payload.get("rol"), required=False)
        if rol_error:
            errors["rol"] = rol_error

    return (len(errors) == 0, errors)


def validate_query_params(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    if "id" in payload:
        id_value = payload.get("id")
        if not isinstance(id_value, int) or id_value <= 0:
            errors["id"] = "El id debe ser un número entero positivo."

    if "correo" in payload:
        correo_error = _validate_email_domain(payload.get("correo"))
        if correo_error:
            errors["correo"] = correo_error

    return (len(errors) == 0, errors)
