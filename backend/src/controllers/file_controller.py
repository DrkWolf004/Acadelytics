from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from services.file_service import (
    create_file,
    create_file_from_upload,
    delete_file,
    delete_file_from_disk,
    get_all_files,
    get_file_by_id,
    get_files_by_class_folder_id,
    update_file,
)
from validations.file_validation import validate_file_data, validate_file_update_data


def create_file_controller(request_data: dict):
    valid, errors = validate_file_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        file_record = create_file(request_data)
        return handle_success(201, "File creada correctamente.", {
            "id": file_record.id,
            "class_folder_id": file_record.class_folder_id,
            "filename": file_record.filename,
            "secure_name": file_record.secure_name,
            "filepath": file_record.filepath,
            "upload_at": file_record.upload_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo crear el file.")


def edit_file_controller(file_id: int, request_data: dict):
    valid, errors = validate_file_update_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    try:
        file_record = update_file(file_id, request_data)
        if file_record is None:
            return handle_error_client(404, "File no encontrado.")

        return handle_success(200, "File actualizado correctamente.", {
            "id": file_record.id,
            "class_folder_id": file_record.class_folder_id,
            "filename": file_record.filename,
            "secure_name": file_record.secure_name,
            "filepath": file_record.filepath,
            "upload_at": file_record.upload_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo actualizar el file.")


def delete_file_controller(file_id: int):
    try:
        deleted = delete_file_from_disk(file_id)
        if not deleted:
            return handle_error_client(404, "File no encontrado.")

        return handle_success(200, "File eliminado correctamente.")
    except Exception:
        return handle_error_server(500, "No se pudo eliminar el file.")


def get_file_by_id_controller(file_id: int):
    try:
        file_record = get_file_by_id(file_id)
        if file_record is None:
            return handle_error_client(404, "File no encontrado.")

        return handle_success(200, "File encontrado.", {
            "id": file_record.id,
            "class_folder_id": file_record.class_folder_id,
            "filename": file_record.filename,
            "secure_name": file_record.secure_name,
            "filepath": file_record.filepath,
            "upload_at": file_record.upload_at.isoformat(),
        })
    except Exception:
        return handle_error_server(500, "No se pudo obtener el file.")


def get_files_controller(class_folder_id: int | None = None):
    try:
        if class_folder_id is not None:
            files = get_files_by_class_folder_id(class_folder_id)
        else:
            files = get_all_files()

        payload = [
            {
                "id": file_record.id,
                "class_folder_id": file_record.class_folder_id,
                "filename": file_record.filename,
                "secure_name": file_record.secure_name,
                "filepath": file_record.filepath,
                "upload_at": file_record.upload_at.isoformat(),
            }
            for file_record in files
        ]
        return handle_success(200, "Files obtenidos correctamente.", payload)
    except Exception:
        return handle_error_server(500, "No se pudieron obtener los files.")


def upload_file_controller(class_folder_id: int, file_obj):
    """Handle file upload for a specific class folder."""
    try:
        if not file_obj or not file_obj.filename:
            return handle_error_client(400, "No se proporcionó ningún archivo.")

        file_record = create_file_from_upload(class_folder_id, file_obj)
        return handle_success(201, "Archivo subido correctamente.", {
            "id": file_record.id,
            "class_folder_id": file_record.class_folder_id,
            "filename": file_record.filename,
            "secure_name": file_record.secure_name,
            "filepath": file_record.filepath,
            "upload_at": file_record.upload_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception as error:
        return handle_error_server(500, f"No se pudo subir el archivo. {str(error)}")
