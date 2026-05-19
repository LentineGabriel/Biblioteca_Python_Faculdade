from pydantic import BaseModel, field_validator
from app.core.validations import validar_nome

class EditoraCreate(BaseModel):
    nome: str

    @field_validator("nome")
    @classmethod
    def validar_nome_editora(cls, v: str) -> str:
        return validar_nome(v)

class EditoraSchema(BaseModel):
    id_editora: int
    nome: str

