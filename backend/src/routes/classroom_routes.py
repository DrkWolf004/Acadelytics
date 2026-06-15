from flask import Blueprint, request

from controllers.classroom_controller import (
    add_classroom_member_controller,
    create_classroom_controller,
    delete_classroom_controller,
    edit_classroom_controller,
    get_classroom_by_id_controller,
    get_classroom_members_controller,
    get_user_classrooms_controller,
)
from middlewares.authentication import authenticate_jwt
from middlewares.authorization import is_profesor_or_admin

classroom_blueprint = Blueprint("classroom_blueprint", __name__)


@classroom_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_classroom_route():
    return create_classroom_controller(request.get_json() or {})


@classroom_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_classrooms_route():
    return get_user_classrooms_controller()


@classroom_blueprint.route("/<int:classroom_id>", methods=["GET"])
@authenticate_jwt
def get_classroom_by_id_route(classroom_id: int):
    return get_classroom_by_id_controller(classroom_id)


@classroom_blueprint.route("/<int:classroom_id>/members", methods=["GET"])
@authenticate_jwt
def get_classroom_members_route(classroom_id: int):
    return get_classroom_members_controller(classroom_id)


@classroom_blueprint.route("/<int:classroom_id>/members", methods=["POST"])
@authenticate_jwt
@is_profesor_or_admin
def add_classroom_member_route(classroom_id: int):
    return add_classroom_member_controller(classroom_id, request.get_json() or {})


@classroom_blueprint.route("/<int:classroom_id>", methods=["PUT"])
@authenticate_jwt
def update_classroom_route(classroom_id: int):
    return edit_classroom_controller(classroom_id, request.get_json() or {})


@classroom_blueprint.route("/<int:classroom_id>", methods=["DELETE"])
@authenticate_jwt
def delete_classroom_route(classroom_id: int):
    return delete_classroom_controller(classroom_id)
