import re

NAME_PATTERN = re.compile(r"^[0-9a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$")
ALLOWED_CLASSROOM_TYPES = {"Solitario", "Grupal"}


def _validate_id(field: str, value: int, required: bool = True) -> str | None:
    if value is None:
        return f"El campo {field} es obligatorio." if required else None
    if not isinstance(value, int) or value <= 0:
        return f"El campo {field} debe ser un número entero positivo."
    return None


def _validate_nombre(field: str, value: str, required: bool = True) -> str | None:
    if value is None:
        return f"El campo {field} es obligatorio." if required else None
    if not isinstance(value, str) or not value.strip():
        return f"El campo {field} no puede estar vacío."
    if len(value.strip()) < 2:
        return f"El campo {field} debe tener al menos 2 caracteres."
    if len(value.strip()) > 100:
        return f"El campo {field} debe tener como máximo 100 caracteres."
    if not NAME_PATTERN.match(value):
        return f"El campo {field} solo puede contener letras y espacios."
    return None


def _validate_type(value: str, required: bool = True) -> str | None:
    if value is None:
        return "El campo type es obligatorio." if required else None
    if not isinstance(value, str) or not value.strip():
        return "El campo type no puede estar vacío."
    if value not in ALLOWED_CLASSROOM_TYPES:
        return "El campo type debe ser 'Solitario' o 'Grupal'."
    return None


def validate_classroom_data(payload: dict, current_role: str | None = None) -> tuple[bool, dict]:
    errors: dict = {}

    nombre_error = _validate_nombre("nombre", payload.get("nombre"), required=True)
    if nombre_error:
        errors["nombre"] = nombre_error

    if "type" in payload:
        type_error = _validate_type(payload.get("type"), required=False)
        if type_error:
            errors["type"] = type_error
        elif payload.get("type") == "Grupal" and current_role not in {"Profesor", "Admin"}:
            errors["type"] = "Solo los roles Profesor o Admin pueden establecer el classroom como Grupal."

    return (len(errors) == 0, errors)


def validate_classroom_update_data(payload: dict, current_role: str | None = None) -> tuple[bool, dict]:
    errors: dict = {}

    if "nombre" in payload:
        nombre_error = _validate_nombre("nombre", payload.get("nombre"), required=False)
        if nombre_error:
            errors["nombre"] = nombre_error

    if "type" in payload:
        type_error = _validate_type(payload.get("type"), required=False)
        if type_error:
            errors["type"] = type_error
        elif payload.get("type") == "Grupal" and current_role not in {"Profesor", "Admin"}:
            errors["type"] = "Solo los roles Profesor o Admin pueden establecer el classroom como Grupal."

    return (len(errors) == 0, errors)
