from app.core.database import get_connection
from app.models.editora import Editora

class EditoraRepositorio:
    def criar(self, editora: Editora) -> Editora:
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

    def listar(self) -> list[Editora]:
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

    def buscar_por_id(self, id_editora: int) -> Editora | None:
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

    def atualizar_nome(self, id_editora: int, novo_nome: str) -> bool:
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

    def deletar(self, id_editora: int) -> bool:
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
