class Editora:
    def __init__(self, id_editora: int = None, nome: str = None):
        self.id_editora = id_editora
        self.nome = nome

    def __repr__(self):
        return f"id = {self.id_editora}, nome = '{self.nome}'"
