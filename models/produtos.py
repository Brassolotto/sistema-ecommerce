from datetime import datetime
import json
import os

class GestaProdutos:
    def __init__(self):
        self.arquivo_dados = os.path.join('data', 'produtos.json')
        self.produtos = {}
        self.proximo_id = 1
        self.carregar_produtos()

    def carregar_produtos(self):
        try:

            os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)

            if not os.path.exists(self.arquivo_dados) or os.path.getsize(self.arquivo_dados) == 0:
                self.produtos = {}
                self.proximo_id = 1
                self.salvar_produtos()
                return

            with open('produtos.json', 'r') as arquivo:
                dados = json.load(arquivo)
                self.produtos = dados['produtos']
                self.proximo_id = dados['proximo_id']
        except json.JSONDecodeError:
            print("Arquivo de produtos corrompido. Iniciando com dados vazios.")
            self.produtos = {}
            self.proximo_id = 1
            self.salvar_produtos()

    def salvar_produtos(self):
        with open('produtos.json', 'w') as arquivo:
            json.dump({
                'produtos': self.produtos,
                'proximo_id': self.proximo_id
            }, arquivo, indent=4)

    def adicionar_produto(self, nome, preco, categoria, estoque, descricao):
        if not nome or not preco or not categoria:
            return False, 'Campos obrigatórios: nome, preço e categoria'
        try:
            preco = float(preco)
            estoque = int(estoque)
        except ValueError:
            return False, 'Preço e estoque devem ser números'
        
        produto = {
            'id': self.proximo_id,
            'nome': nome.strip(),
            'preco': preco,
            'categoria': categoria.strip(),
            'estoque': estoque,
            'descricao': descricao.strip(),
            'data_cadastro': datetime.now().strftime('%d/%m/%Y %H:%M')
        }

        self.produtos[str(self.proximo_id)] = produto
        self.proximo_id += 1
        self.salvar_produtos()
        return True, 'Produto adicionado com sucesso!'
    
    def listar_produtos(self):
        if not self.produtos:
            return 'Nenhum produto cadastrado.'
        
        lista = []
        for produto in self.produtos.values():
            lista.append(f"""
ID: {produto['id']}
Nome: {produto['nome']}
Preço: {produto['preco']:.2f}
Categoria: {produto['categoria']}
Estoque: {produto['estoque']}
Descrição: {produto['descricao']}
Data Cadastro: {produto['data_cadastro']}
{'-' * 30}""")
        return '\n'.join(lista)

    def buscar_produto(self, id):
        id = str(id)
        produto = self.produtos.get(id, None)
        if produto:
            return produto
        else:
            return None

    def atualizar_produto(self, id, **kwargs):
        id = str(id)
        if id not in self.produtos:
            return False, "Produto não encontrado"
        
        campos_permitidos = {'nome', 'preco', 'categoria', 'estoque', 'descricao'}
        
        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                continue
                
            if campo in ['preco', 'estoque']:
                try:
                    valor = float(valor) if campo == 'preco' else int(valor)
                except ValueError:
                    return False, f"{campo} deve ser um número"
                    
            self.produtos[id][campo] = valor
        
        self.salvar_produtos()
        return True, "Produto atualizado com sucesso!"


    def remover_produto(self, id):
        id = str(id)
        if id not in self.produtos:
            return False, "Produto não encontrado"
        
        del self.produtos[id]
        self.salvar_produtos()
        return True, "Produto removido com sucesso!"