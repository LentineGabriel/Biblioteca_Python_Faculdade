from app.core.database import get_connection
from app.models.livros_autor import LivrosAutor

class LivrosAutorRepositorio:
    def criar(self, livro_autor: LivrosAutor) -> LivrosAutor:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livro_autor (id_livro, id_autor)
            VALUES (%s, %s);
        """, (livro_autor.id_livro, livro_autor.id_autor))

        conn.commit()
        cursor.close()
        conn.close()
        return livro_autor

    def listar(self) -> list[LivrosAutor]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM livro_autor
            ORDER BY id_livro ASC, id_autor ASC;
        """)

        rows = cursor.fetchall()
        livro_autores = [LivrosAutor(*row) for row in rows]

        cursor.close()
        conn.close()
        return livro_autores

    def buscar_por_id(self, id_livro: int, id_autor: int) -> LivrosAutor | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM livro_autor
            WHERE id_livro = %s AND id_autor = %s;
        """, (id_livro, id_autor))

        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return LivrosAutor(*row) if row else None

    def listar_por_livro(self, id_livro: int) -> list[LivrosAutor]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM livro_autor
            WHERE id_livro = %s
            ORDER BY id_autor ASC;
        """, (id_livro,))

        rows = cursor.fetchall()
        livro_autores = [LivrosAutor(*row) for row in rows]

        cursor.close()
        conn.close()
        return livro_autores

    def listar_por_autor(self, id_autor: int) -> list[LivrosAutor]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM livro_autor
            WHERE id_autor = %s
            ORDER BY id_livro ASC;
        """, (id_autor,))

        rows = cursor.fetchall()
        livro_autores = [LivrosAutor(*row) for row in rows]

        cursor.close()
        conn.close()
        return livro_autores

    def deletar(self, id_livro: int, id_autor: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM livro_autor
            WHERE id_livro = %s AND id_autor = %s;
        """, (id_livro, id_autor))

        deletado = cursor.rowcount > 0
        conn.commit()

        cursor.close()
        conn.close()
        return deletado
