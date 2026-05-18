from contexto.database import get_connection
from entidades.estante import Estante

class EstanteRepositorio:
    
    def adicionar_ou_atualizar(self, id_usuario, id_livro, status):
        """
        Adiciona um livro à estante do usuário com um status.
        Caso o livro já esteja na estante, o status é atualizado.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO estante (id_usuario, id_livro, status, data_atualizacao)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (id_usuario, id_livro)
            DO UPDATE SET status = EXCLUDED.status, data_atualizacao = CURRENT_TIMESTAMP
            RETURNING id_estante, data_atualizacao;
            """,
            (id_usuario, id_livro, status)
        )
        
        resultado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        if resultado:
            return Estante(
                id_estante=resultado[0],
                id_usuario=id_usuario,
                id_livro=id_livro,
                status=status,
                data_atualizacao=resultado[1]
            )
        return None

    def listar_por_usuario(self, id_usuario):
        """
        Lista todos os livros na estante de um usuário específico,
        trazendo também o nome do livro para exibição.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.id_estante, e.id_usuario, e.id_livro, e.status, e.data_atualizacao, l.nome_livro, u.nome
            FROM estante e
            INNER JOIN livros l ON l.id_livro = e.id_livro
            INNER JOIN usuarios u ON u.id_usuario = e.id_usuario
            WHERE e.id_usuario = %s
            ORDER BY e.data_atualizacao DESC;
            """,
            (id_usuario,)
        )
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        estante_itens = []
        for row in rows:
            estante_itens.append(
                Estante(
                    id_estante=row[0],
                    id_usuario=row[1],
                    id_livro=row[2],
                    status=row[3],
                    data_atualizacao=row[4],
                    nome_livro=row[5],
                    nome_usuario=row[6]
                )
            )
        return estante_itens

    def remover(self, id_usuario, id_livro):
        """
        Remove um livro da estante do usuário.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            DELETE FROM estante
            WHERE id_usuario = %s AND id_livro = %s;
            """,
            (id_usuario, id_livro)
        )
        
        removido = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        
        return removido

    def buscar_por_usuario_e_livro(self, id_usuario, id_livro):
        """
        Busca o registro de um livro específico na estante de um usuário.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.id_estante, e.id_usuario, e.id_livro, e.status, e.data_atualizacao, l.nome_livro, u.nome
            FROM estante e
            INNER JOIN livros l ON l.id_livro = e.id_livro
            INNER JOIN usuarios u ON u.id_usuario = e.id_usuario
            WHERE e.id_usuario = %s AND e.id_livro = %s;
            """,
            (id_usuario, id_livro)
        )
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return Estante(
                id_estante=row[0],
                id_usuario=row[1],
                id_livro=row[2],
                status=row[3],
                data_atualizacao=row[4],
                nome_livro=row[5],
                nome_usuario=row[6]
            )
        return None
