import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="G1u2",
        port=5432
    )