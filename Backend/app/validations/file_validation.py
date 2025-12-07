from typing import Annotated, Optional, Dict, Any, List
from pydantic import BaseModel, validator, StringConstraints, ValidationError
import os

ALLOWED_EXTS = {
    "doc", "docx",
    "ppt", "pptx",
    "xls", "xlsx", "csv", 
    "pdf",
    "jpg", "jpeg", "png",
}

class FileQueryValidationModel(BaseModel):
    id: Optional[int] = None
    creator_id: Optional[int] = None
    classfolder_id: Optional[int] = None

    @validator('id', pre=True)
    def convert_id_to_int(cls, v):
        if v is None:
            return v
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError("El id debe ser un número entero")

    @validator('creator_id', pre=True)
    def convert_creator_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("creator_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("creator_id debe ser un entero válido")

    @validator('classfolder_id', pre=True)
    def convert_classfolder_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("classfolder_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("classfolder_id debe ser un entero válido")

    class Config:
        extra = 'forbid'


class FileBodyValidationModel(BaseModel):
    file: Annotated[Optional[str], StringConstraints(min_length=1, max_length=1024)] = None
    creator_id: Optional[int] = None
    classfolder_id: Optional[int] = None

    @validator('file')
    def check_allowed_extension(cls, v):
        if v is None:
            return v
        v_str = v.strip()
        if v_str == '':
            raise ValueError("file no puede estar vacío")
        
        _, ext = os.path.splitext(v_str)
        if not ext:
            raise ValueError("file debe incluir extensión de archivo")
        ext = ext.lstrip('.').lower()
        if ext not in ALLOWED_EXTS:
            raise ValueError(f"Formato no permitido. Extensiones permitidas: {', '.join(sorted(ALLOWED_EXTS))}")
        return v_str

    @validator('creator_id', pre=True)
    def convert_creator_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("creator_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("creator_id debe ser un entero válido")

    @validator('classfolder_id', pre=True)
    def convert_classfolder_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("classfolder_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("classfolder_id debe ser un entero válido")

    class Config:
        extra = 'forbid'


def FileQueryValidation(data: Dict[str, Any]) -> List[Dict[str, Any]] | Dict:
    try:
        FileQueryValidationModel(**(data or {}))
        return {}
    except ValidationError as e:
        return e.errors()


def FileBodyValidation(data: Dict[str, Any], require_file: bool = True, require_creator: bool = True, require_classfolder: bool = True) -> List[Dict[str, Any]] | Dict:
    try:
        FileBodyValidationModel(**(data or {}))
        missing = []
        if require_file and ('file' not in (data or {}) or not str(data.get('file') or '').strip()):
            missing.append({'loc': ['file'], 'msg': 'file is required', 'type': 'value_error.missing'})
        if require_creator and ('creator_id' not in (data or {}) or data.get('creator_id') in (None, '')):
            missing.append({'loc': ['creator_id'], 'msg': 'creator_id is required', 'type': 'value_error.missing'})
        if require_classfolder and ('classfolder_id' not in (data or {}) or data.get('classfolder_id') in (None, '')):
            missing.append({'loc': ['classfolder_id'], 'msg': 'classfolder_id is required', 'type': 'value_error.missing'})
        if missing:
            return missing
        return {}
    except ValidationError as e:
        return e.errors()
