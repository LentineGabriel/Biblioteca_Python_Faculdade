from fastapi import APIRouter, HTTPException
from typing import List

from app.models.usuarios import Usuarios
from app.repositories.usuarios_repositorio import UsuariosRepositorio
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioSchema
from app.schemas.utils import entity_to_schema

router = APIRouter()
usuario_repo = UsuariosRepositorio()

@router.post("/", response_model=UsuarioSchema)
def criar_usuario(usuario: UsuarioCreate):
    novo_usuario = usuario_repo.criar(Usuarios(**usuario.dict() if hasattr(usuario, 'dict') else usuario.model_dump()))
    return entity_to_schema(novo_usuario, UsuarioSchema)

@router.get("/", response_model=List[UsuarioSchema])
def listar_usuarios():
    return [entity_to_schema(u, UsuarioSchema) for u in usuario_repo.listar()]

@router.get("/{id_usuario}", response_model=UsuarioSchema)
def buscar_usuario(id_usuario: int):
    usuario = usuario_repo.buscar_por_id(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return entity_to_schema(usuario, UsuarioSchema)

@router.patch("/{id_usuario}", response_model=UsuarioSchema)
def atualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    dados = usuario.dict(exclude_unset=True) if hasattr(usuario, 'dict') else usuario.model_dump(exclude_unset=True)
    if not dados:
        raise HTTPException(status_code=400, detail="Nenhum campo fornecido para atualização")

    if not usuario_repo.buscar_por_id(id_usuario):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for campo, valor in dados.items():
        usuario_repo.atualizar_campo(id_usuario, campo, valor)

    return buscar_usuario(id_usuario)

@router.delete("/{id_usuario}")
def deletar_usuario(id_usuario: int):
    if not usuario_repo.deletar(id_usuario):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"detail": "Usuário removido"}
