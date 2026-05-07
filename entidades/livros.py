class Livro:
    def __init__(self, id_livro=None, nome_livro=None, id_editora=None, id_autor=None, nome_autor=None):
        self.id_livro = id_livro
        self.nome_livro = nome_livro
        self.id_editora = id_editora
        self.id_autor = id_autor
        self.nome_autor = nome_autor

    def __repr__(self):
        autor_nome = (self.nome_autor or "").strip()
        autor_str = f"autor = '{autor_nome}'" if autor_nome else ""

        partes = [
            f"id = {self.id_livro}",
            f"nome = '{self.nome_livro}'"
        ]

        if autor_str:
            partes.append(autor_str)
        elif self.id_autor is not None:
            partes.append(f"id_autor = {self.id_autor}")

        partes.append(f"id_editora = {self.id_editora}")
        return ", ".join(partes)