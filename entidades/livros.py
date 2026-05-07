class Livro:
    def __init__(self, id_livro=None, nome_livro=None, id_editora=None):
        self.id_livro = id_livro
        self.nome_livro = nome_livro
        self.id_editora = id_editora

    def __repr__(self):
        return (
            f"id = {self.id_livro}, "
            f"nome = '{self.nome_livro}', "
            f"id_editora = {self.id_editora}"
        )