import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

cursor.execute("SELECT * FROM usuarios;")
dados = cursor.fetchall()

for linha in dados:
    print(linha)

cursor.close()
conn.close()