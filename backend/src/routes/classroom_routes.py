from flask import Blueprint, request

from controllers.classroom_controller import (
    create_classroom_controller,
    delete_classroom_controller,
    edit_classroom_controller,
    get_all_classrooms_controller,
    get_classroom_by_id_controller,
)
from middlewares.authentication import authenticate_jwt

classroom_blueprint = Blueprint("classroom_blueprint", __name__)


@classroom_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_classroom_route():
    return create_classroom_controller(request.get_json() or {})


@classroom_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_classrooms_route():
    return get_all_classrooms_controller()


@classroom_blueprint.route("/<int:classroom_id>", methods=["GET"])
@authenticate_jwt
def get_classroom_by_id_route(classroom_id: int):
    return get_classroom_by_id_controller(classroom_id)


@classroom_blueprint.route("/<int:classroom_id>", methods=["PUT"])
@authenticate_jwt
def update_classroom_route(classroom_id: int):
    return edit_classroom_controller(classroom_id, request.get_json() or {})


@classroom_blueprint.route("/<int:classroom_id>", methods=["DELETE"])
@authenticate_jwt
def delete_classroom_route(classroom_id: int):
    return delete_classroom_controller(classroom_id)
