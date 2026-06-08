from .classroom_validation import _validate_id

ALLOWED_INVITATION_STATUSES = {"pendiente", "aceptada", "rechazada"}
ALLOWED_INVITATION_RESPONSES = {"aceptada", "rechazada"}


def _validate_status(value: str, required: bool = True) -> str | None:
    if value is None:
        return "El campo status es obligatorio." if required else None
    if not isinstance(value, str) or not value.strip():
        return "El campo status no puede estar vacío."
    if value not in ALLOWED_INVITATION_STATUSES:
        return "El campo status debe ser 'pendiente', 'aceptada' o 'rechazada'."
    return None


def _validate_response_status(value: str, required: bool = True) -> str | None:
    if value is None:
        return "El campo status es obligatorio." if required else None
    if not isinstance(value, str) or not value.strip():
        return "El campo status no puede estar vacío."
    if value not in ALLOWED_INVITATION_RESPONSES:
        return "El campo status debe ser 'aceptada' o 'rechazada'."
    return None


def validate_send_invitation_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    classroom_id_error = _validate_id("classroom_id", payload.get("classroom_id"), required=True)
    if classroom_id_error:
        errors["classroom_id"] = classroom_id_error

    receiver_id_error = _validate_id("receiver_id", payload.get("receiver_id"), required=True)
    if receiver_id_error:
        errors["receiver_id"] = receiver_id_error

    return (len(errors) == 0, errors)


def validate_respond_invitation_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    status_error = _validate_response_status(payload.get("status"), required=True)
    if status_error:
        errors["status"] = status_error

    return (len(errors) == 0, errors)
