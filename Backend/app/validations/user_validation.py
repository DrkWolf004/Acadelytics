from typing import Annotated, Optional
from pydantic import BaseModel, validator, StringConstraints, EmailStr, ValidationError

def domain_email_validator(email: str) -> str:
    if not (email.endswith("@gmail.com") or email.endswith("@local.test")):
        raise ValueError("El correo electrónico debe ser del dominio @gmail.com o @local.test")
    return email

class UserQueryValidationModel(BaseModel):
    id: Optional[int] = None
    correo: Annotated[Optional[str], StringConstraints(min_length=1, max_length=120)] = None

    @validator('correo')
    def email_domain_check(cls, v):
        if v is None:
            return v
        return domain_email_validator(v)

    @validator('id', pre=True)
    def convert_id_to_int(cls, v):
        if v is None:
            return v
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError("El id debe ser un número entero")

    class Config:
        extra = 'forbid'  

class UserBodyValidationModel(BaseModel):
    nombre: Annotated[Optional[str], StringConstraints(min_length=1, max_length=50)] = None
    apellidos: Annotated[Optional[str], StringConstraints(min_length=1, max_length=50)] = None
    correo: Annotated[Optional[str], StringConstraints(min_length=1, max_length=120)] = None
    password: Annotated[Optional[str], StringConstraints(min_length=8, max_length=256)] = None
    newPassword: Annotated[Optional[str], StringConstraints(min_length=8, max_length=256)] = None
    rol: Annotated[Optional[str], StringConstraints(min_length=6, max_length=13)] = None  

    @validator('correo')
    def email_domain_check(cls, v):
        if v is None:
            return v
        return domain_email_validator(v)

    class Config:
        extra = 'forbid'

def UserQueryValidation(data: dict):
    
    try:
        UserQueryValidationModel(**data)
        return {}
    except ValidationError as e:
        return e.errors()

def UserBodyValidation(data: dict):
    
    try:
        UserBodyValidationModel(**data)
        return {}
    except ValidationError as e:
        return e.errors()
