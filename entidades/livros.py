class Livro:
    def __init__(
        self,
        id_livro=None,
        nome_livro=None,
        id_editora=None,
        id_autor=None,
        nome_autor=None,
        nome_editora=None,
    ):
        self.id_livro = id_livro
        self.nome_livro = nome_livro
        self.id_editora = id_editora
        self.id_autor = id_autor
        self.nome_autor = nome_autor
        self.nome_editora = nome_editora

    def __repr__(self):
        autor_nome = (self.nome_autor or "").strip()
        autor_str = f"autor = '{autor_nome}'" if autor_nome else ""
        if not autor_str and self.id_autor is not None:
            autor_str = f"id_autor = {self.id_autor}"

        editora_nome = (self.nome_editora or "").strip()
        if editora_nome:
            editora_repr = f"editora = '{editora_nome}'"
        else:
            editora_repr = f"id_editora = {self.id_editora}"

        partes = [
            f"id = {self.id_livro}",
            f"nome = '{self.nome_livro}'",
        ]
        if autor_str:
            partes.append(autor_str)
        partes.append(editora_repr)
        return ", ".join(partes)
