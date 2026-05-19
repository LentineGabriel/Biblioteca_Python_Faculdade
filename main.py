from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from entidades.autor import Autor
from entidades.editora import Editora
from entidades.emprestimos import Emprestimo
from entidades.estante import Estante
from entidades.livros import Livro
from entidades.livros_autor import LivrosAutor
from entidades.usuarios import Usuarios
from repositorios.autor_repositorio import AutorRepositorio
from repositorios.editora_repositorio import EditoraRepositorio
from repositorios.emprestimos_repositorio import EmprestimosRepositorio
from repositorios.estante_repositorio import EstanteRepositorio
from repositorios.livros_autor_repositorio import LivrosAutorRepositorio
from repositorios.livros_repositorio import LivrosRepositorio
from repositorios.usuarios_repositorio import UsuariosRepositorio

app = FastAPI(title="Biblioteca API", version="1.0")

autor_repo = AutorRepositorio()
editora_repo = EditoraRepositorio()
usuario_repo = UsuariosRepositorio()
livro_repo = LivrosRepositorio()
emprestimo_repo = EmprestimosRepositorio()
estante_repo = EstanteRepositorio()
livro_autor_repo = LivrosAutorRepositorio()


class AutorCreate(BaseModel):
    nome: str


class AutorSchema(AutorCreate):
    id_autor: int


class EditoraCreate(BaseModel):
    nome: str


class EditoraSchema(EditoraCreate):
    id_editora: int


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    endereco: str
    telefone: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None


class UsuarioSchema(UsuarioCreate):
    id_usuario: int


class LivroCreate(BaseModel):
    nome_livro: str
    id_editora: int
    id_autor: Optional[int] = None


class LivroUpdate(BaseModel):
    nome_livro: Optional[str] = None
    id_editora: Optional[int] = None


class LivroSchema(BaseModel):
    id_livro: int
    nome_livro: str
    id_editora: Optional[int] = None
    id_autor: Optional[int] = None
    nome_autor: Optional[str] = None
    nome_editora: Optional[str] = None


class LivroAutorCreate(BaseModel):
    id_livro: int
    id_autor: int


class LivroAutorSchema(LivroAutorCreate):
    pass


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


class EstanteCreate(BaseModel):
    id_usuario: int
    id_livro: int
    status: str


class EstanteSchema(BaseModel):
    id_estante: int
    id_usuario: int
    id_livro: int
    status: str
    data_atualizacao: Optional[datetime] = None
    nome_livro: Optional[str] = None
    nome_usuario: Optional[str] = None


def entity_to_schema(entity, schema):
    return schema(**{k: v for k, v in vars(entity).items() if k in schema.__fields__})


@app.get("/")
def root():
    return {"message": "API da Biblioteca pronta"}


@app.post("/autores", response_model=AutorSchema)
def criar_autor(autor: AutorCreate):
    novo_autor = autor_repo.criar(Autor(nome=autor.nome))
    return entity_to_schema(novo_autor, AutorSchema)


@app.get("/autores", response_model=List[AutorSchema])
def listar_autores():
    return [entity_to_schema(a, AutorSchema) for a in autor_repo.listar()]


@app.get("/autores/{id_autor}", response_model=AutorSchema)
def buscar_autor(id_autor: int):
    autor = autor_repo.buscar_por_id(id_autor)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return entity_to_schema(autor, AutorSchema)


@app.put("/autores/{id_autor}", response_model=AutorSchema)
def atualizar_autor(id_autor: int, autor: AutorCreate):
    if not autor_repo.atualizar_nome(id_autor, autor.nome):
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return buscar_autor(id_autor)


@app.delete("/autores/{id_autor}")
def deletar_autor(id_autor: int):
    if not autor_repo.deletar(id_autor):
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return {"detail": "Autor removido"}


@app.post("/editoras", response_model=EditoraSchema)
def criar_editora(editora: EditoraCreate):
    nova_editora = editora_repo.criar(Editora(nome=editora.nome))
    return entity_to_schema(nova_editora, EditoraSchema)


@app.get("/editoras", response_model=List[EditoraSchema])
def listar_editoras():
    return [entity_to_schema(e, EditoraSchema) for e in editora_repo.listar()]


@app.get("/editoras/{id_editora}", response_model=EditoraSchema)
def buscar_editora(id_editora: int):
    editora = editora_repo.buscar_por_id(id_editora)
    if not editora:
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return entity_to_schema(editora, EditoraSchema)


@app.put("/editoras/{id_editora}", response_model=EditoraSchema)
def atualizar_editora(id_editora: int, editora: EditoraCreate):
    if not editora_repo.atualizar_nome(id_editora, editora.nome):
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return buscar_editora(id_editora)


@app.delete("/editoras/{id_editora}")
def deletar_editora(id_editora: int):
    if not editora_repo.deletar(id_editora):
        raise HTTPException(status_code=404, detail="Editora não encontrada")
    return {"detail": "Editora removida"}


@app.post("/usuarios", response_model=UsuarioSchema)
def criar_usuario(usuario: UsuarioCreate):
    novo_usuario = usuario_repo.criar(Usuarios(**usuario.dict()))
    return entity_to_schema(novo_usuario, UsuarioSchema)


@app.get("/usuarios", response_model=List[UsuarioSchema])
def listar_usuarios():
    return [entity_to_schema(u, UsuarioSchema) for u in usuario_repo.listar()]


@app.get("/usuarios/{id_usuario}", response_model=UsuarioSchema)
def buscar_usuario(id_usuario: int):
    usuario = usuario_repo.buscar_por_id(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return entity_to_schema(usuario, UsuarioSchema)


@app.patch("/usuarios/{id_usuario}", response_model=UsuarioSchema)
def atualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    dados = usuario.dict(exclude_unset=True)
    if not dados:
        raise HTTPException(status_code=400, detail="Nenhum campo fornecido para atualização")

    if not usuario_repo.buscar_por_id(id_usuario):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for campo, valor in dados.items():
        usuario_repo.atualizar_campo(id_usuario, campo, valor)

    return buscar_usuario(id_usuario)


@app.delete("/usuarios/{id_usuario}")
def deletar_usuario(id_usuario: int):
    if not usuario_repo.deletar(id_usuario):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"detail": "Usuário removido"}


@app.post("/livros", response_model=LivroSchema)
def criar_livro(livro: LivroCreate):
    novo_livro = livro_repo.criar(Livro(nome_livro=livro.nome_livro, id_editora=livro.id_editora, id_autor=livro.id_autor))
    return entity_to_schema(novo_livro, LivroSchema)


@app.get("/livros", response_model=List[LivroSchema])
def listar_livros():
    return [entity_to_schema(l, LivroSchema) for l in livro_repo.listar()]


@app.get("/livros/{id_livro}", response_model=LivroSchema)
def buscar_livro(id_livro: int):
    livro = livro_repo.buscar_por_id(id_livro)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return entity_to_schema(livro, LivroSchema)


@app.put("/livros/{id_livro}", response_model=LivroSchema)
def atualizar_livro(id_livro: int, livro: LivroUpdate):
    dados = livro.dict(exclude_unset=True)
    if not dados:
        raise HTTPException(status_code=400, detail="Nenhum campo fornecido para atualização")

    if not livro_repo.buscar_por_id(id_livro):
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    for campo, valor in dados.items():
        livro_repo.atualizar_campo(id_livro, campo, valor)

    return buscar_livro(id_livro)


@app.delete("/livros/{id_livro}")
def deletar_livro(id_livro: int):
    if not livro_repo.deletar(id_livro):
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return {"detail": "Livro removido"}


@app.post("/livros/{id_livro}/autores", response_model=LivroAutorSchema)
def adicionar_autor_ao_livro(id_livro: int, relacao: LivroAutorCreate):
    if id_livro != relacao.id_livro:
        raise HTTPException(status_code=400, detail="O id_livro da URL deve corresponder ao corpo da requisição")
    return livro_autor_repo.criar(LivrosAutor(**relacao.dict()))


@app.get("/livros/{id_livro}/autores", response_model=List[LivroAutorSchema])
def listar_autores_do_livro(id_livro: int):
    return [LivroAutorSchema(**vars(item)) for item in livro_autor_repo.listar_por_livro(id_livro)]


@app.delete("/livros/{id_livro}/autores/{id_autor}")
def remover_autor_do_livro(id_livro: int, id_autor: int):
    if not livro_autor_repo.deletar(id_livro, id_autor):
        raise HTTPException(status_code=404, detail="Relação livro-autor não encontrada")
    return {"detail": "Autor removido do livro"}


@app.post("/emprestimos", response_model=EmprestimoSchema)
def criar_emprestimo(emprestimo: EmprestimoCreate):
    data_emprestimo = emprestimo.data_emprestimo or datetime.utcnow()
    novo = emprestimo_repo.criar(Emprestimo(id_usuario=emprestimo.id_usuario, id_livro=emprestimo.id_livro, data_emprestimo=data_emprestimo))
    return entity_to_schema(novo, EmprestimoSchema)


@app.get("/emprestimos", response_model=List[EmprestimoSchema])
def listar_emprestimos():
    return [entity_to_schema(e, EmprestimoSchema) for e in emprestimo_repo.listar()]


@app.get("/emprestimos/{id_emprestimo}", response_model=EmprestimoSchema)
def buscar_emprestimo(id_emprestimo: int):
    emprestimo = emprestimo_repo.buscar_por_id(id_emprestimo)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return entity_to_schema(emprestimo, EmprestimoSchema)


@app.get("/emprestimos/ativos", response_model=List[EmprestimoSchema])
def listar_emprestimos_ativos():
    return [entity_to_schema(e, EmprestimoSchema) for e in emprestimo_repo.listar_emprestimos_ativos()]


@app.post("/emprestimos/{id_emprestimo}/devolucao")
def devolver_emprestimo(id_emprestimo: int):
    if not emprestimo_repo.registrar_devolucao(id_emprestimo):
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou já devolvido")
    return {"detail": "Empréstimo devolvido"}


@app.post("/emprestimos/{id_emprestimo}/atrasado")
def atrasar_emprestimo(id_emprestimo: int):
    if not emprestimo_repo.marcar_como_atrasado(id_emprestimo):
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou não pode ser marcado como atrasado")
    return {"detail": "Empréstimo marcado como atrasado"}


@app.delete("/emprestimos/{id_emprestimo}")
def deletar_emprestimo(id_emprestimo: int):
    if not emprestimo_repo.deletar(id_emprestimo):
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return {"detail": "Empréstimo removido"}


@app.post("/estante", response_model=EstanteSchema)
def adicionar_ou_atualizar_estante(item: EstanteCreate):
    estante = estante_repo.adicionar_ou_atualizar(item.id_usuario, item.id_livro, item.status)
    if not estante:
        raise HTTPException(status_code=400, detail="Não foi possível adicionar ou atualizar o item na estante")
    return entity_to_schema(estante, EstanteSchema)


@app.get("/estante/usuarios/{id_usuario}", response_model=List[EstanteSchema])
def listar_estante_por_usuario(id_usuario: int):
    return [entity_to_schema(item, EstanteSchema) for item in estante_repo.listar_por_usuario(id_usuario)]


@app.get("/estante/usuarios/{id_usuario}/livros/{id_livro}", response_model=EstanteSchema)
def buscar_estante_usuario_livro(id_usuario: int, id_livro: int):
    item = estante_repo.buscar_por_usuario_e_livro(id_usuario, id_livro)
    if not item:
        raise HTTPException(status_code=404, detail="Item da estante não encontrado")
    return entity_to_schema(item, EstanteSchema)


@app.delete("/estante/usuarios/{id_usuario}/livros/{id_livro}")
def remover_estante(id_usuario: int, id_livro: int):
    if not estante_repo.remover(id_usuario, id_livro):
        raise HTTPException(status_code=404, detail="Item da estante não encontrado")
    return {"detail": "Item removido da estante"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
