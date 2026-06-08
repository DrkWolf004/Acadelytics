from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class FileModel(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    class_folder_id = Column(Integer, ForeignKey("class_folders.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    secure_name = Column(String(255), nullable=False)
    filepath = Column(String(1024), nullable=False)
    upload_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    class_folder = relationship("ClassFolderModel", back_populates="files")

    def __repr__(self) -> str:
        return f"<FileModel id={self.id} filename={self.filename} class_folder_id={self.class_folder_id}>"
