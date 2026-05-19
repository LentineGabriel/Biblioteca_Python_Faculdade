from typing import Optional
from pydantic import BaseModel, field_validator
from app.core.validations import validar_nome_livro

class LivroCreate(BaseModel):
    nome_livro: str
    id_editora: int
    id_autor: Optional[int] = None

    @field_validator("nome_livro")
    @classmethod
    def val_nome_livro(cls, v: str) -> str:
        return validar_nome_livro(v)

class LivroUpdate(BaseModel):
    nome_livro: Optional[str] = None
    id_editora: Optional[int] = None
    id_autor: Optional[int] = None

    @field_validator("nome_livro")
    @classmethod
    def val_nome_livro(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_nome_livro(v)
        return v


class LivroSchema(BaseModel):
    id_livro: int
    nome_livro: str
    id_editora: Optional[int] = None
    id_autor: Optional[int] = None
    nome_autor: Optional[str] = None
    nome_editora: Optional[str] = None
