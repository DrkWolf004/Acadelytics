from flask import Blueprint, g, request

from controllers.professor_validation_controller import (
    create_professor_validation_request_controller,
    delete_professor_validation_request_controller,
    get_professor_validation_file_controller,
    get_professor_validation_request_controller,
    list_professor_validation_requests_controller,
    review_professor_validation_request_controller,
)
from middlewares.authentication import authenticate_jwt

professor_validation_blueprint = Blueprint("professor_validation_blueprint", __name__)


@professor_validation_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_professor_validation_request_route():
    current_user = g.current_user or {}
    if "file" not in request.files:
        return {"status": "error", "message": "No se proporcionó ningún archivo.", "code": 400}, 400
    file_obj = request.files["file"]
    return create_professor_validation_request_controller(file_obj, current_user)


@professor_validation_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def list_professor_validation_requests_route():
    current_user = g.current_user or {}
    status = request.args.get("status")
    return list_professor_validation_requests_controller(current_user, status=status)


@professor_validation_blueprint.route("/<int:request_id>", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_professor_validation_request_route(request_id: int):
    current_user = g.current_user or {}
    return get_professor_validation_request_controller(request_id, current_user)


@professor_validation_blueprint.route("/<int:request_id>/file", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_professor_validation_file_route(request_id: int):
    current_user = g.current_user or {}
    return get_professor_validation_file_controller(request_id, current_user)


@professor_validation_blueprint.route("/<int:request_id>/review", methods=["PUT"], strict_slashes=False)
@authenticate_jwt
def review_professor_validation_request_route(request_id: int):
    current_user = g.current_user or {}
    payload = request.get_json() or {}
    return review_professor_validation_request_controller(request_id, payload, current_user)


@professor_validation_blueprint.route("/<int:request_id>", methods=["DELETE"], strict_slashes=False)
@authenticate_jwt
def delete_professor_validation_request_route(request_id: int):
    current_user = g.current_user or {}
    return delete_professor_validation_request_controller(request_id, current_user)
