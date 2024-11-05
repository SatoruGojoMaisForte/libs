from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from urllib.parse import urlencode
import bcrypt
import json

class LoginScreen(MDScreen):

    def on_enter(self, *args):
        # Define os ícones de erro e acerto
        self.ids['error'] = MDIconButton(
            icon='alert-circle',
            theme_font_size='Custom',
            font_size='55sp',
            icon_color='red',
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['acerto'] = MDIconButton(
            icon='check',
            theme_font_size='Custom',
            font_size='50sp',
            icon_color='green',
            pos_hint={'center_x': .5, 'center_y': .6}
        )

        # Configura o cartão de carregamento
        self.card = MDCard(
            id='carregando',
            style='elevated',
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            md_bg_color=(1, 1, 1, 1)
        )
        self.ids['card'] = self.card

        # Cria o layout relativo
        relative = MDRelativeLayout()
        self.ids['relative'] = relative

        # Circular progress indicator
        circle = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['progress'] = circle

        # Label de carregamento
        label = MDLabel(
            text='Carregando...',
            font_style='Title',
            halign='center',
            bold=True,
            text_color='black',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        self.card.add_widget(relative)

    def verificar_nome(self):
        nome = self.ids.usuario.text
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
            on_failure=self.error,

            method='GET',
        )

    def error(self, req, error):
        print(error)

    def sucesso_nome(self, req, result):
        if result:
            for usuario_id, usuario_data in result.items():
                if usuario_data.get('name') == self.ids.usuario.text:
                    self.ids.usuario.error = False
                    self.ids.encontrar.text = ''
                    print('Usuário encontrado')
                    self.verificar_senha()
                    return

        self.remove_widget(self.card)
        self.ids.usuario.error = True
        self.ids.encontrar.text = 'Usuario não cadastrado'

    def verificar_senha(self):
        senha = self.ids.senha.text
        nome = self.ids.usuario.text
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

        # Realiza a requisição GET com UrlRequest para verificação de senha
        UrlRequest(
            f'{url}?{query_string}',
            on_success=self.sucesso_senha_verificacao,
            on_error=self.error_,
            on_failure=self.error_,
            method='GET',
        )

    def error_(self, req, error):
        print(error)

    def sucesso_senha_verificacao(self, req, result):
        senha = self.ids.senha.text
        print('correto')
        if result:
            for usuario_id, usuario_data in result.items():
                password_bytes = senha.encode('utf-8')
                user_password_bytes = usuario_data.get('password', '').encode('utf-8')
                if bcrypt.checkpw(password_bytes, user_password_bytes):
                    self.sucesso_senha()
                    self.ids.senha_correta.text = ''
                    self.ids.senha.error = False
                    return

        self.remove_widget(self.card)
        self.ids.senha_correta.text = 'A senha está incorreta'
        self.ids.senha.error = True

    def sucesso_senha(self):
        self.ids.senha_correta.text = ''
        self.ids.senha.error = False
        acerto = self.ids['acerto']
        progress = self.ids['progress']
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(acerto)
        self.ids.texto_carregando.text = 'Login completo'
        print('Login completo')

    def focus(self):
        textfield_usuario = self.ids.usuario
        textfield_password = self.ids.senha
        text_user = textfield_usuario.text
        text_password = textfield_password.text

        if not textfield_usuario.focus and not textfield_usuario.text:
            textfield_usuario.focus = True

        if text_user:
            textfield_password.focus = True

        if text_user and text_password:
            self.add_widget(self.card)
            self.verificar_nome()

    def chamar_trocar(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "Send"

    def cadastroscreen(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'cadastro'
