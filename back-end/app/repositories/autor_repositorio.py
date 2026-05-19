from app.core.database import get_connection
from app.models.autor import Autor

class AutorRepositorio:
    def criar(self, autor: Autor) -> Autor:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO autor (nome)
            VALUES (%s)
            RETURNING id_autor;
        """, (autor.nome,))

        autor.id_autor = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()
        return autor

    def listar(self) -> list[Autor]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM autor
            ORDER BY id_autor ASC;
        """)

        rows = cursor.fetchall()
        autores = [Autor(*row) for row in rows]

        cursor.close()
        conn.close()
        return autores

    def buscar_por_id(self, id_autor: int) -> Autor | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM autor
            WHERE id_autor = %s;
        """, (id_autor,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Autor(*row) if row else None

    def atualizar_nome(self, id_autor: int, novo_nome: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE autor
            SET nome = %s
            WHERE id_autor = %s;
        """, (novo_nome, id_autor))

        linhas_afetadas = cursor.rowcount
        conn.commit()

        cursor.close()
        conn.close()
        return linhas_afetadas > 0

    def deletar(self, id_autor: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM autor
            WHERE id_autor = %s;
        """, (id_autor,))
        removido = cursor.rowcount > 0
        conn.commit()

        cursor.close()
        conn.close()
        return removido
