from pydantic import BaseModel, field_validator
from app.core.validations import validar_nome

class AutorCreate(BaseModel):
    nome: str

    @field_validator("nome")
    @classmethod
    def validar_nome_autor(cls, v: str) -> str:
        # Chama o validador core. Se levantar ValueError, o Pydantic trata como erro de validação
        return validar_nome(v)

class AutorSchema(BaseModel):
    id_autor: int
    nome: str

