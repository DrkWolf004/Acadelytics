from flask import Blueprint, request, make_response
from app.services.auth_service import login_service, register_service
from app.validations.auth_validation import auth_validation, register_validation
from app.handlers.response_handlers import handle_error_client, handle_error_server, handle_success

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    try:
        body = request.get_json()
        errors = auth_validation(body)
        if errors:
            return handle_error_client(400, 'Error de validación', errors)

        access_token, error_token = login_service(body)
        if error_token:
            return handle_error_client(400, 'Error iniciando sesión', error_token)

        response = make_response(handle_success(200, 'Inicio de sesión exitoso', {'token': access_token}))
        response.set_cookie('jwt', access_token, httponly=True, max_age=24*60*60)
        return response

    except Exception as error:
        return handle_error_server(str(error))

@bp.route('/register', methods=['POST'])
def register():
    try:
        body = request.get_json()
        errors = register_validation(body)
        if errors:
            return handle_error_client(400, 'Error de validación', errors)

        new_user, error_new_user = register_service(body)
        if error_new_user:
            return handle_error_client(400, 'Error registrando al usuario', error_new_user)

        return handle_success(201, 'Usuario registrado con éxito', new_user)

    except Exception as error:
        return handle_error_server(str(error))

@bp.route('/logout', methods=['POST'])
def logout():
    try:
        response = make_response(handle_success(200, 'Sesión cerrada exitosamente'))
        response.delete_cookie('jwt', httponly=True)
        return response
    except Exception as error:
        return handle_error_server(str(error))
