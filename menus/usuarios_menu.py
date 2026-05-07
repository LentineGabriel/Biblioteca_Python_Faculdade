from entidades.usuarios import Usuarios
from repositorios.usuarios_repositorio import UsuariosRepositorio
from validacoes.validar_usuarios import validar_nome, validar_email, validar_endereco, validar_telefone

repo = UsuariosRepositorio()

def exibir_menu():
    print("\n=== MENU USUÁRIOS ===")
    print("1 - Criar usuário")
    print("2 - Listar usuários")
    print("3 - Buscar por ID")
    print("4 - Editar usuário")
    print("5 - Deletar usuário")
    print("0 - Voltar")

def abrir_menu_usuarios():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            buscar_usuario()
        elif opcao == "4":
            editar_usuario()
        elif opcao == "5":
            deletar_usuario()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

# criar usuário
def criar_usuario():
    print("\n--- Criar Usuário ---")

    nome_validado = ler_campo_validado("Nome: ", validar_nome)
    email_validado = ler_campo_validado("Email: ", validar_email)
    endereco_validado = ler_campo_validado("Endereço: ", validar_endereco)
    telefone_validado = ler_campo_validado("Telefone: ", validar_telefone)

    usuario = Usuarios(
        nome=nome_validado,
        email=email_validado,
        endereco=endereco_validado,
        telefone=telefone_validado
    )

    try:
        repo.criar(usuario)
        print("✅ Usuário criado com sucesso:", usuario)
    except Exception as e:
        print("❌ Erro ao criar usuário:", e)

# listar usuários
def listar_usuarios():
    print("\n--- Lista de Usuários ---")

    usuarios = repo.listar()

    if not usuarios:
        print("Nenhum usuário encontrado.")
        return

    for u in usuarios:
        print(u)

# buscar usuário por id
def buscar_usuario():
    print("\n--- Buscar Usuário ---")

    try:
        id_usuario = int(input("ID: "))
        usuario = repo.buscar_por_id(id_usuario)

        if usuario:
            print("🔍 Encontrado:", usuario)
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido.")

# editar usuário
def editar_usuario():
    print("\n--- Editar Usuário ---")
    try:
        id_usuario = int(input("ID do usuário que deseja editar: "))
    except ValueError:
        print("ID inválido.")
        return

    usuario = repo.buscar_por_id(id_usuario)
    if not usuario:
        print("Usuário não encontrado.")
        return

    while True:
        print("\nO que você deseja editar?")
        print("1 - Nome")
        print("2 - Email")
        print("3 - Endereço")
        print("4 - Telefone")
        print("0 - Cancelar")

        opcao_campo = input("Escolha uma opção: ")
        mapa_campos = {
            "1": "nome",
            "2": "email",
            "3": "endereco",
            "4": "telefone"
        }

        if opcao_campo == "0":
            print("Edição cancelada.")
            return

        campo = mapa_campos.get(opcao_campo)
        if not campo:
            print("Opção inválida.")
            continue

        validadores = {
            "nome": validar_nome,
            "email": validar_email,
            "endereco": validar_endereco,
            "telefone": validar_telefone
        }

        novo_valor = ler_campo_validado(
            f"Novo valor para {campo}: ",
            validadores[campo]
        )

        atualizado = repo.atualizar_campo(id_usuario, campo, novo_valor)
        if atualizado:
            usuario_atualizado = repo.buscar_por_id(id_usuario)
            print("✅ Usuário atualizado com sucesso:", usuario_atualizado)
        else:
            print("Não foi possível atualizar o usuário.")
        return

# deletar usuário
def deletar_usuario():
    print("\n--- Deletar Usuário ---")

    try:
        id_usuario = int(input("ID: "))

        confirm = input("Tem certeza? (s/n): ").lower()
        if confirm != "s":
            print("Operação cancelada.")
            return

        deletado = repo.deletar(id_usuario)

        if deletado:
            print("🗑️ Usuário deletado.")
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido.")

def ler_campo_validado(prompt, funcao_validacao):
    while True:
        valor = input(prompt)
        try:
            return funcao_validacao(valor)
        except ValueError as e:
            print(f"❌ {e}. Tente novamente.")