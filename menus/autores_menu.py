from entidades.autor import Autor
from repositorios.autor_repositorio import AutorRepositorio
from validacoes.validar_autor import validar_nome

repo = AutorRepositorio()


def exibir_menu():
    print("\n=== MENU AUTORES ===")
    print("1 - Criar autor")
    print("2 - Listar autores")
    print("3 - Buscar autor por ID")
    print("4 - Editar autor")
    print("5 - Deletar autor")
    print("0 - Voltar")


def abrir_menu_autores():
    while True:
        exibir_menu()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_autor()

        elif opcao == "2":
            listar_autores()

        elif opcao == "3":
            buscar_autor()

        elif opcao == "4":
            editar_autor()

        elif opcao == "5":
            deletar_autor()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


# criar autor
def criar_autor():
    print("\n--- Criar Autor ---")

    nome = ler_campo_validado(
        "Nome do autor: ",
        validar_nome
    )

    autor = Autor(nome=nome)

    try:
        repo.criar(autor)

        print(
            "✅ Autor criado com sucesso:",
            autor
        )

    except Exception as e:
        print(
            "❌ Erro ao criar autor:",
            e
        )


# listar autores
def listar_autores():
    print("\n--- Lista de Autores ---")

    autores = repo.listar()

    if not autores:
        print("Nenhum autor encontrado.")
        return

    for autor in autores:
        print(autor)


# buscar autor
def buscar_autor():
    print("\n--- Buscar Autor ---")

    try:
        id_autor = int(input("ID do autor: "))

        autor = repo.buscar_por_id(id_autor)

        if autor:
            print("🔍 Autor encontrado:", autor)

        else:
            print("Autor não encontrado.")

    except ValueError:
        print("ID inválido.")


# editar autor
def editar_autor():
    print("\n--- Editar Autor ---")

    try:
        id_autor = int(input("ID do autor: "))

    except ValueError:
        print("ID inválido.")
        return

    autor = repo.buscar_por_id(id_autor)

    if not autor:
        print("Autor não encontrado.")
        return

    novo_nome = ler_campo_validado(
        "Novo nome: ",
        validar_nome
    )

    atualizado = repo.atualizar_nome(
        id_autor,
        novo_nome
    )

    if atualizado:
        autor_atualizado = repo.buscar_por_id(
            id_autor
        )

        print(
            "✅ Autor atualizado com sucesso:",
            autor_atualizado
        )

    else:
        print(
            "Não foi possível atualizar o autor."
        )


# deletar autor
def deletar_autor():
    print("\n--- Deletar Autor ---")

    try:
        id_autor = int(input("ID do autor: "))

        confirm = input(
            "Tem certeza? (s/n): "
        ).lower()

        if confirm != "s":
            print("Operação cancelada.")
            return

        repo.deletar(id_autor)

        print("🗑️ Autor deletado.")

    except ValueError:
        print("ID inválido.")


def ler_campo_validado(
    prompt,
    funcao_validacao
):
    while True:
        valor = input(prompt)

        try:
            return funcao_validacao(valor)

        except ValueError as e:
            print(f"❌ {e}. Tente novamente.")