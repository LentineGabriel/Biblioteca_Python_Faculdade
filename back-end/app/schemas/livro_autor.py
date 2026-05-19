from pydantic import BaseModel

class LivroAutorCreate(BaseModel):
    id_livro: int
    id_autor: int

class LivroAutorSchema(LivroAutorCreate):
    pass
