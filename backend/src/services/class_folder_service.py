from models import SessionLocal
from models.class_folder_model import ClassFolderModel
from models.classroom_model import ClassroomModel


def create_class_folder(payload: dict) -> ClassFolderModel:
    session = SessionLocal()
    try:
        classroom = session.query(ClassroomModel).filter(ClassroomModel.id == payload["classroom_id"]).first()
        if classroom is None:
            raise ValueError("La classroom especificada no existe.")

        class_folder = ClassFolderModel(classroom_id=payload["classroom_id"])
        session.add(class_folder)
        session.commit()
        session.refresh(class_folder)
        return class_folder
    finally:
        session.close()


def get_class_folder_by_id(class_folder_id: int) -> ClassFolderModel | None:
    session = SessionLocal()
    try:
        return session.query(ClassFolderModel).filter(ClassFolderModel.id == class_folder_id).first()
    finally:
        session.close()


def get_all_class_folders() -> list[ClassFolderModel]:
    session = SessionLocal()
    try:
        return session.query(ClassFolderModel).order_by(ClassFolderModel.id).all()
    finally:
        session.close()


def get_class_folders_by_classroom_id(classroom_id: int) -> list[ClassFolderModel]:
    session = SessionLocal()
    try:
        return (
            session.query(ClassFolderModel)
            .filter(ClassFolderModel.classroom_id == classroom_id)
            .order_by(ClassFolderModel.id)
            .all()
        )
    finally:
        session.close()


def update_class_folder(class_folder_id: int, payload: dict) -> ClassFolderModel | None:
    session = SessionLocal()
    try:
        class_folder = session.query(ClassFolderModel).filter(ClassFolderModel.id == class_folder_id).first()
        if class_folder is None:
            return None

        if "classroom_id" in payload:
            classroom = session.query(ClassroomModel).filter(ClassroomModel.id == payload["classroom_id"]).first()
            if classroom is None:
                raise ValueError("La classroom especificada no existe.")
            class_folder.classroom_id = payload["classroom_id"]

        session.commit()
        session.refresh(class_folder)
        return class_folder
    finally:
        session.close()


def delete_class_folder(class_folder_id: int) -> bool:
    session = SessionLocal()
    try:
        class_folder = session.query(ClassFolderModel).filter(ClassFolderModel.id == class_folder_id).first()
        if class_folder is None:
            return False

        session.delete(class_folder)
        session.commit()
        return True
    finally:
        session.close()
