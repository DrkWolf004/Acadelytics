from flask import Blueprint, request

from controllers.classroom_invitation_controller import (
    list_received_invitations_controller,
    respond_invitation_controller,
    send_invitation_controller,
)
from middlewares.authentication import authenticate_jwt
from middlewares.authorization import is_profesor

invitation_blueprint = Blueprint("invitation_blueprint", __name__)


@invitation_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
@is_profesor
def send_invitation_route():
    return send_invitation_controller(request.get_json() or {})


@invitation_blueprint.route("/received", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def list_received_invitations_route():
    return list_received_invitations_controller()


@invitation_blueprint.route("/<int:invitation_id>", methods=["PUT"])
@authenticate_jwt
def respond_invitation_route(invitation_id: int):
    return respond_invitation_controller(invitation_id, request.get_json() or {})
