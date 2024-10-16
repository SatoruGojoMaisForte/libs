from kivy.network.urlrequest import UrlRequest
from queue import Queue
import re
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar
from kivymd.material_resources import dp

class Cadastro(MDScreen):
    cadastrar = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result_queue = Queue()

    def sneck(self):
        MDSnackbar(
            MDSnackbarText(
                text="Usuário cadastrado",
            ),
            y=dp(30),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()

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
        if not data['exists']:
            self.ids.erro_nome.text = ''
            self.verificar_email(self.ids.email.text)

        else:
            self.ids.erro_nome.text = 'Usuário já cadastrado'
            self.ids.erro_nome.text_color = 'red'
            self.verificar_email(self.ids.email.text)
            print(True)

    def verificar_email(self, email):
        if not self.verificar_formato(email):
            self.ids.erro_email.text = 'Formato de email inválido'
            self.ids.erro_email.text_color = 'red'
            return
        url = f"https://api-email-evhk.onrender.com/check-email?email={email}"
        UrlRequest(
            url,
            on_success=self.verificar_email_sucesso,
            on_error=self.api_erro,
            on_failure=self.api_erro,
            method='GET'
        )

    def verificar_email_sucesso(self, req, result):
        data = result
        print(result)
        if data['existir']:
            self.ids.erro_email.text = 'Email já cadastrado'
            self.ids.erro_email.text_color = 'red'
        else:
            self.ids.erro_email.text = ''
            if self.ids.erro_nome.text != 'Usuário já cadastrado':
                self.adicionar_usuario()

    def adicionar_usuario(self):
        url = f'https://api-add-user.onrender.com/add-user?nome={self.ids.nome.text}&email={self.ids.email.text}&senha={self.ids.senha.text}'
        UrlRequest(url, req_body=None, on_success=self.adicionar_usuario_sucesso, on_error=self.api_erro, on_failure=self.api_erro, method='POST')

    def adicionar_usuario_sucesso(self, req, result):
        data = result
        if data['message'] == 'O usuario foi adicionado com sucesso':
            self.sneck()
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
