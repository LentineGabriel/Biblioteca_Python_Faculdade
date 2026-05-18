from repositorios.estante_repositorio import EstanteRepositorio
from repositorios.usuarios_repositorio import UsuariosRepositorio
from repositorios.livros_repositorio import LivrosRepositorio

estante_repo = EstanteRepositorio()
usuario_repo = UsuariosRepositorio()
livro_repo = LivrosRepositorio()

usuario_ativo = None  # Guarda o usuário ativo na sessão do menu da estante

def exibir_menu():
    nome_usuario = usuario_ativo.nome if usuario_ativo else "Nenhum selecionado"
    print(f"\n=== ESTANTE PESSOAL (Usuário: {nome_usuario}) ===")
    print("1 - Escolher/Mudar usuário ativo")
    print("2 - Ver meus livros (Estante)")
    print("3 - Adicionar ou Atualizar status de um livro")
    print("4 - Remover livro da estante")
    print("0 - Voltar")

def abrir_menu_estante():
    global usuario_ativo
    
    # Se ainda não há usuário ativo, força a seleção na primeira vez
    if not usuario_ativo:
        print("\nPara acessar a Estante Pessoal, você precisa selecionar um usuário ativo primeiro.")
        selecionar_usuario_ativo()
        if not usuario_ativo:
            print("Nenhum usuário ativo selecionado. Voltando...")
            return

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            selecionar_usuario_ativo()
        elif opcao == "2":
            if verificar_usuario_ativo():
                listar_estante()
        elif opcao == "3":
            if verificar_usuario_ativo():
                adicionar_ou_atualizar_livro()
        elif opcao == "4":
            if verificar_usuario_ativo():
                remover_livro()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def verificar_usuario_ativo():
    if not usuario_ativo:
        print("❌ Nenhum usuário ativo selecionado. Por favor, escolha a opção 1.")
        return False
    return True

def selecionar_usuario_ativo():
    global usuario_ativo
    print("\n--- Selecionar Usuário Ativo ---")
    usuarios = usuario_repo.listar()
    
    if not usuarios:
        print("❌ Nenhum usuário cadastrado no sistema! Cadastre um usuário primeiro no menu 'Usuários'.")
        usuario_ativo = None
        return
        
    print("\nUsuários cadastrados:")
    for u in usuarios:
        print(f"ID: {u.id_usuario} | Nome: {u.nome} | Email: {u.email}")
        
    try:
        id_usuario = int(input("\nDigite o ID do usuário que deseja usar: "))
        usuario = usuario_repo.buscar_por_id(id_usuario)
        if usuario:
            usuario_ativo = usuario
            print(f"✅ Usuário ativo alterado para: {usuario_ativo.nome}")
        else:
            print("❌ Usuário não encontrado.")
    except ValueError:
        print("❌ ID inválido.")

def formatar_data(data):
    if not data:
        return "N/A"
    if hasattr(data, "strftime"):
        return data.strftime("%d/%m/%Y")
    try:
        partes = str(data).split(" ")[0].split("-")
        if len(partes) == 3:
            return f"{partes[2]}/{partes[1]}/{partes[0]}"
    except Exception:
        pass
    return str(data)

def listar_estante():
    print(f"\n--- Estante de {usuario_ativo.nome} ---")
    itens = estante_repo.listar_por_usuario(usuario_ativo.id_usuario)
    
    if not itens:
        print("Sua estante está vazia. Que tal adicionar alguns livros?")
        return
        
    # Organizando por status
    lendo = [i for i in itens if i.status == 'lendo']
    quero_ler = [i for i in itens if i.status == 'quero ler']
    lidos = [i for i in itens if i.status == 'lido']
    
    if lendo:
        print("\n📖 LENDO:")
        for item in lendo:
            data_str = formatar_data(item.data_atualizacao)
            print(f"  - ID Livro: {item.id_livro} | {item.nome_livro} (Atualizado em: {data_str})")
            
    if quero_ler:
        print("\n📌 QUERO LER:")
        for item in quero_ler:
            data_str = formatar_data(item.data_atualizacao)
            print(f"  - ID Livro: {item.id_livro} | {item.nome_livro} (Atualizado em: {data_str})")
            
    if lidos:
        print("\n✅ LIDOS:")
        for item in lidos:
            data_str = formatar_data(item.data_atualizacao)
            print(f"  - ID Livro: {item.id_livro} | {item.nome_livro} (Atualizado em: {data_str})")

def adicionar_ou_atualizar_livro():
    print("\n--- Adicionar/Atualizar Livro na Estante ---")
    livros = livro_repo.listar()
    
    if not livros:
        print("❌ Nenhum livro cadastrado no sistema! Cadastre livros no menu 'Livros' primeiro.")
        return
        
    print("\nLivros disponíveis:")
    for l in livros:
        print(f"ID: {l.id_livro} | Nome: {l.nome_livro} | Autor: {l.nome_autor or 'Não informado'}")
        
    try:
        id_livro = int(input("\nDigite o ID do livro que deseja adicionar/atualizar: "))
        livro = livro_repo.buscar_por_id(id_livro)
        
        if not livro:
            print("❌ Livro não encontrado.")
            return
            
        print("\nEscolha o status de leitura:")
        print("1 - Quero ler")
        print("2 - Lendo")
        print("3 - Lido")
        print("0 - Cancelar")
        
        opcao_status = input("Escolha uma opção: ")
        
        status_map = {
            "1": "quero ler",
            "2": "lendo",
            "3": "lido"
        }
        
        if opcao_status == "0":
            print("Operação cancelada.")
            return
            
        status = status_map.get(opcao_status)
        if not status:
            print("❌ Opção de status inválida.")
            return
            
        # Adiciona ou atualiza na estante
        resultado = estante_repo.adicionar_ou_atualizar(
            usuario_ativo.id_usuario, 
            id_livro, 
            status
        )
        
        if resultado:
            print(f"✅ Livro '{livro.nome_livro}' marcado como '{status.upper()}' na estante de {usuario_ativo.nome}!")
        else:
            print("❌ Ocorreu um erro ao salvar na estante.")
            
    except ValueError:
        print("❌ ID de livro inválido.")

def remover_livro():
    print("\n--- Remover Livro da Estante ---")
    itens = estante_repo.listar_por_usuario(usuario_ativo.id_usuario)
    
    if not itens:
        print("Sua estante está vazia. Não há nada para remover.")
        return
        
    print("\nSeus Livros na Estante:")
    for item in itens:
        print(f"ID Livro: {item.id_livro} | Nome: {item.nome_livro} | Status atual: {item.status.upper()}")
        
    try:
        id_livro = int(input("\nDigite o ID do livro que deseja remover da estante: "))
        
        # Verifica se o livro está realmente na estante
        pertence = any(item.id_livro == id_livro for item in itens)
        if not pertence:
            print("❌ Este livro não está na sua estante.")
            return
            
        confirmacao = input(f"Tem certeza que deseja remover o livro da estante de {usuario_ativo.nome}? (s/n): ").lower()
        if confirmacao != 's':
            print("Operação cancelada.")
            return
            
        removido = estante_repo.remover(usuario_ativo.id_usuario, id_livro)
        if removido:
            print("✅ Livro removido com sucesso da sua estante!")
        else:
            print("❌ Erro ao remover livro da estante.")
            
    except ValueError:
        print("❌ ID inválido.")
