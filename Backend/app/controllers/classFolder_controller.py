from flask import Blueprint, request
from app.services.classFolder_service import (
    get_classfolder_service,
    get_classfolders_service,
    create_classfolder_service,
    update_classfolder_service,
    delete_classfolder_service,
)
from app.validations.classfolder_validation import ClassFolderQueryValidation, ClassFolderBodyValidation
from app.handlers.response_handlers import handle_error_client, handle_error_server, handle_success

bp = Blueprint('classfolders', __name__, url_prefix='/classfolders')


@bp.route('', methods=['GET'])
def get_classfolder():
    try:
        query_params = request.args.to_dict()
        errors = ClassFolderQueryValidation(query_params)
        if errors:
            return handle_error_client(400, errors)

        classfolder, error_cf = get_classfolder_service(query_params)
        if error_cf:
            return handle_error_client(404, error_cf)

        return handle_success(200, "ClassFolder encontrado", classfolder)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('/all', methods=['GET'])
def get_classfolders():
    try:
        classfolders, error_list = get_classfolders_service()
        if error_list:
            return handle_error_client(404, error_list)

        if len(classfolders) == 0:
            return handle_success(204, "No hay classFolders")
        else:
            return handle_success(200, "ClassFolders encontrados", classfolders)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['POST'])
def create_classfolder():
    try:
        body = request.get_json()
        body_errors = ClassFolderBodyValidation(body, require_classroom=True)
        if body_errors:
            return handle_error_client(400, "Error de validación en los datos enviados", body_errors)

        classfolder, cf_error = create_classfolder_service(body)
        if cf_error:
            return handle_error_client(400, "Error creando el classFolder", cf_error)

        return handle_success(201, "ClassFolder creado correctamente", classfolder)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['PUT'])
def update_classfolder():
    try:
        query_params = request.args.to_dict()
        body = request.get_json()

        query_errors = ClassFolderQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        
        body_errors = ClassFolderBodyValidation(body, require_classroom=False)
        if body_errors:
            return handle_error_client(400, "Error de validación en los datos enviados", body_errors)

        classfolder, cf_error = update_classfolder_service(query_params, body)
        if cf_error:
            return handle_error_client(400, "Error modificando el classFolder", cf_error)

        return handle_success(200, "ClassFolder modificado correctamente", classfolder)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['DELETE'])
def delete_classfolder():
    try:
        query_params = request.args.to_dict()

        query_errors = ClassFolderQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        cf_deleted, cf_error = delete_classfolder_service(query_params)
        if cf_error:
            return handle_error_client(404, "Error eliminando el classFolder", cf_error)

        return handle_success(200, "ClassFolder eliminado correctamente", cf_deleted)
    except Exception as error:
        return handle_error_server(str(error))
