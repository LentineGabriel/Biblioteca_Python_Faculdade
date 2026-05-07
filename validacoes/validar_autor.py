def validar_nome(nome: str) -> str:
    nome = nome.strip() # validando entrada e removendo espaços em branco

    if not nome:
        raise ValueError("Nome não pode ser vazio")

    if len(nome) < 3:
        raise ValueError("Nome deve ter pelo menos 3 caracteres")

    if any(ch.isdigit() for ch in nome):
        raise ValueError("Nome não pode conter números")

    if not nome[0].isalpha() or not nome[-1].isalpha():
        raise ValueError(
            "Nome não pode ter caracteres especiais no início nem no final"
        )

    return nome