from fastapi import APIRouter

from app.api.endpoints import autores, editoras, usuarios, livros, emprestimos, estante

api_router = APIRouter()

# Unificamos todas as subrotas e injetamos tags de documentação para o Swagger
api_router.include_router(autores.router, prefix="/autores", tags=["Autores"])
api_router.include_router(editoras.router, prefix="/editoras", tags=["Editoras"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(livros.router, prefix="/livros", tags=["Livros"])
api_router.include_router(emprestimos.router, prefix="/emprestimos", tags=["Empréstimos"])
api_router.include_router(estante.router, prefix="/estante", tags=["Estante"])
