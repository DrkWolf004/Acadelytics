from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from services.class_folder_service import (
    create_class_folder,
    delete_class_folder,
    get_all_class_folders,
    get_class_folder_by_id,
    get_class_folders_by_classroom_id,
    update_class_folder,
)
from validations.class_folder_validation import (
    validate_class_folder_data,
    validate_class_folder_update_data,
)


def create_class_folder_controller(request_data: dict):
    valid, errors = validate_class_folder_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        class_folder = create_class_folder(request_data)
        return handle_success(201, "ClassFolder creada correctamente.", {
            "id": class_folder.id,
            "classroom_id": class_folder.classroom_id,
            "create_at": class_folder.create_at.isoformat(),
            "update_at": class_folder.update_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo crear el class folder.")


def edit_class_folder_controller(class_folder_id: int, request_data: dict):
    valid, errors = validate_class_folder_update_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        class_folder = update_class_folder(class_folder_id, request_data)
        if class_folder is None:
            return handle_error_client(404, "ClassFolder no encontrada.")

        return handle_success(200, "ClassFolder actualizada correctamente.", {
            "id": class_folder.id,
            "classroom_id": class_folder.classroom_id,
            "create_at": class_folder.create_at.isoformat(),
            "update_at": class_folder.update_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo actualizar el class folder.")


def delete_class_folder_controller(class_folder_id: int):
    try:
        deleted = delete_class_folder(class_folder_id)
        if not deleted:
            return handle_error_client(404, "ClassFolder no encontrado.")

        return handle_success(200, "ClassFolder eliminado correctamente.")
    except Exception:
        return handle_error_server(500, "No se pudo eliminar el class folder.")


def get_class_folder_by_id_controller(class_folder_id: int):
    try:
        class_folder = get_class_folder_by_id(class_folder_id)
        if class_folder is None:
            return handle_error_client(404, "ClassFolder no encontrado.")

        return handle_success(200, "ClassFolder encontrada.", {
            "id": class_folder.id,
            "classroom_id": class_folder.classroom_id,
            "create_at": class_folder.create_at.isoformat(),
            "update_at": class_folder.update_at.isoformat(),
        })
    except Exception:
        return handle_error_server(500, "No se pudo obtener el class folder.")


def get_class_folders_controller(classroom_id: int | None = None):
    try:
        if classroom_id is not None:
            class_folders = get_class_folders_by_classroom_id(classroom_id)
        else:
            class_folders = get_all_class_folders()

        payload = [
            {
                "id": class_folder.id,
                "classroom_id": class_folder.classroom_id,
                "create_at": class_folder.create_at.isoformat(),
                "update_at": class_folder.update_at.isoformat(),
            }
            for class_folder in class_folders
        ]
        return handle_success(200, "ClassFolders obtenidos correctamente.", payload)
    except Exception:
        return handle_error_server(500, "No se pudieron obtener los class folders.")
