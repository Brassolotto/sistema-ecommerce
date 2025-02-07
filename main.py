from models.produtos import GestaProdutos

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
    #gestao_usuarios = GestaUsuarios()
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