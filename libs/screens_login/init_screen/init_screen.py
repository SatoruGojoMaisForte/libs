import bcrypt
from kivy.metrics import dp
from kivy.properties import get_color_from_hex, StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar


class InitScreen(MDScreen):
    carregado = False
    key = StringProperty()
    name = False
    senha = ''
    type = ''

    def on_enter(self, *args):
        pass

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
            self.ids.type.text = 'Contratante'
            self.type = 'Contratante'
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')
            self.ids.type.text = 'Funcionario'
            self.type = 'Functionario'

    def carregar_usuarios(self):
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/.json'
        UrlRequest(
            url,
            method='GET',
            on_success=self.usuarios_carregados,
            on_error=self.error,
            on_failure=self.error
        )

    def error(self, req, error):
        print(error)

    def usuarios_carregados(self, req, result):
        global name
        for cargo, nome in result.items():
            if nome['name'] == str(self.ids.nome.text):
                print('achei')
                self.name = True
                self.senha = nome['senha']

                self.etapa2(self.senha)
            else:
                self.name = False

        if not self.name:
            self.ids.nome_errado.text = 'Pessoa não cadastrado'

    def etapa2(self, hashd_password):
        password_bytes = self.ids.senha.text.encode('utf-8')
        user_password_bytes = hashd_password.encode('utf-8')
        if bcrypt.checkpw(password_bytes, user_password_bytes):
            print('senha correta')
        else:
            print('senha incorreta')
            self.ids.senha_errada.text = 'Senha incorreta'
            self.ids.senha.error = True

    def register(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'ChoiceAccount'

    def go_to_next(self, perfil, name):
        self.manager.transition = SlideTransition(direction='left')
        login = self.manager.get_screen('LoginScreen')
        login.perfil = perfil
        login.nome = name
        self.manager.current = 'LoginScreen'

    def show_message(self, message, color='#2196F3'):
        """Display a snackbar message"""
        MDSnackbar(
            MDSnackbarText(
                text=message,
                theme_text_color='Custom',
                text_color='white',
                bold=True
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            halign='center',
            size_hint_x=0.94,
            theme_bg_color='Custom',
            background_color=get_color_from_hex(color)
        ).open()

    def show_error(self, error_message):
        """Display an error message"""
        self.show_message(error_message, color='#FF0000')
        print(f"Error: {error_message}")

    def etapa1(self):
        if not self.type:
            self.show_error('Selecione o tipo de conta para efetuar o login')
            return

        if self.ids.nome.text == '':
            self.ids.nome.focus = True
            return
        else:

            if self.ids.senha.text == '':
                self.ids.senha.focus = True
                return
            else:
                print('Ambos')
                if self.ids.type.text in 'Contratante':
                    print(self.type)
                    self.verificar_senha()
                else:
                    self.senha_employee()
                    return

    def senha_employee(self):
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/.json'
        UrlRequest(
            url,
            method='GET',
            on_success=self.senhas_employee,
        )

    def senhas_employee(self, req, result):
        senha = self.ids.senha.text
        senha_bytes = senha.encode('utf-8')

        for cargo, nome in result.items():
            if nome['Name'] == self.ids.nome.text:
                self.ids.nome_errado.text = ''
                self.ids.nome.error = False
                senha_correta = nome['password'].encode('utf-8')
                if bcrypt.checkpw(senha_bytes, senha_correta):
                    self.ids.senha.error = False
                    self.ids.senha_errada.text = ''
                    print('senha correta meu nobre')
                    self.key = cargo
                    print(cargo)
                    UrlRequest(
                        url=f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{cargo}/.json',
                        on_success=self.next_perfil_employee
                    )

                else:
                    print('senha está errada seu acefalo burro do caralho')
                    self.ids.senha.error = True
                    self.ids.senha_errada.text = 'A senha inserida está incorreta'
                break
            else:
                self.ids.nome_errado.text = 'Pessoa não cadastrado'
                self.ids.nome.error = True

    def next_perfil_employee(self, instance, result):
        print(result)
        app = MDApp.get_running_app()
        screenmanager = app.root
        perfil = screenmanager.get_screen('PrincipalScreenEmployee')
        perfil.employee_name = result['Name']
        perfil.contractor = result['contractor']
        perfil.employee_function = result['function']
        perfil.employee_mail = result['email']
        perfil.request = eval(result['request'])
        perfil.employee_telephone = result['telefone']
        perfil.avatar = result['avatar']
        perfil.employee_summary = result['sumary']
        perfil.skills = result['skills']
        perfil.key = self.key
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'

    def verificar_senha(self):
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/.json'
        UrlRequest(
            url,
            method='GET',
            on_success=self.senhas,
        )

    def senhas(self, req, result):
        senha = self.ids.senha.text
        senha_bytes = senha.encode('utf-8')

        for cargo, nome in result.items():
            if nome['name'] == self.ids.nome.text:
                self.ids.nome_errado.text = ''
                self.ids.nome.error = False
                senha_correta = nome['senha'].encode('utf-8')
                if bcrypt.checkpw(senha_bytes, senha_correta):
                    self.ids.senha.error = False
                    self.ids.senha_errada.text = ''
                    print('senha correta meu nobre')

                    UrlRequest(
                        url=f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{cargo}/.json',
                        on_success=self.next_perfil
                    )

                else:
                    print('senha está errada seu acefalo burro do caralho')
                    self.ids.senha.error = True
                    self.ids.senha_errada.text = 'A senha inserida está incorreta'
                break
            else:
                self.ids.nome_errado.text = 'Pessoa não cadastrado'
                self.ids.nome.error = True

    def next_perfil(self, instance, result):
        app = MDApp.get_running_app()
        screen_manager = app.root
        perfil = screen_manager.get_screen('Perfil')
        perfil.function = result['function']
        perfil.req = result['request']
        perfil.username = result['name']
        perfil.avatar = result['perfil']
        perfil.telefone = result['telefone']
        perfil.state = result['state']
        perfil.city = result['city']
        perfil.company = result['company']
        perfil.email = result['email']
        self.type = result['type']
        self.login_variables()

    def login_variables(self):
        if self.type in 'contractor':
            self.manager.current = 'Perfil'

    def page(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Perfil'
