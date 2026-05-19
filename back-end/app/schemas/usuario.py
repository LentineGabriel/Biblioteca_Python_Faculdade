from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.core.validations import validar_nome, validar_email, validar_endereco, validar_telefone

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    endereco: str
    telefone: str

    @field_validator("nome")
    @classmethod
    def val_nome(cls, v: str) -> str:
        return validar_nome(v)

    @field_validator("email")
    @classmethod
    def val_email(cls, v: EmailStr) -> EmailStr:
        validar_email(v)  # Aplica nossas regras customizadas extras além do EmailStr nativo
        return v

    @field_validator("endereco")
    @classmethod
    def val_endereco(cls, v: str) -> str:
        return validar_endereco(v)

    @field_validator("telefone")
    @classmethod
    def val_telefone(cls, v: str) -> str:
        return validar_telefone(v)

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None

    @field_validator("nome")
    @classmethod
    def val_nome(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_nome(v)
        return v

    @field_validator("email")
    @classmethod
    def val_email(cls, v: Optional[EmailStr]) -> Optional[EmailStr]:
        if v is not None:
            validar_email(v)
        return v

    @field_validator("endereco")
    @classmethod
    def val_endereco(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_endereco(v)
        return v

    @field_validator("telefone")
    @classmethod
    def val_telefone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_telefone(v)
        return v

class UsuarioSchema(BaseModel):
    id_usuario: int
    nome: str
    email: str
    endereco: str
    telefone: str

