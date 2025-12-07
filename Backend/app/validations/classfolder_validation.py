from typing import Annotated, Optional, Dict, Any, List
from pydantic import BaseModel, validator, StringConstraints, ValidationError


class ClassFolderQueryValidationModel(BaseModel):
    id: Optional[int] = None
    classroom_id: Optional[int] = None

    @validator('id', pre=True)
    def convert_id_to_int(cls, v):
        if v is None:
            return v
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError("El id debe ser un número entero")

    @validator('classroom_id', pre=True)
    def convert_classroom_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("classroom_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("classroom_id debe ser un entero válido")

    class Config:
        extra = 'forbid'


class ClassFolderBodyValidationModel(BaseModel):
    classroom_id: Optional[int] = None

    @validator('classroom_id', pre=True)
    def convert_classroom_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("classroom_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("classroom_id debe ser un entero válido")

    class Config:
        extra = 'forbid'


def ClassFolderQueryValidation(data: Dict[str, Any]) -> List[Dict[str, Any]] | Dict:
    
    try:
        ClassFolderQueryValidationModel(**(data or {}))
        return {}
    except ValidationError as e:
        return e.errors()


def ClassFolderBodyValidation(data: Dict[str, Any], require_classroom: bool = True) -> List[Dict[str, Any]] | Dict:
    
    try:
        ClassFolderBodyValidationModel(**(data or {}))
        missing = []
        if require_classroom and ('classroom_id' not in (data or {}) or data.get('classroom_id') in (None, '')):
            missing.append({'loc': ['classroom_id'], 'msg': 'classroom_id is required', 'type': 'value_error.missing'})
        if missing:
            return missing
        return {}
    except ValidationError as e:
        return e.errors()