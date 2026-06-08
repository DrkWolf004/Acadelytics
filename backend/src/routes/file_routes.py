from flask import Blueprint, request

from controllers.file_controller import (
    create_file_controller,
    delete_file_controller,
    edit_file_controller,
    get_file_by_id_controller,
    get_files_controller,
)
from middlewares.authentication import authenticate_jwt

file_blueprint = Blueprint("file_blueprint", __name__)


@file_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_file_route():
    return create_file_controller(request.get_json() or {})


@file_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_files_route():
    class_folder_id = request.args.get("class_folder_id", type=int)
    return get_files_controller(class_folder_id)


@file_blueprint.route("/<int:file_id>", methods=["GET"])
@authenticate_jwt
def get_file_by_id_route(file_id: int):
    return get_file_by_id_controller(file_id)


@file_blueprint.route("/<int:file_id>", methods=["PUT"])
@authenticate_jwt
def update_file_route(file_id: int):
    return edit_file_controller(file_id, request.get_json() or {})


@file_blueprint.route("/<int:file_id>", methods=["DELETE"])
@authenticate_jwt
def delete_file_route(file_id: int):
    return delete_file_controller(file_id)
