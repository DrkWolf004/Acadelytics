from flask import Blueprint, request
from app.services.user_service import (
    get_user_service,
    get_users_service,
    update_user_service,
    delete_user_service
)
from app.validations.user_validation import UserQueryValidation, UserBodyValidation
from app.handlers.response_handlers import handle_error_client, handle_error_server, handle_success

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET'])
def get_user():
    try:
        query_params = request.args.to_dict()
        errors = UserQueryValidation(query_params)
        if errors:
            return handle_error_client(400, errors)

        user, error_user = get_user_service(query_params)
        if error_user:
            return handle_error_client(404, error_user)

        return handle_success(200, "Usuario encontrado", user)
    except Exception as error:
        return handle_error_server(str(error))

@bp.route('/all', methods=['GET'])
def get_users():
    try:
        users, error_users = get_users_service()
        if error_users:
            return handle_error_client(404, error_users)

        if len(users) == 0:
            return handle_success(204, "No hay usuarios")
        else:
            return handle_success(200, "Usuarios encontrados", users)
    except Exception as error:
        return handle_error_server(str(error))

@bp.route('', methods=['PUT'])
def update_user():
    try:
        query_params = request.args.to_dict()
        body = request.get_json()

        query_errors = UserQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        body_errors = UserBodyValidation(body)
        if body_errors:
            return handle_error_client(400, "Error de validación en los datos enviados", body_errors)

        user, user_error = update_user_service(query_params, body)
        if user_error:
            return handle_error_client(400, "Error modificando al usuario", user_error)

        return handle_success(200, "Usuario modificado correctamente", user)
    except Exception as error:
        return handle_error_server(str(error))

@bp.route('', methods=['DELETE'])
def delete_user():
    try:
        query_params = request.args.to_dict()

        query_errors = UserQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        user_deleted, error_user_deleted = delete_user_service(query_params)
        if error_user_deleted:
            return handle_error_client(404, "Error eliminado al usuario", error_user_deleted)

        return handle_success(200, "Usuario eliminado correctamente", user_deleted)
    except Exception as error:
        return handle_error_server(str(error))
