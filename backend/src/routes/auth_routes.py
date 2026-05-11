from flask import Blueprint, request

from controllers.user_controller import login_user_controller, register_user_controller

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register_route():
    return register_user_controller(request.get_json() or {})


@auth_blueprint.route("/login", methods=["POST"])
def login_route():
    return login_user_controller(request.get_json() or {})
