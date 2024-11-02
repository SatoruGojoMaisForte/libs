import json
from urllib.parse import urlencode
import bcrypt
from kivy.network.urlrequest import UrlRequest
import re
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock


class Cadastro(MDScreen):
    cadastrar = False
    email = False

    def on_enter(self, *args):

        # Configurações visuais
        icone_erro = MDIconButton(icon='alert-circle', theme_font_size='Custom', font_size='55sp',
                                  theme_icon_color='Custom', pos_hint={'center_x': .5, 'center_y': .6},
                                  icon_color='red')
        self.ids['error'] = icone_erro

        icone_acerto = MDIconButton(icon='check', theme_font_size='Custom', font_size='50sp',
                                    theme_icon_color='Custom', pos_hint={'center_x': .5, 'center_y': .6},
                                    icon_color='green')
        self.ids['acerto'] = icone_acerto

        self.card = MDCard(id='carregando', style='elevated', size_hint=(1, 1),
                           pos_hint={"center_y": 0.5, "center_x": 0.5},
                           padding="16dp", md_bg_color=(1, 1, 1, 1))
        self.ids['card'] = self.card

        relative = MDRelativeLayout()
        self.ids['relative'] = relative

        circle = MDCircularProgressIndicator(size_hint=(None, None), size=("60dp", "60dp"),
                                             pos_hint={'center_x': .5, 'center_y': .6})
        self.ids['progress'] = circle

        label = MDLabel(text='Carregando...', font_style='Title', halign='center', bold=True,
                        theme_text_color='Custom', text_color='black', pos_hint={'center_x': .5, 'center_y': .5})
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        self.card.add_widget(relative)

    def login(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Login'

    def verificar_formato(self, email: str) -> bool:
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(regex, email))

    def ping_api_nome(self):
        url = "https://api-name.onrender.com/ping"
        UrlRequest(url, on_success=self.on_ping_success, on_error=self.error_request_ping, timeout=2, method='GET')

    def ping_api_email(self):
        url = "https://api-email-5a79.onrender.com/ping"
        UrlRequest(url, on_success=self.on_ping_success, on_error=self.error_request_ping, timeout=2, method='GET')

    def on_ping_success(self, req, result):
        pass

    def verificar_nome(self, tentativa=1):
        nome = self.ids.nome.text
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios.json'
        parametros = {
            "rules": {
                "Usuarios": {
                    ".indexOn": ["name"],
                    ".read": "auth != null",
                    ".write": "auth != null"
                }
            }
        }

        # Converte os parâmetros para query string
        query_string = urlencode(parametros)

        # Realiza a requisição GET com UrlRequest
        UrlRequest(
            f'{url}?{query_string}',
            on_success=self.sucesso_nome,

            method='GET',
        )

    def sucesso_nome(self, req, result):
        if result:
            for usuario_id, usuario_data in result.items():
                if usuario_data.get('name') == self.ids.nome.text:
                    self.ids.erro_nome.text = 'Usuário já cadastrado'
                    self.ids.erro_nome.text_color = 'red'
                    self.email = False
                    self.remove_widget(self.card)
                    return

        self.ids.erro_nome.text = ''
        self.email = True
        self.verificar_email()

    def verificar_email(self, tentativa=1):
        email = self.ids.email.text
        if not self.verificar_formato(email):
            self.remove_widget(self.card)
            self.ids.erro_email.text = 'Formato de email inválido'
            self.ids.erro_email.text_color = 'red'
            return

        nome = self.ids.email.text
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios.json'
        parametros = {
            "rules": {
                "Usuarios": {
                    ".indexOn": ["email"],
                    ".read": "auth != null",
                    ".write": "auth != null"
                }
            }
        }

        # Converte os parâmetros para query string
        query_string = urlencode(parametros)

        # Realiza a requisição GET com UrlRequest
        UrlRequest(
            f'{url}?{query_string}',
            on_success=self.sucesso_email,
            method='GET',
        )

    def sucesso_email(self, req, result):
        if result:
            for usuario_id, usuario_data in result.items():
                if usuario_data.get('email') == self.ids.email.text:
                    self.ids.erro_email.text = 'Email já cadastrado'
                    self.ids.erro_email.text_color = 'red'
                    self.remove_widget(self.card)
                    return

        self.ids.erro_email.text = ''
        if self.email:
            if len(self.ids.senha.text) >= 6:
                self.ids.erro_senha.text = ''
                self.ids.senha.error = False
                self.adicionar_usuario()
            else:
                self.ids.error_senha.text = 'A senha deve ter mais de 6 caracteres'
                self.ids.senha.error = True
        else:
            pass

    def adicionar_usuario(self):
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios.json'
        senha = self.ids.senha.text
        hashed_password = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=hashed_password, salt=salt).decode(
            'utf-8')  # Decodifique para armazenar como string

        dados = {
            'name': self.ids.nome.text,
            'email': self.ids.email.text,
            'password': hashed_password,
            'bio': 'Olá sou usuario do Chatto',
            'perfil': 'https://res.cloudinary.com/dsmgwupky/image/upload/v1726685784/a8da222be70a71e7858bf752065d5cc3-fotor-20240918154039_dokawo.png'
        }

        # Realiza a requisição POST com UrlRequest para adicionar o usuário
        UrlRequest(
            url,
            req_body=json.dumps(dados),
            on_success=self.sucesso_adicionar_usuario,
            method='POST',
            req_headers={'Content-Type': 'application/json'}
        )

    def sucesso_adicionar_usuario(self, req, result):
        self.ids.nome.text = ''
        self.ids.email.text = ''
        self.ids.senha.text = ''
        progress = self.ids['progress']
        icon_acerto = self.ids['acerto']
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_acerto)
        self.ids.texto_carregando.text = 'Usuario cadastrado com sucesso'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}


    def logica(self):
        nome = self.ids.nome.text
        email = self.ids.email.text
        senha = self.ids.senha.text



        self.verificar_nome()  # Verifica o nome e inicia a lógica de cadastro
        self.add_widget(self.card)
