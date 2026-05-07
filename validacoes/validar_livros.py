def validar_nome_livro(nome_livro: str) -> str:
    nome_livro = nome_livro.strip()

    if not nome_livro:
        raise ValueError("Nome do livro não pode ser vazio")

    if len(nome_livro) < 2:
        raise ValueError(
            "Nome do livro deve ter pelo menos 2 caracteres"
        )

    if len(nome_livro) > 255:
        raise ValueError(
            "Nome do livro deve ter no máximo 255 caracteres"
        )

    if "  " in nome_livro:
        raise ValueError(
            "Nome do livro não pode conter espaços duplos"
        )

    if not nome_livro[0].isalnum():
        raise ValueError(
            "Nome do livro deve começar com letra ou número"
        )

    if not nome_livro[-1].isalnum():
        raise ValueError(
            "Nome do livro deve terminar com letra ou número"
        )

    return nome_livro