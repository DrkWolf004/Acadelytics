from flask import Blueprint, request
from app.services.classroom_service import (
    get_classroom_service,
    get_classrooms_service,
    create_classroom_service,
    update_classroom_service,
    delete_classroom_service,
)
from app.validations.classroom_validation import ClassroomQueryValidation, ClassroomBodyValidation
from app.handlers.response_handlers import handle_error_client, handle_error_server, handle_success

bp = Blueprint('classrooms', __name__, url_prefix='/classrooms')


@bp.route('', methods=['GET'])
def get_classroom():
    try:
        query_params = request.args.to_dict()
        errors = ClassroomQueryValidation(query_params)
        if errors:
            return handle_error_client(400, errors)

        classroom, error_classroom = get_classroom_service(query_params)
        if error_classroom:
            return handle_error_client(404, error_classroom)

        return handle_success(200, "Classroom encontrado", classroom)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('/all', methods=['GET'])
def get_classrooms():
    try:
        classrooms, error_classrooms = get_classrooms_service()
        if error_classrooms:
            return handle_error_client(404, error_classrooms)

        if len(classrooms) == 0:
            return handle_success(204, "No hay classrooms")
        else:
            return handle_success(200, "Classrooms encontrados", classrooms)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['POST'])
def create_classroom():
    try:
        body = request.get_json()
        body_errors = ClassroomBodyValidation(body, require_member=True, require_nombre=True)
        if body_errors:
            return handle_error_client(400, "Error de validación en los datos enviados", body_errors)

        classroom, classroom_error = create_classroom_service(body)
        if classroom_error:
            return handle_error_client(400, "Error creando el classroom", classroom_error)

        return handle_success(201, "Classroom creado correctamente", classroom)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['PUT'])
def update_classroom():
    try:
        query_params = request.args.to_dict()
        body = request.get_json()

        query_errors = ClassroomQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        body_errors = ClassroomBodyValidation(body, require_member=False, require_nombre=False)
        if body_errors:
            return handle_error_client(400, "Error de validación en los datos enviados", body_errors)

        classroom, classroom_error = update_classroom_service(query_params, body)
        if classroom_error:
            return handle_error_client(400, "Error modificando el classroom", classroom_error)

        return handle_success(200, "Classroom modificado correctamente", classroom)
    except Exception as error:
        return handle_error_server(str(error))


@bp.route('', methods=['DELETE'])
def delete_classroom():
    try:
        query_params = request.args.to_dict()

        query_errors = ClassroomQueryValidation(query_params)
        if query_errors:
            return handle_error_client(400, "Error de validación en la consulta", query_errors)

        classroom_deleted, error_deleted = delete_classroom_service(query_params)
        if error_deleted:
            return handle_error_client(404, "Error eliminando el classroom", error_deleted)

        return handle_success(200, "Classroom eliminado correctamente", classroom_deleted)
    except Exception as error:
        return handle_error_server(str(error))