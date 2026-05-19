class LivrosAutor:
    def __init__(self, id_livro: int = None, id_autor: int = None):
        self.id_livro = id_livro
        self.id_autor = id_autor

    def __repr__(self):
        return (
            f"id_livro = {self.id_livro}, "
            f"id_autor = {self.id_autor}"
        )
