from models import SessionLocal
from models.class_folder_model import ClassFolderModel
from models.classroom_model import ClassroomModel, ClassroomType


def create_classroom(payload: dict) -> ClassroomModel:
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

        session.commit()
        session.refresh(classroom)
        return classroom
    finally:
        session.close()


def get_classroom_by_id(classroom_id: int) -> ClassroomModel | None:
    session = SessionLocal()
    try:
        return session.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()
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
