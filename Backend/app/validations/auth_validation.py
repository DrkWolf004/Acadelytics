from typing import Annotated
from pydantic import BaseModel, validator, StringConstraints, EmailStr, ValidationError
import re

def domain_email_validator(email: str) -> str:
    if not (email.endswith("@gmail.com") or email.endswith("@local.test")):
        raise ValueError("El correo electrónico debe finalizar en @gmail.com o @local.test.")
    return email

class AuthValidationModel(BaseModel):
    email: Annotated[str, StringConstraints(min_length=15, max_length=35)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=26, pattern=r"^[a-zA-Z0-9]+$")]

    @validator('email')
    def validate_email(cls, v):
        return domain_email_validator(v)

class RegisterValidationModel(BaseModel):
    nombreCompleto: Annotated[str, StringConstraints(min_length=15, max_length=50)]
    rut: Annotated[str, StringConstraints(min_length=9, max_length=12)]
    email: Annotated[str, StringConstraints(min_length=15, max_length=35)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=26, pattern=r"^[a-zA-Z0-9]+$")]

    @validator('nombreCompleto')
    def validate_nombre_completo(cls, v):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", v):
            raise ValueError("El nombre completo solo puede contener letras y espacios.")
        return v

    @validator('rut')
    def validate_rut(cls, v):
        rut_pattern = r"^(?:(?:[1-9]\d{0}|[1-2]\d{1})(\.\d{3}){2}|[1-9]\d{6}|[1-2]\d{7}|29\.999\.999|29999999)-[\dkK]$"
        if not re.match(rut_pattern, v):
            raise ValueError("El RUT no tiene un formato válido.")
        return v

    @validator('email')
    def validate_email(cls, v):
        return domain_email_validator(v)

def auth_validation(data: dict) -> dict:
    """Valida datos de autenticación y retorna errores si los hay"""
    try:
        AuthValidationModel(**data)
        return {}
    except ValidationError as e:
        return e.errors()

def register_validation(data: dict) -> dict:
    """Valida datos de registro y retorna errores si los hay"""
    try:
        RegisterValidationModel(**data)
        return {}
    except ValidationError as e:
        return e.errors()
