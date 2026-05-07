from entidades.livros import Livro
from repositorios.livros_repositorio import LivrosRepositorio
from validacoes.validar_livros import validar_nome_livro

repo = LivrosRepositorio()


def exibir_menu():
    print("\n=== MENU LIVROS ===")
    print("1 - Criar livro")
    print("2 - Listar livros")
    print("3 - Buscar livro por ID")
    print("4 - Editar livro")
    print("5 - Deletar livro")
    print("0 - Voltar")


def abrir_menu_livros():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_livro()
        elif opcao == "2":
            listar_livros()
        elif opcao == "3":
            buscar_livro()
        elif opcao == "4":
            editar_livro()
        elif opcao == "5":
            deletar_livro()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def criar_livro():
    print("\n--- Criar Livro ---")

    nome_livro = ler_campo_validado(
        "Nome do livro: ",
        validar_nome_livro
    )

    try:
        id_editora = int(input("ID da editora: "))
    except ValueError:
        print("ID da editora inválido.")
        return

    livro = Livro(
        nome_livro=nome_livro,
        id_editora=id_editora
    )

    try:
        repo.criar(livro)
        print("✅ Livro criado com sucesso:", livro)
    except Exception as e:
        print("❌ Erro ao criar livro:", e)


def listar_livros():
    print("\n--- Lista de Livros ---")

    livros = repo.listar()

    if not livros:
        print("Nenhum livro encontrado.")
        return

    for livro in livros:
        print(livro)


def buscar_livro():
    print("\n--- Buscar Livro ---")

    try:
        id_livro = int(input("ID do livro: "))
    except ValueError:
        print("ID inválido.")
        return

    livro = repo.buscar_por_id(id_livro)

    if livro:
        print("📚 Encontrado:", livro)
    else:
        print("Livro não encontrado.")


def editar_livro():
    print("\n--- Editar Livro ---")

    try:
        id_livro = int(input("ID do livro: "))
    except ValueError:
        print("ID inválido.")
        return

    livro = repo.buscar_por_id(id_livro)

    if not livro:
        print("Livro não encontrado.")
        return

    while True:
        print("\nO que deseja editar?")
        print("1 - Nome do livro")
        print("2 - ID da editora")
        print("0 - Cancelar")

        opcao = input("Escolha uma opção: ")

        mapa_campos = {
            "1": "nome_livro",
            "2": "id_editora"
        }

        if opcao == "0":
            print("Edição cancelada.")
            return

        campo = mapa_campos.get(opcao)

        if not campo:
            print("Opção inválida.")
            continue

        if campo == "nome_livro":
            novo_valor = ler_campo_validado(
                "Novo nome do livro: ",
                validar_nome_livro
            )

        else:
            try:
                novo_valor = int(input("Novo ID da editora: "))
            except ValueError:
                print("ID inválido.")
                return

        atualizado = repo.atualizar_campo(
            id_livro,
            campo,
            novo_valor
        )

        if atualizado:
            livro_atualizado = repo.buscar_por_id(id_livro)
            print("✅ Livro atualizado:", livro_atualizado)
        else:
            print("Não foi possível atualizar o livro.")

        return


def deletar_livro():
    print("\n--- Deletar Livro ---")

    try:
        id_livro = int(input("ID do livro: "))
    except ValueError:
        print("ID inválido.")
        return

    confirm = input("Tem certeza? (s/n): ").lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    deletado = repo.deletar(id_livro)

    if deletado:
        print("🗑️ Livro deletado.")
    else:
        print("Livro não encontrado.")


def ler_campo_validado(prompt, funcao_validacao):
    while True:
        valor = input(prompt)

        try:
            return funcao_validacao(valor)
        except ValueError as e:
            print(f"❌ {e}. Tente novamente.")