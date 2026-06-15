import os

from .classroom_validation import _validate_id

ALLOWED_FILE_EXTENSIONS = {".docx", ".xlsx", ".pptx", ".pdf", ".jpg", ".jpeg", ".png", ".zip", ".rar"}


def _validate_string(field: str, value: str, required: bool = True) -> str | None:
    if value is None:
        return f"El campo {field} es obligatorio." if required else None
    if not isinstance(value, str) or not value.strip():
        return f"El campo {field} no puede estar vacío."
    return None


def _validate_filename(field: str, value: str, required: bool = True) -> str | None:
    error = _validate_string(field, value, required=required)
    if error:
        return error

    extension = os.path.splitext(value)[1].lower()
    if extension not in ALLOWED_FILE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_FILE_EXTENSIONS))
        return f"El archivo debe tener una extensión válida: {allowed}."
    return None


def validate_file_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    class_folder_id_error = _validate_id("class_folder_id", payload.get("class_folder_id"), required=True)
    if class_folder_id_error:
        errors["class_folder_id"] = class_folder_id_error

    filename_error = _validate_filename("filename", payload.get("filename"), required=True)
    if filename_error:
        errors["filename"] = filename_error

    secure_name_error = _validate_string("secure_name", payload.get("secure_name"), required=True)
    if secure_name_error:
        errors["secure_name"] = secure_name_error

    filepath_error = _validate_string("filepath", payload.get("filepath"), required=True)
    if filepath_error:
        errors["filepath"] = filepath_error

    return (len(errors) == 0, errors)


def validate_file_update_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    if "class_folder_id" in payload:
        class_folder_id_error = _validate_id("class_folder_id", payload.get("class_folder_id"), required=False)
        if class_folder_id_error:
            errors["class_folder_id"] = class_folder_id_error

    if "filename" in payload:
        filename_error = _validate_filename("filename", payload.get("filename"), required=False)
        if filename_error:
            errors["filename"] = filename_error

    if "secure_name" in payload:
        secure_name_error = _validate_string("secure_name", payload.get("secure_name"), required=False)
        if secure_name_error:
            errors["secure_name"] = secure_name_error

    if "filepath" in payload:
        filepath_error = _validate_string("filepath", payload.get("filepath"), required=False)
        if filepath_error:
            errors["filepath"] = filepath_error

    return (len(errors) == 0, errors)
