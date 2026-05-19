from app.core.database import get_connection
from app.models.livros import Livro

_SQL_COLUNAS_LIVRO_COM_AUTOR_EDITORA = """
    l.id_livro,
    l.nome_livro,
    l.id_editora,
    (
        SELECT MIN(la2.id_autor)
        FROM livro_autor la2
        WHERE la2.id_livro = l.id_livro
    ),
    (
        SELECT STRING_AGG(a2.nome, ', ' ORDER BY a2.id_autor)
        FROM livro_autor la2
        INNER JOIN autor a2 ON a2.id_autor = la2.id_autor
        WHERE la2.id_livro = l.id_livro
    ),
    ed.nome
"""

class LivrosRepositorio:
    def criar(self, livro: Livro) -> Livro:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO livros (nome_livro, id_editora)
            VALUES (%s, %s)
            RETURNING id_livro;
            """,
            (livro.nome_livro, livro.id_editora),
        )

        livro.id_livro = cursor.fetchone()[0]

        if livro.id_autor is not None:
            cursor.execute(
                """
                INSERT INTO livro_autor (id_livro, id_autor)
                VALUES (%s, %s);
                """,
                (livro.id_livro, livro.id_autor),
            )

        conn.commit()
        cursor.close()
        conn.close()
        return livro

    def listar(self) -> list[Livro]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT
                {_SQL_COLUNAS_LIVRO_COM_AUTOR_EDITORA}
            FROM livros l
            LEFT JOIN editora ed ON ed.id_editora = l.id_editora
            ORDER BY l.id_livro ASC;
            """
        )

        rows = cursor.fetchall()
        livros = [Livro(*row) for row in rows]

        cursor.close()
        conn.close()
        return livros

    def buscar_por_id(self, id_livro: int) -> Livro | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT
                {_SQL_COLUNAS_LIVRO_COM_AUTOR_EDITORA}
            FROM livros l
            LEFT JOIN editora ed ON ed.id_editora = l.id_editora
            WHERE l.id_livro = %s;
            """,
            (id_livro,),
        )

        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Livro(*row) if row else None

    def atualizar_campo(self, id_livro: int, campo: str, novo_valor) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        campos_permitidos = {
            "nome_livro",
            "id_editora",
            "id_autor",
        }

        if campo not in campos_permitidos:
            cursor.close()
            conn.close()
            raise ValueError("Campo inválido.")

        if campo == "id_autor":
            # Remove qualquer autor associado a este livro antes
            cursor.execute(
                """
                DELETE FROM livro_autor
                WHERE id_livro = %s;
                """,
                (id_livro,),
            )
            # Se um novo ID de autor foi enviado, cria a nova associação
            if novo_valor is not None:
                cursor.execute(
                    """
                    INSERT INTO livro_autor (id_livro, id_autor)
                    VALUES (%s, %s);
                    """,
                    (id_livro, novo_valor),
                )
            atualizado = True
        else:
            query = f"""
                UPDATE livros
                SET {campo} = %s
                WHERE id_livro = %s;
            """
            cursor.execute(query, (novo_valor, id_livro))
            atualizado = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()
        return atualizado


    def deletar(self, id_livro: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM livros
            WHERE id_livro = %s;
            """,
            (id_livro,),
        )

        deletado = cursor.rowcount > 0
        conn.commit()

        cursor.close()
        conn.close()
        return deletado
