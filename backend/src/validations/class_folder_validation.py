from .classroom_validation import _validate_id


def validate_class_folder_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    classroom_id_error = _validate_id("classroom_id", payload.get("classroom_id"), required=True)
    if classroom_id_error:
        errors["classroom_id"] = classroom_id_error

    return (len(errors) == 0, errors)


def validate_class_folder_update_data(payload: dict) -> tuple[bool, dict]:
    errors: dict = {}

    if "classroom_id" in payload:
        classroom_id_error = _validate_id("classroom_id", payload.get("classroom_id"), required=False)
        if classroom_id_error:
            errors["classroom_id"] = classroom_id_error

    return (len(errors) == 0, errors)
