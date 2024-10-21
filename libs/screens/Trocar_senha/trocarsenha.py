import queue
import threading

import requests
from kivymd.uix.screen import MDScreen
from dotenv import load_dotenv
import os

class TrocarSenha(MDScreen):
    def pegar_nome(self, result_queue):
        email = os.getenv('EMAIL_USER')
        response = requests.post(f'https://api-name.onrender.com/name-user?email={email}')
        try:
            data = response.json()
            if data['usuario']:
                result_queue.put(data['message'])
        except:
            result_queue.put(email)


    def nome(self):
        result_queue = queue.Queue()

        # Inicia a thread para verificar o nome
        thread = threading.Thread(target=self.pegar_nome, args=(result_queue,))
        thread.start()
        thread.join()

        # Retorna o resultado da fila
        return f'{result_queue.get()} - Chatto'

    def senha(self):
        result_queue = queue.Queue()

        # Inicia a thread para verificar o nome
        thread = threading.Thread(target=self.pegar_nome, args=(result_queue,))
        thread.start()
        thread.join()

        # Retorna o resultado da fila
        return f'{result_queue.get()} - Chatto'


    def trocar_senha(self, result_queue):
        email = os.getenv('EMAIL_USER')
        senha = self.ids.senha.text
        token = "spike"  # Substitua pelo seu Bearer Token

        # Definindo o cabeçalho com o Bearer Token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Fazendo a requisição PUT com o token e nome
        response = requests.put(
            f'https://api-password.onrender.com/trocar-senha?email={email}&senha={senha}',
            headers=headers)
        try:
            data = response.json()
            if data.get('alterado'):
                result_queue.put('senha alterada')
            else:
                result_queue.put('senha não alterada')

        except Exception as e:
            result_queue.put(f'Erro: {str(e)}')

    def modificar(self, campo):
        if campo == 'confirmar':
            text = self.ids.confirmar.text
            text = str(text).replace(' ', '')
            text = str(text).replace(':', '')
            text = str(text).replace(';', '')
            self.ids.confirmar.text =  text

        else:
            text = self.ids.senha.text
            text = str(text).replace(' ', '')
            text = str(text).replace(':', '')
            text = str(text).replace(';', '')
            self.ids.senha.text = text

    def alterar_senha(self):
        result_queue = queue.Queue()

        # inicia a thread para trocar a senha
        thread = threading.Thread(target=self.trocar_senha, args=(result_queue,))
        thread.start()
        thread.join()
        return result_queue.get()

    def visibilizar_senha1(self):
        visivel = self.ids.senha.password
        if visivel:
            self.ids.senha.password = False
            self.ids.confirmar.password = False
        else:
            self.ids.senha.password = True
            self.ids.confirmar.password = True

    def requisitos(self):
        texto_confirmar = self.ids.confirmar.text
        texto_senha = self.ids.senha.text
        if texto_senha == '':
            self.ids.senha.focus = True
            return
        elif texto_confirmar == '':
            self.ids.confirmar.focus = True
            return
        if texto_senha == texto_confirmar:
            if len(texto_senha) >= 6:
                variavel = self.alterar_senha()
                self.ids.hint.text = 'Confirmar nova palavra-passe'
                print(variavel)
                return
            else:
                self.ids.erro.text = 'Minimo de 6 caracteres'
        else:
            self.ids.erro.text = 'As senhas devem ser iguais'
            return

