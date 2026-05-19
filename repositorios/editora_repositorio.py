from contexto.database import get_connection
from entidades.editora import Editora


class EditoraRepositorio:

    def criar(self, editora: Editora):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO editora (nome)
            VALUES (%s)
            RETURNING id_editora;
        """, (editora.nome,))

        editora.id_editora = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        return editora

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM editora
            ORDER BY id_editora ASC;
        """)

        rows = cursor.fetchall()

        editoras = [Editora(*row) for row in rows]

        cursor.close()
        conn.close()

        return editoras

    def buscar_por_id(self, id_editora):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM editora
            WHERE id_editora = %s;
        """, (id_editora,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return Editora(*row) if row else None

    def atualizar_nome(self, id_editora, novo_nome):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE editora
            SET nome = %s
            WHERE id_editora = %s;
        """, (novo_nome, id_editora))

        linhas_afetadas = cursor.rowcount

        conn.commit()

        cursor.close()
        conn.close()

        return linhas_afetadas > 0

    def deletar(self, id_editora):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM editora
            WHERE id_editora = %s;
        """, (id_editora,))
        removido = cursor.rowcount > 0

        conn.commit()

        cursor.close()
        conn.close()

        return removido
