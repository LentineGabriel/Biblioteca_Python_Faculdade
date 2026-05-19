from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from app.models.emprestimos import Emprestimo
from app.repositories.emprestimos_repositorio import EmprestimosRepositorio
from app.schemas.emprestimo import EmprestimoCreate, EmprestimoSchema
from app.schemas.utils import entity_to_schema

router = APIRouter()
emprestimo_repo = EmprestimosRepositorio()

@router.post("/", response_model=EmprestimoSchema)
def criar_emprestimo(emprestimo: EmprestimoCreate):
    data_emprestimo = emprestimo.data_emprestimo or datetime.utcnow()
    novo = emprestimo_repo.criar(
        Emprestimo(id_usuario=emprestimo.id_usuario, id_livro=emprestimo.id_livro, data_emprestimo=data_emprestimo)
    )
    return entity_to_schema(novo, EmprestimoSchema)

@router.get("/", response_model=List[EmprestimoSchema])
def listar_emprestimos():
    return [entity_to_schema(e, EmprestimoSchema) for e in emprestimo_repo.listar()]

@router.get("/ativos", response_model=List[EmprestimoSchema])
def listar_emprestimos_ativos():
    return [entity_to_schema(e, EmprestimoSchema) for e in emprestimo_repo.listar_emprestimos_ativos()]

@router.get("/{id_emprestimo}", response_model=EmprestimoSchema)
def buscar_emprestimo(id_emprestimo: int):
    emprestimo = emprestimo_repo.buscar_por_id(id_emprestimo)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return entity_to_schema(emprestimo, EmprestimoSchema)

@router.post("/{id_emprestimo}/devolucao")
def devolver_emprestimo(id_emprestimo: int):
    if not emprestimo_repo.registrar_devolucao(id_emprestimo):
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou já devolvido")
    return {"detail": "Empréstimo devolvido"}

@router.post("/{id_emprestimo}/atrasado")
def atrasar_emprestimo(id_emprestimo: int):
    if not emprestimo_repo.marcar_como_atrasado(id_emprestimo):
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou não pode ser marcado como atrasado")
    return {"detail": "Empréstimo marcado como atrasado"}

@router.delete("/{id_emprestimo}")
def deletar_emprestimo(id_emprestimo: int):
    if not emprestimo_repo.deletar(id_emprestimo):
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return {"detail": "Empréstimo removido"}
