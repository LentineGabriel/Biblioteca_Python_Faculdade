class Autor:
    def __init__(self, id_autor: int = None, nome: str = None):
        self.id_autor = id_autor
        self.nome = nome

    def __repr__(self):
        return f"id = {self.id_autor}, nome = '{self.nome}'"
