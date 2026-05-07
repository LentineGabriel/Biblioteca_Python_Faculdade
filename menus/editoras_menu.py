from entidades.editora import Editora
from repositorios.editora_repositorio import EditoraRepositorio
from validacoes.validar_editora import validar_nome

repo = EditoraRepositorio()


def exibir_menu():
    print("\n=== MENU EDITORAS ===")
    print("1 - Criar editora")
    print("2 - Listar editoras")
    print("3 - Buscar editora por ID")
    print("4 - Editar editora")
    print("5 - Deletar editora")
    print("0 - Voltar")


def abrir_menu_editoras():
    while True:
        exibir_menu()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_editora()
        elif opcao == "2":
            listar_editoras()
        elif opcao == "3":
            buscar_editora()
        elif opcao == "4":
            editar_editora()
        elif opcao == "5":
            deletar_editora()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def criar_editora():
    print("\n--- Criar Editora ---")

    nome = ler_campo_validado(
        "Nome da editora: ",
        validar_nome
    )

    editora = Editora(nome=nome)

    try:
        repo.criar(editora)
        print("✅ Editora criada com sucesso:", editora)

    except Exception as e:
        print("❌ Erro ao criar editora:", e)


def listar_editoras():
    print("\n--- Lista de Editoras ---")

    editoras = repo.listar()

    if not editoras:
        print("Nenhuma editora encontrada.")
        return

    for e in editoras:
        print(e)


def buscar_editora():
    print("\n--- Buscar Editora ---")

    try:
        id_editora = int(input("ID da editora: "))
    except ValueError:
        print("ID inválido.")
        return

    editora = repo.buscar_por_id(id_editora)

    if editora:
        print("🔍 Editora encontrada:", editora)
    else:
        print("Editora não encontrada.")


def editar_editora():
    print("\n--- Editar Editora ---")

    try:
        id_editora = int(input("ID da editora: "))
    except ValueError:
        print("ID inválido.")
        return

    editora = repo.buscar_por_id(id_editora)

    if not editora:
        print("Editora não encontrada.")
        return

    novo_nome = ler_campo_validado(
        "Novo nome: ",
        validar_nome
    )

    atualizado = repo.atualizar_nome(id_editora, novo_nome)

    if atualizado:
        editora_atualizada = repo.buscar_por_id(id_editora)
        print("✅ Editora atualizada com sucesso:", editora_atualizada)
    else:
        print("Não foi possível atualizar a editora.")


def deletar_editora():
    print("\n--- Deletar Editora ---")

    try:
        id_editora = int(input("ID da editora: "))

        confirm = input("Tem certeza? (s/n): ").lower()

        if confirm != "s":
            print("Operação cancelada.")
            return

        repo.deletar(id_editora)
        print("🗑️ Editora deletada.")

    except ValueError:
        print("ID inválido.")


def ler_campo_validado(prompt, funcao_validacao):
    while True:
        valor = input(prompt)

        try:
            return funcao_validacao(valor)

        except ValueError as e:
            print(f"❌ {e}. Tente novamente.")
