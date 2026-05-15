from datetime import datetime


def validar_id_usuario(id_usuario):
    """Valida se o ID do usuário é válido"""
    try:
        id_int = int(id_usuario)
        if id_int <= 0:
            return False, "ID do usuário deve ser um número positivo"
        return True, ""
    except ValueError:
        return False, "ID do usuário deve ser um número inteiro"


def validar_id_livro(id_livro):
    """Valida se o ID do livro é válido"""
    try:
        id_int = int(id_livro)
        if id_int <= 0:
            return False, "ID do livro deve ser um número positivo"
        return True, ""
    except ValueError:
        return False, "ID do livro deve ser um número inteiro"


def validar_data_emprestimo(data_str):
    """Valida a data de empréstimo (formato: DD/MM/YYYY ou DD/MM/YYYY HH:MM)"""
    try:
        # Tenta diferentes formatos
        for fmt in ["%d/%m/%Y %H:%M", "%d/%m/%Y"]:
            try:
                data = datetime.strptime(data_str.strip(), fmt)
                
                # Verifica se a data não é futura
                if data > datetime.now():
                    return False, "Data de empréstimo não pode ser futura"
                
                return True, ""
            except ValueError:
                continue
        
        return False, "Formato de data inválido. Use DD/MM/YYYY ou DD/MM/YYYY HH:MM"
    except Exception as e:
        return False, f"Erro ao validar data: {str(e)}"


def validar_emprestimo(id_usuario, id_livro, data_emprestimo):
    """Valida todos os campos do empréstimo"""
    
    # Valida ID do usuário
    valido, msg = validar_id_usuario(id_usuario)
    if not valido:
        return False, msg
    
    # Valida ID do livro
    valido, msg = validar_id_livro(id_livro)
    if not valido:
        return False, msg
    
    # Valida data de empréstimo
    valido, msg = validar_data_emprestimo(data_emprestimo)
    if not valido:
        return False, msg
    
    return True, ""
