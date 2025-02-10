from models.produtos import GestaProdutos
from models.usuarios import GestaUsuarios
from models.pedidos import GestaPedidos

def menu_usuarios(gestao):
    while True:
        print("\n=== Gestão de Usuários ===")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Buscar usuário")
        print("4. Adicionar endereço")
        print("5. Atualizar usuário")
        print("6. Remover usuário")
        print("7. Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            tipo = input("Tipo (cliente/admin) [cliente]: ") or 'cliente'

            sucesso, mensagem = gestao.cadastrar_usuario(nome, email, senha, tipo)
            print(f"\n{mensagem}")

        elif opcao == "2":
            print(gestao.listar_usuarios())

        elif opcao == "3":
            id = input("ID do usuário: ")
            usuario = gestao.buscar_usuario(id)
            if usuario:
                print(f"""
ID: {usuario['id']}
Nome: {usuario['nome']}
Email: {usuario['email']}
Tipo: {usuario['tipo']}
Endereços: {len(usuario['enderecos'])}
Data cadastro: {usuario['data_cadastro']}""")
            else:
                print("\nUsuário não encontrado")

        elif opcao == "4":
            id = input("ID do usuário: ")
            print("\nDados do endereço: ")
            rua = input("Rua: ")
            numero = input("Número: ")
            complemento = input("Complemento: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            cep = input("CEP: ")

            endereco = {
                'rua': rua,
                'numero': numero,
                'complemento': complemento,
                'cidade': cidade,
                'estado': estado,
                'cep': cep
            }

            sucesso, mensagem = gestao.adicionar_endereco(id, endereco)
            print(f"\n{mensagem}")

        elif opcao == "5":
            id = input("ID do usuário: ")
            print("\nDeixe em branco para manter o valor atual")
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            tipo = input("Novo tipo (cliente/admin): ")

            atualizacoes = []
            if nome: atualizacoes['nome'] = nome
            if email: atualizacoes['email'] = email
            if tipo: atualizacoes['tipo'] = tipo

            sucesso, mensagem = gestao.atualizar_usuario(id, **atualizacoes)
            print(f"\n{mensagem}")

        elif opcao == "6":
            id = input("ID do usuário: ")
            confirma = input("Tem certeza? (S/N): ").upper()

            if confirma == 'S':
                sucesso, mensagem = gestao.remover_usuario(id)
                print(f"\n{mensagem}")
            else:
                print("\nOperação cancelada")

        elif opcao == "7":
            break
        else:
            print("\nOpção inválida!")

def menu_produtos(gestao):
    while True:
        print("\n=== Gestão de Produtos ===")
        print("1. Adicionar produto")
        print("2. Listar produtos")
        print("3. Buscar produto")
        print("4. Atualizar produto")
        print("5. Remover produto")
        print("6. Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

def main():
    print("=== Sistema de E-commerce ===")
    gestao_produtos = GestaProdutos()
    gestao_usuarios = GestaUsuarios()
    #gestao_pedidos = GestaPedidos()

    while True:
        print("\n1. Gestão de Produtos")
        print("2. Gestão de Usuários")
        print("3. Gestão de Pedidos")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_produtos(gestao_produtos)
        elif opcao == "2":
            print("\nGestão de Usuários em desenvolvimento")
        elif opcao == "3":
            print("\nGestão de Pedidos em desenvolvimento")
        elif opcao == "4":
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()