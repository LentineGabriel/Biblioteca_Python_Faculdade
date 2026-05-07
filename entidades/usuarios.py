class Usuarios:
    def __init__(self, id_usuario=None, nome=None, email=None, endereco=None, telefone=None):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.endereco = endereco
        self.telefone = telefone

    def __repr__(self):
        return f"id = {self.id_usuario}, nome = '{self.nome}', email = '{self.email}', endereco = '{self.endereco}', telefone = '{self.telefone}')"