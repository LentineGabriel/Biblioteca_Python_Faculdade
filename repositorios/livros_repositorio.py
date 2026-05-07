from contexto.database import get_connection
from entidades.livros import Livro


class LivrosRepositorio:
    # criar livros
    def criar(self, livro: Livro):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livros (nome_livro, id_editora)
            VALUES (%s, %s)
            RETURNING id_livro;
        """, (livro.nome_livro, livro.id_editora))

        livro.id_livro = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return livro

    # Listar
    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM livros
            ORDER BY id_livro ASC;
        """)

        rows = cursor.fetchall()

        livros = [Livro(*row) for row in rows]

        cursor.close()
        conn.close()

        return livros

    # buscar por id
    def buscar_por_id(self, id_livro):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM livros
            WHERE id_livro = %s;
        """, (id_livro,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return Livro(*row) if row else None

    # atualizar campo
    def atualizar_campo(self, id_livro, campo, novo_valor):
        conn = get_connection()
        cursor = conn.cursor()

        campos_permitidos = {
            "nome_livro",
            "id_editora"
        }

        if campo not in campos_permitidos:
            cursor.close()
            conn.close()
            raise ValueError("Campo inválido.")

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

    # deletar
    def deletar(self, id_livro):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM livros
            WHERE id_livro = %s;
        """, (id_livro,))

        deletado = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()

        return deletado