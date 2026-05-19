import os
from pathlib import Path
from dotenv import load_dotenv

# Define o caminho base do projeto (raiz da pasta back-end)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Tenta encontrar o arquivo .env no diretório back-end/ ou na raiz do projeto
dotenv_path = BASE_DIR / ".env"
if not dotenv_path.exists():
    dotenv_path = BASE_DIR.parent / ".env"

# Carrega as variáveis do arquivo .env encontrado
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    PROJECT_NAME: str = "Biblioteca API"
    PROJECT_VERSION: str = "1.0"
    
    # DATABASE_URL com fallback seguro para desenvolvimento local tradicional
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:P57u9j@localhost:5432/postgres"
    )

# Instanciamos as configurações globalmente para que todo o app as importe daqui
settings = Settings()
