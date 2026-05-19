from fastapi import APIRouter, HTTPException
from typing import List

from app.models.editora import Editora
from app.repositories.editora_repositorio import EditoraRepositorio
from app.schemas.editora import EditoraCreate, EditoraSchema
from app.schemas.utils import entity_to_schema

router = APIRouter()
editora_repo = EditoraRepositorio()

@router.post("/", response_model=EditoraSchema)
def criar_editora(editora: EditoraCreate):
    nova_editora = editora_repo.criar(Editora(nome=editora.nome))
    return entity_to_schema(nova_editora, EditoraSchema)

@router.get("/", response_model=List[EditoraSchema])
def listar_editoras():
    return [entity_to_schema(e, EditoraSchema) for e in editora_repo.listar()]

@router.get("/{id_editora}", response_model=EditoraSchema)
def buscar_editora(id_editora: int):
    editora = editora_repo.buscar_por_id(id_editora)
    if not editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return entity_to_schema(editora, EditoraSchema)

@router.put("/{id_editora}", response_model=EditoraSchema)
def atualizar_editora(id_editora: int, editora: EditoraCreate):
    if not editora_repo.atualizar_nome(id_editora, editora.nome):
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return buscar_editora(id_editora)

@router.delete("/{id_editora}")
def deletar_editora(id_editora: int):
    if not editora_repo.deletar(id_editora):
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return {"detail": "Editora removida"}
