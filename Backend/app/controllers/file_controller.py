from flask import Blueprint, request
from app.services.file_service import (
    get_file_service,
    get_files_service,
    create_file_service,
    update_file_service,
    delete_file_service,
)
from app.validations.file_validation import FileQueryValidation, FileBodyValidation
from app.handlers.response_handlers import handle_error_client, handle_error_server, handle_success

bp = Blueprint('files', __name__, url_prefix='/files')


@bp.route('', methods=['GET'])
def get_file():
    try:
        query_params = request.args.to_dict()
        errors = FileQueryValidation(query_params)
        if errors:
            return handle_error_client(400, errors)

        file_obj, error_file = get_file_service(query_params)
        if error_file:
            return handle_error_client(404, error_file)

        return handle_success(200, "File encontrado", file_obj)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('/all', methods=['GET'])
def get_files():
    try:
        files, error_files = get_files_service()
        if error_files:
            return handle_error_client(404, error_files)

        if len(files) == 0:
            return handle_success(204, "No hay files")
        else:
            return handle_success(200, "Files encontrados", files)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['POST'])
def create_file():
    try:
        body = request.get_json()
        body_errors = FileBodyValidation(body, require_file=True, require_creator=True, require_classfolder=True)
        if body_errors:
            return handle_error_client(400, "Error de validación en los datos enviados", body_errors)

        file_obj, file_error = create_file_service(body)
        if file_error:
            return handle_error_client(400, "Error creando el file", file_error)

        return handle_success(201, "File creado correctamente", file_obj)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['PUT'])
def update_file():
    try:
        query_params = request.args.to_dict()
        body = request.get_json()

        query_errors = FileQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        body_errors = FileBodyValidation(body, require_file=False, require_creator=False, require_classfolder=False)
        if body_errors:
            return handle_error_client(400, "Error de validación en los datos enviados", body_errors)

        file_obj, file_error = update_file_service(query_params, body)
        if file_error:
            return handle_error_client(400, "Error modificando el file", file_error)

        return handle_success(200, "File modificado correctamente", file_obj)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['DELETE'])
def delete_file():
    try:
        query_params = request.args.to_dict()

        query_errors = FileQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        file_deleted, error_deleted = delete_file_service(query_params)
        if error_deleted:
            return handle_error_client(404, "Error eliminando el file", error_deleted)

        return handle_success(200, "File eliminado correctamente", file_deleted)
    except Exception as error:
        return handle_error_server(str(error))