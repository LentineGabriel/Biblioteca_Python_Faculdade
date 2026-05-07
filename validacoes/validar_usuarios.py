import re

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

def validar_email(email: str) -> str:
    email = email.strip() # validando entrada e removendo espaços em branco

    if not email:
        raise ValueError("Email não pode ser vazio")

    if any(c.isspace() for c in email):
        raise ValueError("Email não pode conter espaços em branco")

    if email.count("@") != 1:
        raise ValueError("Email inválido. Deve conter exatamente um @")

    local, domain = email.split("@", 1)
    if not local or not domain:
        raise ValueError("Email inválido. Parte antes ou depois do @ não pode ser vazia")

    if ".." in email:
        raise ValueError("Email inválido. Não use pontos consecutivos (..)")

    if local.startswith(".") or local.endswith("."):
        raise ValueError(
            "Email inválido. A parte antes do @ não pode começar ou terminar com ponto"
        )

    if not local[0].isalnum() or not local[-1].isalnum():
        raise ValueError(
            "Email inválido. Use letras ou números no início e no fim da parte antes do @"
        )

    padrao_local = re.compile(r"^[a-zA-Z0-9._-]+$")
    if not padrao_local.fullmatch(local):
        raise ValueError(
            "Email inválido. Antes do @ use apenas letras, números, ponto, hífen e sublinhado"
        )

    padrao_dominio = re.compile(r"^[a-zA-Z0-9.-]+$")
    if not padrao_dominio.fullmatch(domain):
        raise ValueError(
            "Email inválido. No domínio use apenas letras, números, ponto e hífen"
        )

    if not domain.endswith(".com"):
        raise ValueError("Email inválido. Deve terminar com '.com'")

    if len(email) < 11:
        raise ValueError("Email inválido. Deve ter pelo menos 11 caracteres")

    return email

def validar_endereco(endereco: str) -> str:
    endereco = endereco.strip() # validando entrada e removendo espaços em branco

    if not endereco:
        raise ValueError("Endereço não pode ser vazio")

    if len(endereco) < 10:
        raise ValueError("Endereço inválido. Deve ter pelo menos 10 caracteres")

    if len(endereco) > 150:
        raise ValueError("Endereço inválido. Use no máximo 150 caracteres")

    if "\n" in endereco or "\r" in endereco or "\t" in endereco:
        raise ValueError("Endereço não pode conter tabulação nem quebra de linha")

    if not endereco[0].isalnum() or not endereco[-1].isalnum():
        raise ValueError(
            "Endereço inválido. Deve começar e terminar com letra ou número"
        )

    if not any(c.isalpha() for c in endereco):
        raise ValueError("Endereço inválido. Deve conter pelo menos uma letra")

    if "  " in endereco:
        raise ValueError("Endereço inválido. Não use dois espaços seguidos")

    return endereco

def validar_telefone(telefone: str) -> str:
    telefone = telefone.strip() # validando entrada e removendo espaços em branco

    if not telefone:
        raise ValueError("Telefone não pode ser vazio")

    apenas_digitos = re.sub(r"\D", "", telefone)

    if apenas_digitos.startswith("55"):
        apenas_digitos = apenas_digitos[2:]

    if len(apenas_digitos) not in (10, 11):
        raise ValueError(
            "Telefone inválido. Use DDD + número (fixo com 8 dígitos ou celular com 9)"
        )

    ddd = apenas_digitos[:2]
    numero = apenas_digitos[2:]

    if ddd[0] == "0" or ddd == "00":
        raise ValueError("Telefone inválido. DDD inválido.")

    if len(numero) == 9:
        if numero[0] != "9":
            raise ValueError(
                "Telefone inválido. Celular deve ter nove dígitos após o DDD e começar com 9"
            )

    dd_formatado = f"({ddd})"
    if len(numero) == 8:
        return f"{dd_formatado} {numero[:4]}-{numero[4:]}"

    return f"{dd_formatado} {numero[:5]}-{numero[5:]}"