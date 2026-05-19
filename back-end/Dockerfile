# Usamos uma imagem oficial do Python slim como base para manter o container leve
FROM python:3.11-slim

WORKDIR /app

# Evita que o Python grave arquivos .pyc em disco (economiza espaço e evita lixo no build)
ENV PYTHONDONTWRITEBYTECODE 1

# Evita que o Python armazene em buffer a saída padrão e a saída de erro (logs instantâneos)
ENV PYTHONUNBUFFERED 1

# Copia e instala as dependências antes do código para aproveitar o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação FastAPI para o container
COPY . .

# Expõe a porta 8000 que a aplicação escutará
EXPOSE 8000

# Executa o Uvicorn como servidor web padrão em produção
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
