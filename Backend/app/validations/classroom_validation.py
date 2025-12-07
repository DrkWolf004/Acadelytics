from typing import Annotated, Optional, Dict, Any, List
from pydantic import BaseModel, validator, StringConstraints, ValidationError
import re

NAME_RE = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')  


class ClassroomQueryValidationModel(BaseModel):
    id: Optional[int] = None
    nombre: Annotated[Optional[str], StringConstraints(min_length=1, max_length=100)] = None
    member_id: Optional[int] = None

    @validator('id', pre=True)
    def convert_id_to_int(cls, v):
        if v is None:
            return v
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError("El id debe ser un número entero")

    @validator('member_id', pre=True)
    def convert_member_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("member_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("member_id debe ser un entero válido")

    @validator('nombre')
    def nombre_letters_spaces(cls, v):
        if v is None:
            return v
        sval = v.strip()
        if not NAME_RE.match(sval):
            raise ValueError("nombre debe contener solo letras y espacios")
        return sval

    class Config:
        extra = 'forbid'


class ClassroomBodyValidationModel(BaseModel):
    nombre: Annotated[Optional[str], StringConstraints(min_length=1, max_length=100)] = None
    member_id: Optional[int] = None

    @validator('member_id', pre=True)
    def convert_member_to_int(cls, v):
        if v is None or v == '':
            return None
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError("member_id debe ser un entero positivo")
            return iv
        except (ValueError, TypeError):
            raise ValueError("member_id debe ser un entero válido")

    @validator('nombre')
    def nombre_letters_spaces(cls, v):
        if v is None:
            return v
        sval = v.strip()
        if not NAME_RE.match(sval):
            raise ValueError("nombre debe contener solo letras y espacios")
        return sval

    class Config:
        extra = 'forbid'


def ClassroomQueryValidation(data: Dict[str, Any]) -> List[Dict[str, Any]] | Dict:
    
    try:
        ClassroomQueryValidationModel(**(data or {}))
        return {}
    except ValidationError as e:
        return e.errors()


def ClassroomBodyValidation(data: Dict[str, Any], require_member: bool = True, require_nombre: bool = True) -> List[Dict[str, Any]] | Dict:
    
    try:
        ClassroomBodyValidationModel(**(data or {}))
        
        missing = []
        if require_member and ('member_id' not in (data or {}) or data.get('member_id') in (None, '')):
            missing.append({'loc': ['member_id'], 'msg': 'member_id is required', 'type': 'value_error.missing'})
        if require_nombre and ('nombre' not in (data or {}) or not str(data.get('nombre') or '').strip()):
            missing.append({'loc': ['nombre'], 'msg': 'nombre is required', 'type': 'value_error.missing'})
        if missing:
            return missing
        return {}
    except ValidationError as e:
        return e.errors()