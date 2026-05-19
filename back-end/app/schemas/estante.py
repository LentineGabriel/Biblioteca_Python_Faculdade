from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator

class EstanteCreate(BaseModel):
    id_usuario: int
    id_livro: int
    status: str

    @field_validator("status")
    @classmethod
    def val_status(cls, v: str) -> str:
        v = v.lower().strip()
        status_permitidos = {"lido", "lendo", "quero ler"}
        if v not in status_permitidos:
            raise ValueError("Status inválido. Deve ser 'lido', 'lendo' ou 'quero ler'")
        return v

class EstanteSchema(BaseModel):
    id_estante: int
    id_usuario: int
    id_livro: int
    status: str
    data_atualizacao: Optional[datetime] = None
    nome_livro: Optional[str] = None
    nome_usuario: Optional[str] = None
