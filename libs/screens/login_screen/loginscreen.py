import queue
import threading

from kivy.properties import Clock
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
import requests
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
click_button_user = 0
click_button_password = 0


class LoginScreen(MDScreen):
    def on_enter(self, *args):
        # Limpa todos os widgets e adiciona novamente
        children = list(self.children)  # Salva os widgets atuais
        self.clear_widgets()
        for widget in children:
            self.add_widget(widget)

    def verificar_nome(self):
        nome = self.ids.usuario.text
        url = f"https://api-name.onrender.com/check-name?name={nome}"
        UrlRequest(
            url,
            on_success=self.sucesso_nome,
            method='GET'

        )

    def sucesso_nome(self, req, result):
        data = result
        if data['exists']:
            self.ids.encontrar.text = ''
            self.ids.usuario.error = False
            print('usuario cadastrado')
            self.verificar_senha()
        else:
            self.ids.encontrar.text = 'Usuario não cadastrado'
            self.ids.usuario.error = True
            print('usuario não cadastrado')
            self.ids.carregando.size_hint = (0.00001, 0.00001)
            self.ids.carregando.pos_hint = {"center_y": 0.91, "center_x": 1.05}

    def error(self, req, error):
        print(error)

    def verificar_senha(self):
        senha = self.ids.senha.text
        nome = self.ids.usuario.text
        url = f"https://api-senha.onrender.com/check-password?name={nome}&password={senha}"
        headers = {
            'Authorization': 'Bearer spike'
        }
        UrlRequest(
            url,
            method='GET',
            on_success=self.sucesso_senha,
            on_error=self.error,
            on_failure=self.error,
            req_headers=headers
        )

    def sucesso_senha(self, req, result):
        data = result
        print('sei la')
        if data['exists']:
            self.ids.senha_correta.text = ''
            self.ids.senha.error = False
            self.ids.progresso.pos_hint = {"center_y": 0.93, "center_x": 1.2}
            self.ids.carregando2.add_widget(
                MDIconButton(
                    icon='check',
                    theme_font_size='Custom',
                    font_size='50sp',
                    theme_icon_color='Custom',
                    pos_hint={'center_x': .5, 'center_y': .6},
                    icon_color='green'
            )
            )
            self.ids.texto_carregando.text = 'Login completo'
            print('senha correta')
        else:
            self.ids.senha_correta.text = 'Senha incorreta'
            self.ids.senha.error = True
            self.ids.carregando.size_hint = (0.000001, 0.0000001)
            self.ids.carregando.pos_hint = {"center_y": 0.93, "center_x": 1.05}
            print('senha incorreta')

    def focus(self):
        global click_button_user, click_button_password
        textfield_usuario = self.ids.usuario
        textfield_password = self.ids.senha
        text_user = self.ids.usuario.text
        text_password = textfield_password.text
        # verificações se os campos estiverem vazios
        if not textfield_usuario.focus and not textfield_usuario.text:
            textfield_usuario.focus = True
            click_button_user += 1

        if text_user:
            textfield_password.focus = True

        if text_user and text_password:
            self.ids.carregando.size_hint = (1, 1)
            self.ids.carregando.pos_hint = {"center_y": 0.5, "center_x": 0.5}
            self.verificar_nome()

    def chamar_trocar(self, *args):
        self.manager.current = "Send"

    def cadastroscreen(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'cadastro'
