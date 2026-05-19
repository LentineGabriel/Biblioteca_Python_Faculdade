from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class EmprestimoCreate(BaseModel):
    id_usuario: int
    id_livro: int
    data_emprestimo: Optional[datetime] = None

class EmprestimoSchema(BaseModel):
    id_emprestimo: int
    id_usuario: int
    id_livro: int
    data_emprestimo: Optional[datetime] = None
    data_prazo: Optional[datetime] = None
    data_devolucao: Optional[datetime] = None
    status: Optional[str] = None
    nome_usuario: Optional[str] = None
    nome_livro: Optional[str] = None
