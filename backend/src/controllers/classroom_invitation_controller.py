from flask import g

from handlers.response_handlers import handle_error_client, handle_error_server, handle_success
from services.classroom_invitation_service import (
    create_invitation,
    get_pending_invitations_for_receiver,
    get_invitation_by_id,
    respond_invitation,
)
from services.user_service import get_user_by_id
from services.classroom_service import get_classroom_by_id
from validations.classroom_invitation_validation import (
    validate_respond_invitation_data,
    validate_send_invitation_data,
)


def send_invitation_controller(request_data: dict):
    valid, errors = validate_send_invitation_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    sender_id = getattr(g, "current_user", {}).get("id")
    try:
        invitation = create_invitation(sender_id, request_data)
        return handle_success(201, "Invitación enviada correctamente.", {
            "id": invitation.id,
            "classroom_id": invitation.classroom_id,
            "sender_id": invitation.sender_id,
            "receiver_id": invitation.receiver_id,
            "status": invitation.status.value,
            "create_at": invitation.create_at.isoformat(),
            "update_at": invitation.update_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo enviar la invitación.")


def list_received_invitations_controller():
    receiver_id = getattr(g, "current_user", {}).get("id")
    try:
        invitations = get_pending_invitations_for_receiver(receiver_id)
        payload = [
            {
                "id": invitation.id,
                "classroom_id": invitation.classroom_id,
                "sender_id": invitation.sender_id,
                "receiver_id": invitation.receiver_id,
                "status": invitation.status.value,
                "create_at": invitation.create_at.isoformat(),
                "update_at": invitation.update_at.isoformat(),
                "sender_nombre": (get_user_by_id(invitation.sender_id).nombre if get_user_by_id(invitation.sender_id) else None),
                "sender_apellido": (get_user_by_id(invitation.sender_id).apellido if get_user_by_id(invitation.sender_id) else None),
                "classroom_name": (get_classroom_by_id(invitation.classroom_id).nombre if get_classroom_by_id(invitation.classroom_id) else None),
            }
            for invitation in invitations
        ]
        return handle_success(200, "Invitaciones recibidas obtenidas correctamente.", payload)
    except Exception:
        return handle_error_server(500, "No se pudieron obtener las invitaciones.")


def respond_invitation_controller(invitation_id: int, request_data: dict):
    valid, errors = validate_respond_invitation_data(request_data)
    if not valid:
        return handle_error_client(400, "Validación fallida.", errors)

    receiver_id = getattr(g, "current_user", {}).get("id")
    try:
        invitation = respond_invitation(invitation_id, receiver_id, request_data["status"])
        return handle_success(200, "Invitación respondida correctamente.", {
            "id": invitation.id,
            "classroom_id": invitation.classroom_id,
            "sender_id": invitation.sender_id,
            "receiver_id": invitation.receiver_id,
            "status": invitation.status.value,
            "create_at": invitation.create_at.isoformat(),
            "update_at": invitation.update_at.isoformat(),
        })
    except ValueError as error:
        return handle_error_client(400, str(error))
    except Exception:
        return handle_error_server(500, "No se pudo responder la invitación.")
