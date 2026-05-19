from fastapi import APIRouter, HTTPException
from typing import List

from app.models.autor import Autor
from app.repositories.autor_repositorio import AutorRepositorio
from app.schemas.autor import AutorCreate, AutorSchema
from app.schemas.utils import entity_to_schema

router = APIRouter()
autor_repo = AutorRepositorio()

@router.post("/", response_model=AutorSchema)
def criar_autor(autor: AutorCreate):
    novo_autor = autor_repo.criar(Autor(nome=autor.nome))
    return entity_to_schema(novo_autor, AutorSchema)

@router.get("/", response_model=List[AutorSchema])
def listar_autores():
    return [entity_to_schema(a, AutorSchema) for a in autor_repo.listar()]

@router.get("/{id_autor}", response_model=AutorSchema)
def buscar_autor(id_autor: int):
    autor = autor_repo.buscar_por_id(id_autor)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return entity_to_schema(autor, AutorSchema)

@router.put("/{id_autor}", response_model=AutorSchema)
def atualizar_autor(id_autor: int, autor: AutorCreate):
    if not autor_repo.atualizar_nome(id_autor, autor.nome):
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return buscar_autor(id_autor)

@router.delete("/{id_autor}")
def deletar_autor(id_autor: int):
    if not autor_repo.deletar(id_autor):
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return {"detail": "Autor removido"}
