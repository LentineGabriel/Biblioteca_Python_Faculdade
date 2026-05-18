from menus.usuarios_menu import abrir_menu_usuarios
from menus.autores_menu import abrir_menu_autores
from menus.editoras_menu import abrir_menu_editoras
from menus.livros_menu import abrir_menu_livros
from menus.estante_menu import abrir_menu_estante

def exibir_menu():
    print("\n=== ESTANTE VIRTUAL ===")
    print("1 - Usuários")
    print("2 - Livros")
    print("3 - Autores")
    print("4 - Editoras")
    print("5 - Minha Estante (Controle de Leitura)")
    print("0 - Sair")

def abrir_menu_principal():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            abrir_menu_usuarios()
        elif opcao == "2":
            abrir_menu_livros()
        elif opcao == "3":
            abrir_menu_autores()
        elif opcao == "4":
            abrir_menu_editoras()
        elif opcao == "5":
            abrir_menu_estante()
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")