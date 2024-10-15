import queue
import threading
import requests
from kivymd.uix.screen import MDScreen
import re
from kivy.clock import Clock


class Cadastro(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_queue = queue.Queue()  # Fila para comunicação entre threads

    # Função pura para verificar o formato de e-mail
    def verificar_formato(self, email: str) -> bool:
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(regex, email))

    # Função pura para enviar a requisição e verificar o e-mail
    def verificar_email(self, email):
        url = f"https://api-email-evhk.onrender.com/check-email?email={email}"
        return requests.get(url).json()['existir']

    # Função pura para verificar o nome
    def verificar_nome(self, nome):
        url = f"https://api-name.onrender.com/check-name?name={nome}"
        return requests.get(url).json()['exists']

    # Thread para adicionar o usuário, mantendo a lógica de requisição pura
    def adicionar_usuario_thread(self):
        url = f'https://api-add-user.onrender.com/add-user?nome={self.ids.nome.text}&email={self.ids.email.text}&senha={self.ids.senha.text}'
        response = requests.post(url)
        data = response.json()
        # Adiciona o resultado na fila para ser processado na UI
        self.api_queue.put(data['message'] == 'O usuario foi adicionado com sucesso')
        Clock.schedule_once(self.processar_fila)

    # Processa a fila no thread principal para atualizar a interface
    def processar_fila(self, dt):
        while not self.api_queue.empty():
            sucesso = self.api_queue.get()
            self.atualizar_interface(sucesso)

    # Atualiza a interface com base no resultado
    def atualizar_interface(self, sucesso):
        if sucesso:
            print('Usuário adicionado com sucesso')
        else:
            print('Falha ao adicionar o usuário')

    # Lógica que pode ser chamada ao adicionar um usuário
    def adicionar_usuario(self):
        threading.Thread(target=self.adicionar_usuario_thread).start()

    # Função para organizar o fluxo de validação e cadastro
    def logica(self):
        nome = self.ids.nome.text
        email = self.ids.email.text
        senha = self.ids.senha.text

        if nome == '':
            self.ids.nome.focus = True
            return
        elif email == '' and nome != '':
            self.ids.email.focus = True
            return
        elif senha == '' and nome != '' and email != '':
            self.ids.senha.focus = True
            return

        if self.verificar_nome(nome):
            self.ids.erro_nome.text = 'Usuário já cadastrado'
            self.ids.erro_nome.text_color = 'red'
        else:
            self.ids.erro_nome.text = ''
            if not self.verificar_formato(email):
                self.ids.erro_email.text = 'Formato de email inválido'
                self.ids.erro_email.text_color = 'red'
            elif self.verificar_email(email):
                self.ids.erro_email.text = 'Email já cadastrado'
                self.ids.erro_email.text_color = 'red'
            else:
                self.ids.erro_email.text = ''
                if len(senha) < 6:
                    self.ids.erro_senha.text = 'O tamanho da senha deve ser superior a 6'
                    self.ids.erro_senha.text_color = 'red'
                else:
                    self.ids.erro_senha.text = ''
                    self.adicionar_usuario()
