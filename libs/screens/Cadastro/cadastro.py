import queue
import threading
import requests
from kivymd.uix.screen import MDScreen
import re


class Cadastro(MDScreen):

    def verificar_formato(self, email: str) -> bool:
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    def verificar_email(self, email):
        email_enviar = email
        response = requests.get(f"https://api-email-evhk.onrender.com/check-email?email={email_enviar}")
        data = response.json()
        return data['existir']

    def verificar_nome(self):
        nome = self.ids.nome.text
        response = requests.get(f"https://api-name.onrender.com/check-name?name={nome}")
        data = response.json()
        return data['exists']

    def adicionar_usuario(self):
        # Inicia a thread para adicionar o usuário
        threading.Thread(target=self.adicionar_usuario_thread).start()

    def adicionar_usuario_thread(self):
        url = f'https://api-add-user.onrender.com/add-user?nome={self.ids.nome.text}&email={self.ids.email.text}&senha={self.ids.senha.text}'
        response = requests.post(url)
        data = response.json()

        # Atualiza a UI no thread principal
        self.atualizar_interface(data['message'] == 'O usuario foi adicionado com sucesso')

    def atualizar_interface(self, sucesso):
        # Método chamado no thread principal para atualizar a interface
        if sucesso:
            print('Usuário adicionado com sucesso')
            # Aqui você pode adicionar uma lógica para mudar de tela ou exibir uma mensagem de sucesso
        else:
            print('Falha ao adicionar o usuário')
            # Aqui você pode exibir uma mensagem de erro na UI

    def voltar(self):
        self.manager.current = 'Login'

    def logica(self):
        if self.ids.nome.text == '':
            self.ids.nome.focus = True
            return

        elif self.ids.email.text == '' and self.ids.nome.text != '':
            self.ids.email.focus = True
            return

        elif self.ids.senha.text == '' and self.ids.nome.text != '':
            if self.ids.email.text != '':
                self.ids.senha.focus = True
                return
        else:
            name = self.verificar_nome()
            if name:
                self.ids.erro_nome.text = 'Usuário já cadastrado'
                self.ids.erro_nome.text_color = 'red'
                self.ids.erro_nome.pos_hint = {'center_y': 0.63, 'center_x': 1.06}
            else:
                self.ids.erro_nome.text = ''
                email = self.verificar_formato(email=self.ids.email.text)

                if not email:
                    self.ids.erro_email.text = 'Formato de email inválido'
                    self.ids.erro_email.text_color = 'red'
                else:
                    self.ids.erro_email.text = ''
                    email_verificado = self.verificar_email(self.ids.email.text)
                    if email_verificado:
                        self.ids.erro_email.text = 'Email já cadastrado'
                        self.ids.erro_email.text_color = 'red'
                    else:
                        self.ids.erro_email.text = ''
                        if len(self.ids.senha.text) < 6:
                            self.ids.erro_senha.text = 'O tamanho da senha deve ser superior a 6'
                            self.ids.erro_senha.text_color = 'red'
                        else:
                            self.ids.erro_senha.text = ''
                            self.adicionar_usuario()
