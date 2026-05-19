from fastapi import APIRouter, HTTPException
from typing import List

from app.models.livros import Livro
from app.models.livros_autor import LivrosAutor
from app.repositories.livros_repositorio import LivrosRepositorio
from app.repositories.livros_autor_repositorio import LivrosAutorRepositorio
from app.schemas.livro import LivroCreate, LivroUpdate, LivroSchema
from app.schemas.livro_autor import LivroAutorCreate, LivroAutorSchema
from app.schemas.utils import entity_to_schema

router = APIRouter()
livro_repo = LivrosRepositorio()
livro_autor_repo = LivrosAutorRepositorio()

@router.post("/", response_model=LivroSchema)
def criar_livro(livro: LivroCreate):
    novo_livro = livro_repo.criar(
        Livro(nome_livro=livro.nome_livro, id_editora=livro.id_editora, id_autor=livro.id_autor)
    )
    return entity_to_schema(novo_livro, LivroSchema)

@router.get("/", response_model=List[LivroSchema])
def listar_livros():
    return [entity_to_schema(l, LivroSchema) for l in livro_repo.listar()]

@router.get("/{id_livro}", response_model=LivroSchema)
def buscar_livro(id_livro: int):
    livro = livro_repo.buscar_por_id(id_livro)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return entity_to_schema(livro, LivroSchema)

@router.put("/{id_livro}", response_model=LivroSchema)
def atualizar_livro(id_livro: int, livro: LivroUpdate):
    dados = livro.dict(exclude_unset=True) if hasattr(livro, 'dict') else livro.model_dump(exclude_unset=True)
    if not dados:
        raise HTTPException(status_code=400, detail="Nenhum campo fornecido para atualização")

    if not livro_repo.buscar_por_id(id_livro):
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    for campo, valor in dados.items():
        livro_repo.atualizar_campo(id_livro, campo, valor)

    return buscar_livro(id_livro)

@router.delete("/{id_livro}")
def deletar_livro(id_livro: int):
    if not livro_repo.deletar(id_livro):
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return {"detail": "Livro removido"}

# --- ROTAS ASSOCIATIVAS LIVRO-AUTOR ---

@router.post("/{id_livro}/autores", response_model=LivroAutorSchema)
def adicionar_autor_ao_livro(id_livro: int, relacao: LivroAutorCreate):
    if id_livro != relacao.id_livro:
        raise HTTPException(status_code=400, detail="O id_livro da URL deve corresponder ao corpo da requisição")
    
    dados = relacao.dict() if hasattr(relacao, 'dict') else relacao.model_dump()
    relacao_criada = livro_autor_repo.criar(LivrosAutor(**dados))
    return LivroAutorSchema(**vars(relacao_criada))

@router.get("/{id_livro}/autores", response_model=List[LivroAutorSchema])
def listar_autores_do_livro(id_livro: int):
    return [LivroAutorSchema(**vars(item)) for item in livro_autor_repo.listar_por_livro(id_livro)]

@router.delete("/{id_livro}/autores/{id_autor}")
def remover_autor_do_livro(id_livro: int, id_autor: int):
    if not livro_autor_repo.deletar(id_livro, id_autor):
        raise HTTPException(status_code=404, detail="Relação livro-autor não encontrada")
    return {"detail": "Autor removido do livro"}
