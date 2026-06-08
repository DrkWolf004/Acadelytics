from models import SessionLocal
from models.class_folder_model import ClassFolderModel
from models.file_model import FileModel


def create_file(payload: dict) -> FileModel:
    session = SessionLocal()
    try:
        class_folder = session.query(ClassFolderModel).filter(ClassFolderModel.id == payload["class_folder_id"]).first()
        if class_folder is None:
            raise ValueError("El class folder especificado no existe.")

        file_record = FileModel(
            class_folder_id=payload["class_folder_id"],
            filename=payload["filename"].strip(),
            secure_name=payload["secure_name"].strip(),
            filepath=payload["filepath"].strip(),
        )
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
        return file_record
    finally:
        session.close()


def get_file_by_id(file_id: int) -> FileModel | None:
    session = SessionLocal()
    try:
        return session.query(FileModel).filter(FileModel.id == file_id).first()
    finally:
        session.close()


def get_all_files() -> list[FileModel]:
    session = SessionLocal()
    try:
        return session.query(FileModel).order_by(FileModel.id).all()
    finally:
        session.close()


def get_files_by_class_folder_id(class_folder_id: int) -> list[FileModel]:
    session = SessionLocal()
    try:
        return (
            session.query(FileModel)
            .filter(FileModel.class_folder_id == class_folder_id)
            .order_by(FileModel.id)
            .all()
        )
    finally:
        session.close()


def update_file(file_id: int, payload: dict) -> FileModel | None:
    session = SessionLocal()
    try:
        file_record = session.query(FileModel).filter(FileModel.id == file_id).first()
        if file_record is None:
            return None

        if "class_folder_id" in payload:
            class_folder = session.query(ClassFolderModel).filter(ClassFolderModel.id == payload["class_folder_id"]).first()
            if class_folder is None:
                raise ValueError("El class folder especificado no existe.")
            file_record.class_folder_id = payload["class_folder_id"]

        if "filename" in payload:
            file_record.filename = payload["filename"].strip()
        if "secure_name" in payload:
            file_record.secure_name = payload["secure_name"].strip()
        if "filepath" in payload:
            file_record.filepath = payload["filepath"].strip()

        session.commit()
        session.refresh(file_record)
        return file_record
    finally:
        session.close()


def delete_file(file_id: int) -> bool:
    session = SessionLocal()
    try:
        file_record = session.query(FileModel).filter(FileModel.id == file_id).first()
        if file_record is None:
            return False

        session.delete(file_record)
        session.commit()
        return True
    finally:
        session.close()
