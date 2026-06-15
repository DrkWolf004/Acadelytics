import os
import uuid
from werkzeug.utils import secure_filename

from models import SessionLocal
from models.class_folder_model import ClassFolderModel
from models.file_model import FileModel


UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")


def ensure_uploads_dir_exists(class_folder_id: int) -> str:
    """Create uploads directory structure and return the path."""
    folder_path = os.path.join(UPLOADS_DIR, str(class_folder_id))
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_uploaded_file(file_obj, class_folder_id: int) -> tuple[str, str]:
    """
    Save uploaded file to disk and return (secure_name, filepath).
    
    Returns:
        tuple: (secure_filename, full_filepath)
    """
    if not hasattr(file_obj, 'filename'):
        raise ValueError("Invalid file object")
    
    original_filename = secure_filename(file_obj.filename)
    if not original_filename:
        raise ValueError("Invalid filename")
    
    name_parts = os.path.splitext(original_filename)
    secure_name = f"{uuid.uuid4().hex}_{name_parts[0]}{name_parts[1]}"
    
    folder_path = ensure_uploads_dir_exists(class_folder_id)
    
    filepath = os.path.join(folder_path, secure_name)
    file_obj.save(filepath)
    
    return secure_name, filepath


def create_file(payload: dict) -> FileModel:
    """Create a file record from JSON payload (legacy method)."""
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


def create_file_from_upload(class_folder_id: int, file_obj) -> FileModel:
    """Create a file record from an uploaded file."""
    session = SessionLocal()
    try:
        class_folder = session.query(ClassFolderModel).filter(ClassFolderModel.id == class_folder_id).first()
        if class_folder is None:
            raise ValueError("El class folder especificado no existe.")
        
        secure_name, filepath = save_uploaded_file(file_obj, class_folder_id)
        
        file_record = FileModel(
            class_folder_id=class_folder_id,
            filename=file_obj.filename,
            secure_name=secure_name,
            filepath=filepath,
        )
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
        return file_record
    finally:
        session.close()


def delete_file_from_disk(file_id: int) -> bool:
    """Delete file from disk and database."""
    session = SessionLocal()
    try:
        file_record = session.query(FileModel).filter(FileModel.id == file_id).first()
        if file_record is None:
            return False
        
        if os.path.exists(file_record.filepath):
            try:
                os.remove(file_record.filepath)
            except OSError:
                pass
        
        session.delete(file_record)
        session.commit()
        return True
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
