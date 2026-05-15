from datetime import datetime
from entidades.emprestimos import Emprestimo
from repositorios.emprestimos_repositorio import EmprestimosRepositorio
from repositorios.usuarios_repositorio import UsuariosRepositorio
from repositorios.livros_repositorio import LivrosRepositorio
from validacoes.validar_emprestimos import validar_emprestimo

repo = EmprestimosRepositorio()
usuarios_repo = UsuariosRepositorio()
livros_repo = LivrosRepositorio()


def exibir_menu():
    print("\n=== MENU EMPRÉSTIMOS ===")
    print("1 - Criar empréstimo")
    print("2 - Listar empréstimos")
    print("3 - Listar empréstimos ativos")
    print("4 - Buscar empréstimo por ID")
    print("5 - Registrar devolução")
    print("6 - Marcar como atrasado")
    print("7 - Deletar empréstimo")
    print("0 - Voltar")


def abrir_menu_emprestimos():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_emprestimo()
        elif opcao == "2":
            listar_emprestimos()
        elif opcao == "3":
            listar_emprestimos_ativos()
        elif opcao == "4":
            buscar_emprestimo()
        elif opcao == "5":
            registrar_devolucao()
        elif opcao == "6":
            marcar_como_atrasado()
        elif opcao == "7":
            deletar_emprestimo()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def criar_emprestimo():
    print("\n--- Criar Empréstimo ---")

    # Solicitar ID do usuário
    try:
        id_usuario = int(input("ID do usuário: "))
    except ValueError:
        print("❌ ID do usuário inválido.")
        return

    # Verificar se o usuário existe
    usuario = usuarios_repo.buscar_por_id(id_usuario)
    if not usuario:
        print("❌ Usuário não encontrado.")
        return

    # Solicitar ID do livro
    try:
        id_livro = int(input("ID do livro: "))
    except ValueError:
        print("❌ ID do livro inválido.")
        return

    # Verificar se o livro existe
    livro = livros_repo.buscar_por_id(id_livro)
    if not livro:
        print("❌ Livro não encontrado.")
        return

    # Solicitar data de empréstimo
    data_atual = datetime.now()
    sugestao = data_atual.strftime("%d/%m/%Y %H:%M")
    print(f"Data de empréstimo (Padrão: {sugestao}):")
    print("Digite a data em DD/MM/YYYY ou DD/MM/YYYY HH:MM, ou deixe em branco para usar agora:")
    data_str = input("Data: ").strip()

    # Se deixado em branco, usar data/hora atual
    if not data_str:
        data_emprestimo = data_atual
    else:
        # Validar empréstimo
        valido, msg = validar_emprestimo(id_usuario, id_livro, data_str)
        if not valido:
            print(f"❌ {msg}")
            return

        # Converter string para datetime
        try:
            data_emprestimo = None
            # Tenta primeiro com hora e minuto
            try:
                data_emprestimo = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
            except ValueError:
                # Se não tiver hora, tenta só a data
                try:
                    data_emprestimo = datetime.strptime(data_str, "%d/%m/%Y")
                    # Se inseriu só a data, completa com a hora atual
                    hora_agora = datetime.now().time()
                    data_emprestimo = datetime.combine(data_emprestimo.date(), hora_agora)
                except ValueError:
                    print(f"❌ Formato de data inválido")
                    return
        except Exception as e:
            print(f"❌ Erro ao processar data: {e}")
            return

    # Criar empréstimo
    emprestimo = Emprestimo(
        id_usuario=id_usuario,
        id_livro=id_livro,
        data_emprestimo=data_emprestimo,
        nome_usuario=usuario.nome,
        nome_livro=livro.nome_livro,
    )

    try:
        repo.criar(emprestimo)
        print("✅ Empréstimo criado com sucesso:")
        print(emprestimo)
        print(f"📌 Prazo de devolução: {emprestimo.data_prazo.strftime('%d/%m/%Y %H:%M')}")
    except Exception as e:
        print("❌ Erro ao criar empréstimo:", e)


def listar_emprestimos():
    print("\n--- Lista de Empréstimos ---")

    emprestimos = repo.listar()

    if not emprestimos:
        print("Nenhum empréstimo encontrado.")
        return

    for emprestimo in emprestimos:
        print(emprestimo)


def listar_emprestimos_ativos():
    print("\n--- Empréstimos Ativos ---")

    emprestimos = repo.listar_emprestimos_ativos()

    if not emprestimos:
        print("Nenhum empréstimo ativo.")
        return

    for emprestimo in emprestimos:
        print(emprestimo)


def buscar_emprestimo():
    print("\n--- Buscar Empréstimo ---")

    try:
        id_emprestimo = int(input("ID do empréstimo: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    emprestimo = repo.buscar_por_id(id_emprestimo)

    if emprestimo:
        print("📌 Encontrado:", emprestimo)
    else:
        print("❌ Empréstimo não encontrado.")


def registrar_devolucao():
    print("\n--- Registrar Devolução ---")

    try:
        id_emprestimo = int(input("ID do empréstimo: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    # Buscar empréstimo
    emprestimo = repo.buscar_por_id(id_emprestimo)
    if not emprestimo:
        print("❌ Empréstimo não encontrado.")
        return

    if emprestimo.status == "devolvido":
        print("⚠️ Este empréstimo já foi devolvido.")
        return

    confirm = input("Confirmar devolução? (s/n): ").lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    try:
        repo.registrar_devolucao(id_emprestimo)
        print("✅ Devolução registrada com sucesso.")
    except Exception as e:
        print("❌ Erro ao registrar devolução:", e)


def marcar_como_atrasado():
    print("\n--- Marcar como Atrasado ---")

    try:
        id_emprestimo = int(input("ID do empréstimo: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    # Buscar empréstimo
    emprestimo = repo.buscar_por_id(id_emprestimo)
    if not emprestimo:
        print("❌ Empréstimo não encontrado.")
        return

    if emprestimo.status != "emprestado":
        print("⚠️ Apenas empréstimos ativos podem ser marcados como atrasados.")
        return

    confirm = input("Confirmar marcação como atrasado? (s/n): ").lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    try:
        repo.marcar_como_atrasado(id_emprestimo)
        print("✅ Empréstimo marcado como atrasado.")
    except Exception as e:
        print("❌ Erro ao marcar como atrasado:", e)


def deletar_emprestimo():
    print("\n--- Deletar Empréstimo ---")

    try:
        id_emprestimo = int(input("ID do empréstimo: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    # Buscar empréstimo
    emprestimo = repo.buscar_por_id(id_emprestimo)
    if not emprestimo:
        print("❌ Empréstimo não encontrado.")
        return

    confirm = input("Tem certeza? (s/n): ").lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    try:
        repo.deletar(id_emprestimo)
        print("🗑️ Empréstimo deletado.")
    except Exception as e:
        print("❌ Erro ao deletar empréstimo:", e)
