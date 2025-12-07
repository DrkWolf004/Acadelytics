from typing import Annotated
from pydantic import BaseModel, validator, StringConstraints, EmailStr, ValidationError
import re

def domain_email_validator(correo: str) -> str:
    if not (correo.endswith("@gmail.com") or correo.endswith("@local.test")):
        raise ValueError("El correo electrónico debe finalizar en @gmail.com o @local.test.")
    return correo

class AuthValidationModel(BaseModel):
    correo: Annotated[str, StringConstraints(min_length=15, max_length=35)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=26, pattern=r"^[a-zA-Z0-9]+$")]

    @validator('correo')
    def validate_email(cls, v):
        return domain_email_validator(v)

class RegisterValidationModel(BaseModel):
    nombreCompleto: Annotated[str, StringConstraints(min_length=15, max_length=50)]
    correo: Annotated[str, StringConstraints(min_length=15, max_length=35)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=26, pattern=r"^[a-zA-Z0-9]+$")]

    @validator('nombreCompleto')
    def validate_nombre_completo(cls, v):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", v):
            raise ValueError("El nombre completo solo puede contener letras y espacios.")
        return v

    @validator('correo')
    def validate_email(cls, v):
        return domain_email_validator(v)

def auth_validation(data: dict) -> dict:
    
    try:
        AuthValidationModel(**data)
        return {}
    except ValidationError as e:
        return e.errors()

def register_validation(data: dict) -> dict:
    
    try:
        RegisterValidationModel(**data)
        return {}
    except ValidationError as e:
        return e.errors()
