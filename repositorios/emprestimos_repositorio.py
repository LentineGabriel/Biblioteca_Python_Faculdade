from contexto.database import get_connection
from entidades.emprestimos import Emprestimo
from datetime import datetime, timedelta


class EmprestimosRepositorio:
    # Criar empréstimo
    def criar(self, emprestimo: Emprestimo):
        conn = get_connection()
        cursor = conn.cursor()

        # Calcula o prazo (20 dias após data_emprestimo)
        emprestimo.calcular_prazo()

        cursor.execute(
            """
            INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo, data_prazo, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_emprestimo;
            """,
            (
                emprestimo.id_usuario,
                emprestimo.id_livro,
                emprestimo.data_emprestimo,
                emprestimo.data_prazo,
                "emprestado",  # Status padrão
            ),
        )

        emprestimo.id_emprestimo = cursor.fetchone()[0]
        emprestimo.status = "emprestado"

        conn.commit()
        cursor.close()
        conn.close()

        return emprestimo

    # Listar todos os empréstimos
    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                e.id_emprestimo,
                e.id_usuario,
                e.id_livro,
                e.data_emprestimo,
                e.data_prazo,
                e.data_devolucao,
                e.status,
                u.nome,
                l.nome_livro
            FROM emprestimos e
            LEFT JOIN usuarios u ON u.id_usuario = e.id_usuario
            LEFT JOIN livros l ON l.id_livro = e.id_livro
            ORDER BY e.id_emprestimo ASC;
            """
        )

        rows = cursor.fetchall()
        emprestimos = [Emprestimo(*row) for row in rows]

        cursor.close()
        conn.close()

        return emprestimos

    # Buscar por ID
    def buscar_por_id(self, id_emprestimo):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                e.id_emprestimo,
                e.id_usuario,
                e.id_livro,
                e.data_emprestimo,
                e.data_prazo,
                e.data_devolucao,
                e.status,
                u.nome,
                l.nome_livro
            FROM emprestimos e
            LEFT JOIN usuarios u ON u.id_usuario = e.id_usuario
            LEFT JOIN livros l ON l.id_livro = e.id_livro
            WHERE e.id_emprestimo = %s;
            """,
            (id_emprestimo,),
        )

        row = cursor.fetchone()
        emprestimo = Emprestimo(*row) if row else None

        cursor.close()
        conn.close()

        return emprestimo

    # Buscar empréstimos ativos (não devolvidos)
    def listar_emprestimos_ativos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                e.id_emprestimo,
                e.id_usuario,
                e.id_livro,
                e.data_emprestimo,
                e.data_prazo,
                e.data_devolucao,
                e.status,
                u.nome,
                l.nome_livro
            FROM emprestimos e
            LEFT JOIN usuarios u ON u.id_usuario = e.id_usuario
            LEFT JOIN livros l ON l.id_livro = e.id_livro
            WHERE e.status = 'emprestado'
            ORDER BY e.data_prazo ASC;
            """
        )

        rows = cursor.fetchall()
        emprestimos = [Emprestimo(*row) for row in rows]

        cursor.close()
        conn.close()

        return emprestimos

    # Registrar devolução
    def registrar_devolucao(self, id_emprestimo):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE emprestimos
            SET data_devolucao = CURRENT_TIMESTAMP, status = 'devolvido'
            WHERE id_emprestimo = %s;
            """,
            (id_emprestimo,),
        )

        conn.commit()
        cursor.close()
        conn.close()

    # Atualizar status para atrasado
    def marcar_como_atrasado(self, id_emprestimo):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE emprestimos
            SET status = 'atrasado'
            WHERE id_emprestimo = %s AND status = 'emprestado';
            """,
            (id_emprestimo,),
        )

        conn.commit()
        cursor.close()
        conn.close()

    # Deletar empréstimo
    def deletar(self, id_emprestimo):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM emprestimos WHERE id_emprestimo = %s;",
            (id_emprestimo,),
        )

        conn.commit()
        cursor.close()
        conn.close()
