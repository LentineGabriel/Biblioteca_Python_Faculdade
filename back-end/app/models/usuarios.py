class Usuarios:
    def __init__(
        self,
        id_usuario: int = None,
        nome: str = None,
        email: str = None,
        endereco: str = None,
        telefone: str = None,
    ):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.endereco = endereco
        self.telefone = telefone

    def __repr__(self):
        return f"id = {self.id_usuario}, nome = '{self.nome}', email = '{self.email}', endereco = '{self.endereco}', telefone = '{self.telefone}')"
