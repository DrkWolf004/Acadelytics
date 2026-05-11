from flask import Blueprint, request

from controllers.user_controller import (
    create_user_controller,
    delete_user_controller,
    edit_user_controller,
    get_all_users_controller,
    get_user_by_email_controller,
    get_user_by_id_controller,
)
from middlewares.authentication import authenticate_jwt
from middlewares.authorization import is_admin

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_user_route():
    return create_user_controller(request.get_json() or {})


@user_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_users_route():
    correo = request.args.get("correo")
    if correo:
        return get_user_by_email_controller(correo)
    return get_all_users_controller()


@user_blueprint.route("/<int:user_id>", methods=["GET"])
@authenticate_jwt
def get_user_by_id_route(user_id: int):
    return get_user_by_id_controller(user_id)


@user_blueprint.route("/<int:user_id>", methods=["PUT"])
@authenticate_jwt
def update_user_route(user_id: int):
    return edit_user_controller(user_id, request.get_json() or {})


@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
@authenticate_jwt
@is_admin
def delete_user_route(user_id: int):
    return delete_user_controller(user_id)
