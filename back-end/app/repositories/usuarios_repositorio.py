from app.core.database import get_connection
from app.models.usuarios import Usuarios

class UsuariosRepositorio:
    def criar(self, usuario: Usuarios) -> Usuarios:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nome, email, endereco, telefone)
            VALUES (%s, %s, %s, %s)
            RETURNING id_usuario;
        """, (usuario.nome, usuario.email, usuario.endereco, usuario.telefone))

        usuario.id_usuario = cursor.fetchone()[0]
        conn.commit()
        
        cursor.close()
        conn.close()
        return usuario

    def listar(self) -> list[Usuarios]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios ORDER BY id_usuario ASC;")
        rows = cursor.fetchall()
        usuarios = [Usuarios(*row) for row in rows]

        cursor.close()
        conn.close()
        return usuarios

    def buscar_por_id(self, id_usuario: int) -> Usuarios | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return Usuarios(*row) if row else None

    def atualizar_campo(self, id_usuario: int, campo: str, novo_valor) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        campos_permitidos = {"nome", "email", "endereco", "telefone"}
        if campo not in campos_permitidos:
            cursor.close()
            conn.close()
            raise ValueError("Campo inválido para atualização.")

        query = f"UPDATE usuarios SET {campo} = %s WHERE id_usuario = %s;"
        cursor.execute(query, (novo_valor, id_usuario))
        linhas_afetadas = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()
        return linhas_afetadas > 0

    def deletar(self, id_usuario: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
        removido = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()
        return removido
