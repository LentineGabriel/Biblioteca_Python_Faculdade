from datetime import datetime

class Estante:
    def __init__(
        self,
        id_estante: int = None,
        id_usuario: int = None,
        id_livro: int = None,
        status: str = None,
        data_atualizacao: datetime = None,
        nome_livro: str = None,
        nome_usuario: str = None,
    ):
        self.id_estante = id_estante
        self.id_usuario = id_usuario
        self.id_livro = id_livro
        self.status = status
        self.data_atualizacao = data_atualizacao
        
        # Atributos auxiliares para listagens amigáveis
        self.nome_livro = nome_livro
        self.nome_usuario = nome_usuario

    def __repr__(self):
        partes = [
            f"id_estante = {self.id_estante}",
            f"status = '{self.status}'"
        ]
        
        if self.nome_livro:
            partes.append(f"livro = '{self.nome_livro}'")
        else:
            partes.append(f"id_livro = {self.id_livro}")
            
        if self.nome_usuario:
            partes.append(f"usuario = '{self.nome_usuario}'")
        else:
            partes.append(f"id_usuario = {self.id_usuario}")
            
        if self.data_atualizacao:
            partes.append(f"atualizado_em = '{self.data_atualizacao}'")
            
        return ", ".join(partes)
