from fastapi import APIRouter, HTTPException
from typing import List

from app.repositories.estante_repositorio import EstanteRepositorio
from app.schemas.estante import EstanteCreate, EstanteSchema
from app.schemas.utils import entity_to_schema

router = APIRouter()
estante_repo = EstanteRepositorio()

@router.post("/", response_model=EstanteSchema)
def adicionar_ou_atualizar_estante(item: EstanteCreate):
    estante = estante_repo.adicionar_ou_atualizar(item.id_usuario, item.id_livro, item.status)
    if not estante:
        raise HTTPException(status_code=400, detail="Não foi possível adicionar ou atualizar o item na estante")
    return entity_to_schema(estante, EstanteSchema)

@router.get("/usuarios/{id_usuario}", response_model=List[EstanteSchema])
def listar_estante_por_usuario(id_usuario: int):
    return [entity_to_schema(item, EstanteSchema) for item in estante_repo.listar_por_usuario(id_usuario)]

@router.get("/usuarios/{id_usuario}/livros/{id_livro}", response_model=EstanteSchema)
def buscar_estante_usuario_livro(id_usuario: int, id_livro: int):
    item = estante_repo.buscar_por_usuario_e_livro(id_usuario, id_livro)
    if not item:
        raise HTTPException(status_code=404, detail="Item da estante não encontrado")
    return entity_to_schema(item, EstanteSchema)

@router.delete("/usuarios/{id_usuario}/livros/{id_livro}")
def remover_estante(id_usuario: int, id_livro: int):
    if not estante_repo.remover(id_usuario, id_livro):
        raise HTTPException(status_code=404, detail="Item da estante não encontrado")
    return {"detail": "Item removido da estante"}
