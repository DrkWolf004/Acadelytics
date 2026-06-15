from flask import Blueprint, g, request

from controllers.user_controller import (
    create_user_controller,
    delete_user_controller,
    edit_user_controller,
    get_all_users_controller,
    get_user_by_email_controller,
    get_user_by_id_controller,
    get_user_query_controller,
)
from handlers.response_handlers import handle_error_client
from middlewares.authentication import authenticate_jwt
from middlewares.authorization import is_admin

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
@is_admin
def create_user_route():
    return create_user_controller(request.get_json() or {})


@user_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_users_route():
    current_user = g.current_user or {}
    id_param = request.args.get("id")
    correo = request.args.get("correo")

    if id_param or correo:
        query_payload: dict = {}
        if id_param:
            try:
                query_payload["id"] = int(id_param)
            except (TypeError, ValueError):
                return handle_error_client(400, "Validación fallida.", {"id": "El id debe ser un número entero positivo."})
        if correo:
            query_payload["correo"] = correo

        if current_user.get("rol") != "Admin":
            target = None
            if "id" in query_payload and query_payload["id"] != current_user.get("id"):
                return handle_error_client(403, "Acceso denegado.", {"info": "Solo puedes ver tu propio perfil."})
            if "correo" in query_payload and query_payload["correo"] != current_user.get("correo"):
                return handle_error_client(403, "Acceso denegado.", {"info": "Solo puedes ver tu propio perfil."})
        return get_user_query_controller(query_payload)

    return get_all_users_controller(current_user)


@user_blueprint.route("/<int:user_id>", methods=["GET"])
@authenticate_jwt
def get_user_by_id_route(user_id: int):
    current_user = g.current_user or {}
    if current_user.get("rol") != "Admin" and current_user.get("id") != user_id:
        return handle_error_client(403, "Acceso denegado.", {"info": "Solo puedes ver tu propio perfil."})
    return get_user_by_id_controller(user_id)


@user_blueprint.route("/<int:user_id>", methods=["PUT"])
@authenticate_jwt
def update_user_route(user_id: int):
    current_user = g.current_user or {}
    payload = request.get_json() or {}
    if current_user.get("rol") != "Admin" and current_user.get("id") != user_id:
        return handle_error_client(403, "Acceso denegado.", {"info": "Solo puedes editar tu propio perfil."})
    return edit_user_controller(user_id, payload, current_user)


@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
@authenticate_jwt
@is_admin
def delete_user_route(user_id: int):
    return delete_user_controller(user_id)
