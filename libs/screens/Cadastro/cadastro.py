from kivy.network.urlrequest import UrlRequest
import re
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar, MDSnackbarCloseButton
from kivymd.material_resources import dp


class Cadastro(MDScreen):
    cadastrar = False
    email = False

    def login(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Login'

    def verificar_formato(self, email: str) -> bool:
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(regex, email))

    def verificar_nome(self):
        nome = self.ids.nome.text
        url = f"https://api-name.onrender.com/check-name?name={nome}"
        UrlRequest(
            url,
            on_success=self.verificar_nome_sucesso,
            on_error=self.api_erro,
            on_failure=self.api_erro,
            method='GET'
        )

    def verificar_nome_sucesso(self, req, result):
        data = result
        print(f'response nome: {data}')
        if not data['exists']:
            self.ids.erro_nome.text = ''
            self.verificar_email(self.ids.email.text)
            self.email = True

        else:
            self.ids.erro_nome.text = 'Usuário já cadastrado'
            self.ids.erro_nome.text_color = 'red'
            self.verificar_email(self.ids.email.text)
            self.email = False
            self.ids.carregando.size_hint = (0.00001, 0.00001)
            self.ids.carregando.pos_hint = {"center_y": 0.91, "center_x": 1.05}

    def verificar_email(self, email):
        if not self.verificar_formato(email):
            self.ids.erro_email.text = 'Formato de email inválido'
            self.ids.erro_email.text_color = 'red'
            self.ids.carregando.size_hint = (0.00001, 0.00001)
            self.ids.carregando.pos_hint = {"center_y": 0.91, "center_x": 1.05}
            return
        url = f"https://api-email-2gyg.onrender.com/check-email?email={email}"
        UrlRequest(
            url,
            on_success=self.verificar_email_sucesso,
            on_error=self.api_erro,
            on_failure=self.api_erro,
            method='GET'
        )

    def verificar_email_sucesso(self, req, result):
        data = result
        print(f"response email: {result}")
        if data['existir']:
            self.ids.erro_email.text = 'Email já cadastrado'
            self.ids.erro_email.text_color = 'red'
            self.ids.carregando.size_hint = (0.00001, 0.00001)
            self.ids.carregando.pos_hint = {"center_y": 0.91, "center_x": 1.05}
        else:
            self.ids.erro_email.text = ''
            print(f"pode adicionar usuario: {self.email}")
            if self.email:
                self.adicionar_usuario()
            else:
                pass

    def adicionar_usuario(self):
        url = f'https://api-add-user.onrender.com/add-user?nome={self.ids.nome.text}&email={self.ids.email.text}&senha={self.ids.senha.text}'
        UrlRequest(url, req_body=None, on_success=self.adicionar_usuario_sucesso, on_error=self.api_erro, on_failure=self.api_erro, method='POST')

    def adicionar_usuario_sucesso(self, req, result):
        data = result
        print(f'response adicionar_usuario: {data}')
        if data['message'] == 'O usuario foi adicionado com sucesso':
            self.sneck()
            self.ids.nome.text = ''
            self.ids.email.text = ''
            self.ids.senha.text = ''
        else:
            print('Falha ao adicionar o usuário')

    def api_erro(self, req, error):
        pass

    def logica(self):
        nome = self.ids.nome.text
        email = self.ids.email.text
        senha = self.ids.senha.text

        # Verificação inicial dos campos
        if nome == '':
            self.ids.nome.focus = True
            return
        elif email == '' and nome != '':
            self.ids.email.focus = True
            return
        elif senha == '' and nome != '' and email != '':
            self.ids.senha.focus = True
            return

        # Iniciar verificações de nome e email
        self.verificar_nome()
        self.ids.carregando.size_hint = (1, 1)
        self.ids.carregando.pos_hint = {"center_y": 0.5, "center_x": 0.5}

