import threading
import time

from flask import current_app
from sqlalchemy.exc import IntegrityError

from models import SessionLocal
from models.classroom_invitation_model import ClassroomInvitationModel, InvitationStatus
from models.classroom_model import ClassroomModel
from models.classroom_student_model import ClassroomStudentModel
from services.user_service import get_user_by_id


def create_invitation(sender_id: int, payload: dict) -> ClassroomInvitationModel:
    session = SessionLocal()
    try:
        classroom = session.query(ClassroomModel).filter(ClassroomModel.id == payload["classroom_id"]).first()
        if classroom is None:
            raise ValueError("El classroom especificado no existe.")

        receiver = get_user_by_id(payload["receiver_id"])
        if receiver is None:
            raise ValueError("El alumno invitado no existe.")

        existing_membership = session.query(ClassroomStudentModel).filter(
            ClassroomStudentModel.classroom_id == payload["classroom_id"],
            ClassroomStudentModel.student_id == payload["receiver_id"],
        ).first()
        if existing_membership is not None:
            raise ValueError("El alumno ya pertenece a este classroom.")

        invitation = ClassroomInvitationModel(
            classroom_id=payload["classroom_id"],
            sender_id=sender_id,
            receiver_id=payload["receiver_id"],
            status=InvitationStatus.pendiente,
        )
        session.add(invitation)
        session.commit()
        session.refresh(invitation)
        return invitation
    except IntegrityError:
        session.rollback()
        raise ValueError("No se pudo crear la invitación. Verifique los datos.")
    finally:
        session.close()


def get_pending_invitations_for_receiver(receiver_id: int) -> list[ClassroomInvitationModel]:
    session = SessionLocal()
    try:
        return (
            session.query(ClassroomInvitationModel)
            .filter(
                ClassroomInvitationModel.receiver_id == receiver_id,
                ClassroomInvitationModel.status == InvitationStatus.pendiente,
            )
            .order_by(ClassroomInvitationModel.id)
            .all()
        )
    finally:
        session.close()


def get_invitation_by_id(invitation_id: int) -> ClassroomInvitationModel | None:
    session = SessionLocal()
    try:
        return session.query(ClassroomInvitationModel).filter(ClassroomInvitationModel.id == invitation_id).first()
    finally:
        session.close()


def is_student_in_classroom(classroom_id: int, student_id: int) -> bool:
    session = SessionLocal()
    try:
        membership = session.query(ClassroomStudentModel).filter(
            ClassroomStudentModel.classroom_id == classroom_id,
            ClassroomStudentModel.student_id == student_id,
        ).first()
        return membership is not None
    finally:
        session.close()


def _delete_invitation_after_delay(invitation_id: int, app):
    time.sleep(180)
    with app.app_context():
        session = SessionLocal()
        try:
            invitation = session.query(ClassroomInvitationModel).filter(ClassroomInvitationModel.id == invitation_id).first()
            if invitation is not None:
                session.delete(invitation)
                session.commit()
        finally:
            session.close()


def _schedule_invitation_deletion(invitation_id: int):
    app = current_app._get_current_object()
    thread = threading.Thread(
        target=_delete_invitation_after_delay,
        args=(invitation_id, app),
        daemon=True,
    )
    thread.start()


def create_classroom_student(classroom_id: int, student_id: int) -> ClassroomStudentModel:
    session = SessionLocal()
    try:
        membership = session.query(ClassroomStudentModel).filter(
            ClassroomStudentModel.classroom_id == classroom_id,
            ClassroomStudentModel.student_id == student_id,
        ).first()
        if membership is not None:
            return membership

        membership = ClassroomStudentModel(
            classroom_id=classroom_id,
            student_id=student_id,
        )
        session.add(membership)
        session.commit()
        session.refresh(membership)
        return membership
    finally:
        session.close()


def respond_invitation(invitation_id: int, receiver_id: int, status: str) -> ClassroomInvitationModel:
    session = SessionLocal()
    try:
        invitation = session.query(ClassroomInvitationModel).filter(ClassroomInvitationModel.id == invitation_id).first()
        if invitation is None:
            raise ValueError("Invitación no encontrada.")
        if invitation.receiver_id != receiver_id:
            raise ValueError("No tienes permiso para responder esta invitación.")
        if invitation.status != InvitationStatus.pendiente:
            raise ValueError("La invitación ya ha sido respondida.")

        invitation.status = InvitationStatus(status)
        session.commit()
        session.refresh(invitation)

        if invitation.status == InvitationStatus.aceptada:
            if not is_student_in_classroom(invitation.classroom_id, receiver_id):
                create_classroom_student(invitation.classroom_id, receiver_id)

        _schedule_invitation_deletion(invitation.id)
        return invitation
    finally:
        session.close()
