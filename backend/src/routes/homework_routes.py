from flask import Blueprint, request, send_file

from controllers.homework_controller import (
    create_homework_controller,
    delete_homework_controller,
    download_homework_attachment_controller,
    download_homework_response_file_controller,
    get_homework_by_id_controller,
    get_homeworks_controller,
    submit_homework_response_controller,
    update_homework_controller,
    get_homework_responses_controller,
    grade_homework_response_controller,
    auto_grade_missing_responses_controller,
)
from middlewares.authentication import authenticate_jwt

homework_blueprint = Blueprint("homework_blueprint", __name__)


@homework_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_homework_route():
    if "file" in request.files:
        return create_homework_controller(request.form.to_dict(), file_obj=request.files["file"])
    return create_homework_controller(request.get_json() or {})


@homework_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_homeworks_route():
    classroom_id = request.args.get("classroom_id", type=int)
    return get_homeworks_controller(classroom_id)


@homework_blueprint.route("/<int:homework_id>", methods=["GET"])
@authenticate_jwt
def get_homework_by_id_route(homework_id: int):
    return get_homework_by_id_controller(homework_id)


@homework_blueprint.route("/<int:homework_id>", methods=["PUT"])
@authenticate_jwt
def update_homework_route(homework_id: int):
    if "file" in request.files:
        return update_homework_controller(homework_id, request.form.to_dict(), file_obj=request.files["file"])
    return update_homework_controller(homework_id, request.get_json() or {})


@homework_blueprint.route("/<int:homework_id>", methods=["DELETE"])
@authenticate_jwt
def delete_homework_route(homework_id: int):
    return delete_homework_controller(homework_id)


@homework_blueprint.route("/<int:homework_id>/responses", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def submit_homework_response_route(homework_id: int):
    if "file" in request.files:
        return submit_homework_response_controller(homework_id, request.form.to_dict(), file_obj=request.files["file"])
    return submit_homework_response_controller(homework_id, request.get_json() or {})


@homework_blueprint.route("/<int:homework_id>/attachment", methods=["GET"])
@authenticate_jwt
def download_homework_attachment_route(homework_id: int):
    return download_homework_attachment_controller(homework_id)


@homework_blueprint.route("/<int:homework_id>/responses", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_homework_responses_route(homework_id: int):
    return get_homework_responses_controller(homework_id)


@homework_blueprint.route("/<int:homework_id>/responses/<int:response_id>/grade", methods=["PUT"])
@authenticate_jwt
def grade_homework_response_route(homework_id: int, response_id: int):
    return grade_homework_response_controller(homework_id, response_id, request.get_json() or {})


@homework_blueprint.route("/<int:homework_id>/responses/<int:response_id>/file", methods=["GET"])
@authenticate_jwt
def download_homework_response_file_route(homework_id: int, response_id: int):
    return download_homework_response_file_controller(homework_id, response_id)


@homework_blueprint.route("/<int:homework_id>/auto-grade", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def auto_grade_missing_responses_route(homework_id: int):
    return auto_grade_missing_responses_controller(homework_id)
