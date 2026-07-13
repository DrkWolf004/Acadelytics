from datetime import datetime, timezone
import re


def validate_homework_grade(grade_value) -> tuple[bool, str | None]:
    if grade_value is None:
        return True, None

    if isinstance(grade_value, (int, float)):
        grade_text = str(grade_value)
    else:
        grade_text = str(grade_value).strip()

    if not grade_text:
        return False, "La nota no puede estar vacía."

    if not re.fullmatch(r"^(?:[1-6](?:\.\d)?|7(?:\.0)?)$", grade_text):
        return False, "La nota debe estar entre 1 y 7 con un solo decimal."

    try:
        numeric_grade = float(grade_text)
    except ValueError:
        return False, "La nota debe ser un número válido."

    if numeric_grade < 1 or numeric_grade > 7:
        return False, "La nota debe estar entre 1 y 7."

    if abs(numeric_grade * 10 - round(numeric_grade * 10)) > 1e-9:
        return False, "La nota debe tener un solo decimal."

    return True, None


def validate_homework_payload(payload: dict) -> tuple[bool, dict]:
    errors: dict[str, str] = {}

    classroom_id = payload.get("classroom_id")
    if classroom_id in (None, ""):
        errors["classroom_id"] = "Debes indicar el classroom de la tarea."
    else:
        try:
            int(classroom_id)
        except (TypeError, ValueError):
            errors["classroom_id"] = "El classroom debe ser un identificador válido."

    title = payload.get("title")
    if title is None or str(title).strip() == "":
        errors["title"] = "El título es obligatorio."

    description = payload.get("description")
    if description is None:
        description = ""
    if not isinstance(description, str):
        errors["description"] = "La descripción debe ser texto."

    deadline_at = payload.get("deadline_at")
    if deadline_at in (None, ""):
        errors["deadline_at"] = "Debes indicar una fecha y hora límite."
    else:
        if isinstance(deadline_at, str):
            try:
                parsed_deadline = datetime.fromisoformat(deadline_at.replace("Z", "+00:00"))
            except ValueError:
                errors["deadline_at"] = "La fecha límite debe tener formato válido."
            else:
                if parsed_deadline.tzinfo is None:
                    parsed_deadline = parsed_deadline.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                if parsed_deadline <= now:
                    errors["deadline_at"] = "La fecha límite no puede ser anterior o igual a la fecha actual."
        else:
            errors["deadline_at"] = "La fecha límite debe ser una cadena en formato ISO."

    return len(errors) == 0, errors
