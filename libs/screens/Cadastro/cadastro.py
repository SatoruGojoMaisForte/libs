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

        # Check if the name exists in the database
        response = requests.get(f"https://api-email-evhk.onrender.com/check-email?email={email_enviar}")
        data = response.json()

        if data['existir']:
             return True
        else:
             return False

    def verificar_nome(self):
        nome = self.ids.nome.text

        # Check if the name exists in the database
        response = requests.get(f"https://api-name.onrender.com/check-name?name={nome}")
        data = response.json()

        if data['exists']:
            return True
        else:
            return False

    def adicionar_usuario(self):
        result_queue = queue.Queue()
        server = threading.Thread(target=self.adicionar_usuario_thread, args=(result_queue,))
        server.start()
        return result_queue.get()

    def adicionar_usuario_thread(self, result_queue):
        url = f'https://api-add-user.onrender.com/add-user?nome={self.ids.nome.text}&email={self.ids.email.text}&senha={self.ids.senha.text}'
        response = requests.post(url)
        data = response.json()

        if data['message'] == 'O usuario foi adicionado com sucesso':
            result_queue.put(True)
        else:
            result_queue.put(False)

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
                self.ids.erro_nome.text = 'Usuario já cadstrado'
                self.ids.erro_nome.text_color = 'red'
                self.ids.erro_nome.pos_hint = {'center_y': 0.63, 'center_x': 1.06}
            else:
                self.ids.erro_nome.text = ''
                email = self.verificar_formato(email=self.ids.email.text)

                if not email:
                    self.ids.erro_email.text = 'Formato de email invalido'
                    self.ids.erro_email.text_color = 'red'
                    self.ids.erro_email.pos_hint = {'center_y': 0.48, 'center_x': 0.99}
                else:
                    self.ids.erro_email.text = ''
                    email_verificado = self.verificar_email(self.ids.email.text)
                    if email_verificado:
                        self.ids.erro_email.text = 'Email ja cadastrado'
                        self.ids.erro_email.text_color = 'red'
                        self.ids.erro_email.pos_hint = {'center_y': 0.48, 'center_x': 1.09}
                    else:
                        self.ids.erro_email.text = ''
                        print(len(self.ids.senha.text))
                        if len(self.ids.senha.text) < 6:
                            self.ids.erro_senha.text = 'O tamanho da senha deve ser superior a 6'
                            self.ids.erro_senha.text_color = 'red'
                            self.ids.erro_senha.pos_hint= {'center_y': 0.33, 'center_x': 0.75}
                        else:
                            adicionar = self.adicionar_usuario()
                            if adicionar == True:
                                print('adicionedo com sucesso')
