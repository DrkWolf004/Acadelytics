from models import SessionLocal
from models.class_folder_model import ClassFolderModel
from models.classroom_model import ClassroomModel, ClassroomType
from models.classroom_student_model import ClassroomStudentModel
from models.user_model import UserModel


def create_classroom(payload: dict, creator_id: int | None = None) -> ClassroomModel:
    session = SessionLocal()
    try:
        classroom = ClassroomModel(
            nombre=payload["nombre"].strip(),
            type=ClassroomType(payload.get("type", "Solitario")),
        )
        session.add(classroom)
        session.flush()

        default_folder = ClassFolderModel(classroom_id=classroom.id)
        session.add(default_folder)

        if creator_id is not None:
            classroom_member = ClassroomStudentModel(
                classroom_id=classroom.id,
                student_id=creator_id,
            )
            session.add(classroom_member)

        session.commit()
        session.refresh(classroom)
        return classroom
    finally:
        session.close()


def get_classrooms_with_folder_ids(user_id: int | None = None) -> list[tuple[ClassroomModel, int | None]]:
    session = SessionLocal()
    try:
        query = (
            session.query(ClassroomModel, ClassFolderModel.id.label("folder_id"))
            .join(ClassFolderModel, ClassFolderModel.classroom_id == ClassroomModel.id)
        )
        if user_id is not None:
            query = query.join(ClassroomStudentModel, ClassroomStudentModel.classroom_id == ClassroomModel.id)
            query = query.filter(ClassroomStudentModel.student_id == user_id)
        return query.order_by(ClassroomModel.id).all()
    finally:
        session.close()


def get_classroom_by_id(classroom_id: int) -> ClassroomModel | None:
    session = SessionLocal()
    try:
        return session.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()
    finally:
        session.close()


def get_classroom_members(classroom_id: int) -> list[UserModel]:
    session = SessionLocal()
    try:
        return (
            session.query(UserModel)
            .join(ClassroomStudentModel, ClassroomStudentModel.student_id == UserModel.id)
            .filter(ClassroomStudentModel.classroom_id == classroom_id)
            .order_by(UserModel.id)
            .all()
        )
    finally:
        session.close()


def is_user_in_classroom(classroom_id: int, user_id: int) -> bool:
    session = SessionLocal()
    try:
        membership = (
            session.query(ClassroomStudentModel)
            .filter(
                ClassroomStudentModel.classroom_id == classroom_id,
                ClassroomStudentModel.student_id == user_id,
            )
            .first()
        )
        return membership is not None
    finally:
        session.close()


def add_classroom_member_by_email(classroom_id: int, correo: str) -> ClassroomStudentModel:
    session = SessionLocal()
    try:
        user = session.query(UserModel).filter(UserModel.correo == correo.strip().lower()).first()
        if user is None:
            raise ValueError("El usuario especificado no existe.")

        existing_membership = session.query(ClassroomStudentModel).filter(
            ClassroomStudentModel.classroom_id == classroom_id,
            ClassroomStudentModel.student_id == user.id,
        ).first()
        if existing_membership is not None:
            raise ValueError("El usuario ya pertenece a este classroom.")

        membership = ClassroomStudentModel(
            classroom_id=classroom_id,
            student_id=user.id,
        )
        session.add(membership)
        session.commit()
        session.refresh(membership)
        return membership
    finally:
        session.close()


def get_all_classrooms() -> list[ClassroomModel]:
    session = SessionLocal()
    try:
        return session.query(ClassroomModel).order_by(ClassroomModel.id).all()
    finally:
        session.close()


def update_classroom(classroom_id: int, payload: dict) -> ClassroomModel | None:
    session = SessionLocal()
    try:
        classroom = session.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()
        if classroom is None:
            return None

        if "nombre" in payload:
            classroom.nombre = payload["nombre"].strip()
        if "type" in payload:
            classroom.type = ClassroomType(payload["type"])

        session.commit()
        session.refresh(classroom)
        return classroom
    finally:
        session.close()


def delete_classroom(classroom_id: int) -> bool:
    session = SessionLocal()
    try:
        classroom = session.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()
        if classroom is None:
            return False

        session.delete(classroom)
        session.commit()
        return True
    finally:
        session.close()
