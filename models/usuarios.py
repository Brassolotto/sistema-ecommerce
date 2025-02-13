from datetime import datetime
import json
import os
from hashlib import sha256

class GestaUsuarios:
    def __init__(self):
        self.arquivo_dados = os.path.join('data', 'usuarios.json')
        self.usuarios = {}
        self.proximo_id = 1
        self.arquivo_dados = os.path.join('data', 'usuarios.json')
        self.carregar_usuarios()

    def salvar_usuarios(self):
        with open(self.arquivo_dados, 'w') as arquivo:
            json.dump({
                'usuarios': self.usuarios,
                'proximo_id': self.proximo_id
            }, arquivo, indent=4)

    def carregar_usuarios(self):
        try:

            os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)

            if not os.path.exists(self.arquivo_dados) or os.path.getsize(self.arquivo_dados) == 0:
                self.usuarios = {}
                self.proximo_id = 1
                self.salvar_usuarios()
                return

            with open(self.arquivo_dados, 'r') as arquivo:
                dados = json.load(arquivo)
                self.usuarios = dados['usuarios']
                self.proximo_id = dados['proximo_id']
        except json.JSONDecodeError:
            print("Arquivo de dados corrompido. Iniciando com dados vazios.")
            self.usuarios = {}
            self.proximo_id = 1
            self.salvar_usuarios()

    def _criptografar_senha(self, senha):
        return sha256(senha.encode()).hexdigest()
    
    def cadastrar_usuario(self, nome, email, senha, tipo='cliente'):
        if not nome or not email or not senha:
            return False, "Todos os campos são obrigatórios"
        
        #verificar se o e-mail já existe
        for usuario in self.usuarios.values():
            if usuario['email'] == email:
                return False, "Email já cadastrado"
            
        usuario = {
            'id': self.proximo_id,
            'nome': nome.strip(),
            'email': email.lower().strip(),
            'senha': self._criptografar_senha(senha),
            'tipo': tipo.strip().lower(),
            'enderecos': [],
            'data_cadastro': datetime.now().strftime('%d/%m/%Y %H:%M')
        }

        self.usuarios[str(self.proximo_id)] = usuario
        self.proximo_id += 1
        self.salvar_usuarios()
        return True, "Usuário cadastrado com sucesso!"
    
    def login(self, email, senha):
        senha_cripto = self._criptografar_senha(senha)
        for usuario in self.usuarios.values():
            if usuario['email'] == email and usuario['senha'] == senha_cripto:
                return True, usuario
            
        return False, "Email ou senha inválidos"
    
    def adicionar_endereco(self, usuario_id, endereco):
        usuario_id = str(usuario_id)
        if usuario_id not in self.usuarios:
            return False, "Usuário não encontrado"
        
        self.usuarios[usuario_id]['enderecos'].append(endereco)
        self.salvar_usuarios()
        return True, "Endereço adicionado com sucesso!"
    
    def listar_usuarios(self, apenas_clientes=True):
        if not self.usuarios:
            return "Nenhum usuário cadastrado."
        
        lista = []
        for usuario in self.usuarios.values():
            if apenas_clientes and usuario['tipo'] != 'cliente':
                continue

            lista.append(f"""
ID: {usuario['id']}
Nome: {usuario['nome']}
Email: {usuario['email']}
Tipo: {usuario['tipo']}
Endereços: {usuario['enderecos']}
Data cadastro: {usuario['data_cadastro']}
{'-' * 30}""")
        return '\n'.join(lista)
        
    def buscar_usuario(self, id):
        id = str(id)
        return self.usuarios.get(id, None)
    
    def atualizar_usuario(self, id, **kwargs):
        id = str(id)
        if id not in self.usuarios:
            return False, "Usuário não encontrado"
            
        campos_permitidos = {'nome', 'email', 'tipo'}

        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                continue

            if campo == 'email':
                for uid, usuario in self.usuarios.items():
                    if uid != id and usuario['email'] == valor:
                        return False, "Email já cadastrado"
                        
                self.usuarios[id][campo] = valor

            self.salvar_usuarios()
            return True, "Usuário atualizado com sucesso!"
        
    def remover_usuario(self, id):
        id = str(id)
        if id not in self.usuarios:
            return False, "Usuário não encontrado"
            
        del self.usuarios[id]
        self.salvar_usuarios()
        return True, "Usuário removido com sucesso!"
            