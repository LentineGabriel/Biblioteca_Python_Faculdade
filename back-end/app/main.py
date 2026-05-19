import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

# Instancia a aplicação FastAPI definindo o título e versão de forma dinâmica
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API robusta para gerenciamento de biblioteca e controle pessoal de livros (Estante virtual)."
)

# Configuração do Middleware de CORS (Cross-Origin Resource Sharing)
# Essencial para que o seu front-end futuro consiga se conectar e consumir a API localmente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem. Pode ser restrito em produção.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, PATCH, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos HTTP nas requisições
)

# Registro do roteador centralizado contendo todos os endpoints
app.include_router(api_router)

@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raiz amigável para checagem rápida de integridade da API.
    """
    return {
        "message": "API da Biblioteca pronta e operacional",
        "status": "healthy",
        "version": settings.PROJECT_VERSION
    }

if __name__ == "__main__":
    # Inicializa o servidor web Uvicorn caso este arquivo seja rodado diretamente
    # com recarregamento dinâmico em tempo de execução (--reload)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
