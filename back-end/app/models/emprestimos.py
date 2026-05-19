from datetime import datetime, timedelta

class Emprestimo:
    def __init__(
        self,
        id_emprestimo: int = None,
        id_usuario: int = None,
        id_livro: int = None,
        data_emprestimo: datetime = None,
        data_prazo: datetime = None,
        data_devolucao: datetime = None,
        status: str = None,
        nome_usuario: str = None,
        nome_livro: str = None,
    ):
        self.id_emprestimo = id_emprestimo
        self.id_usuario = id_usuario
        self.id_livro = id_livro
        self.data_emprestimo = data_emprestimo
        self.data_prazo = data_prazo
        self.data_devolucao = data_devolucao
        self.status = status
        self.nome_usuario = nome_usuario
        self.nome_livro = nome_livro

    def calcular_prazo(self):
        """Calcula o prazo de devolução (20 dias após a data de empréstimo)"""
        if self.data_emprestimo:
            if isinstance(self.data_emprestimo, str):
                data = datetime.fromisoformat(self.data_emprestimo.replace(" ", "T"))
            else:
                data = self.data_emprestimo
            self.data_prazo = data + timedelta(days=20)
            return self.data_prazo
        return None

    def __repr__(self):
        data_emp = self.data_emprestimo.strftime("%d/%m/%Y %H:%M") if isinstance(self.data_emprestimo, datetime) else str(self.data_emprestimo)
        data_prazo = self.data_prazo.strftime("%d/%m/%Y %H:%M") if isinstance(self.data_prazo, datetime) else str(self.data_prazo)
        data_dev = self.data_devolucao.strftime("%d/%m/%Y %H:%M") if self.data_devolucao and isinstance(self.data_devolucao, datetime) else str(self.data_devolucao) if self.data_devolucao else "N/A"
        
        usuario_str = f"'{self.nome_usuario}'" if self.nome_usuario else f"id_usuario = {self.id_usuario}"
        livro_str = f"'{self.nome_livro}'" if self.nome_livro else f"id_livro = {self.id_livro}"
        
        return f"id = {self.id_emprestimo}, usuario = {usuario_str}, livro = {livro_str}, emprestado em = {data_emp}, prazo = {data_prazo}, devolvido em = {data_dev}, status = '{self.status}'"
