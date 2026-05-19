import psycopg
from app.core.config import settings

def get_connection():
    """
    Abre e retorna uma nova conexão ativa com o banco de dados PostgreSQL.
    
    Diferente da versão anterior que continha credenciais estáticas (hardcoded),
    este conector lê a string de conexão de forma dinâmica através do módulo 'settings',
    respeitando os princípios do 12-Factor App para segurança e portabilidade.
    """
    return psycopg.connect(settings.DATABASE_URL)
