from flask import Blueprint, request

from controllers.class_folder_controller import (
    create_class_folder_controller,
    delete_class_folder_controller,
    edit_class_folder_controller,
    get_class_folder_by_id_controller,
    get_class_folders_controller,
)
from middlewares.authentication import authenticate_jwt

class_folder_blueprint = Blueprint("class_folder_blueprint", __name__)


@class_folder_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_class_folder_route():
    return create_class_folder_controller(request.get_json() or {})


@class_folder_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_class_folders_route():
    classroom_id = request.args.get("classroom_id", type=int)
    return get_class_folders_controller(classroom_id)


@class_folder_blueprint.route("/<int:class_folder_id>", methods=["GET"])
@authenticate_jwt
def get_class_folder_by_id_route(class_folder_id: int):
    return get_class_folder_by_id_controller(class_folder_id)


@class_folder_blueprint.route("/<int:class_folder_id>", methods=["PUT"])
@authenticate_jwt
def update_class_folder_route(class_folder_id: int):
    return edit_class_folder_controller(class_folder_id, request.get_json() or {})


@class_folder_blueprint.route("/<int:class_folder_id>", methods=["DELETE"])
@authenticate_jwt
def delete_class_folder_route(class_folder_id: int):
    return delete_class_folder_controller(class_folder_id)
