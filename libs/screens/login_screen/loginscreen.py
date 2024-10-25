import queue
import threading

from kivy.properties import Clock
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
import requests
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
click_button_user = 0
click_button_password = 0
cont = 0

class LoginScreen(MDScreen):
    def on_enter(self, *args):
        # definindo o icone de erro para as telas
        icone_erro = MDIconButton(
            icon='alert-circle',
            theme_font_size='Custom',
            font_size='55sp',
            theme_icon_color='Custom',
            pos_hint={'center_x': .5, 'center_y': .6},
            icon_color='red'  # Cor vermelha para representar o erro
        )
        self.ids['error'] = icone_erro
        # definindo o icone de acerto para as telas
        icone_acerto = MDIconButton(
            icon='check',
            theme_font_size='Custom',
            font_size='50sp',
            theme_icon_color='Custom',
            pos_hint={'center_x': .5, 'center_y': .6},
            icon_color='green'  # Cor vermelha para representar o erro
        )
        self.ids['acerto'] = icone_acerto
        # definindo o md card onde vai fica todo o corpo do layout
        self.card = MDCard(
            id='carregando',
            style='elevated',
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            # Sets custom properties.
            theme_bg_color="Custom",
            md_bg_color=(1, 1, 1, 1),
            md_bg_color_disabled="grey",
            theme_shadow_offset="Custom",
            shadow_offset=(1, -2),
            theme_shadow_softness="Custom",
            shadow_softness=1,
            theme_elevation_level="Custom",
            elevation_level=2
        )
        self.ids['card'] = self.card
        # definindo o relative onde todo o corpo será posicionado
        relative = MDRelativeLayout()
        self.ids['relative'] = relative
        # definindo o circular progress onde o usuario vai ter o carregamento visual
        circle = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['progress'] = circle

        # definindo o label com texto carregando onde o usuario vai ter o indicador visual
        label = MDLabel(
            text='Carregando...',
            font_style='Title',
            role='medium',
            halign='center',
            bold=True,
            theme_text_color='Custom',
            text_color='black',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        self.card.add_widget(
            relative
        )

    def verificar_nome(self):
        nome = self.ids.usuario.text
        url = f"https://api-name.onrender.com/check-name?name={nome}"
        UrlRequest(
            url,
            on_success=self.sucesso_nome,
            timeout=5,
            on_error=self.error_request_name,
            method='GET'

        )

    def error_request_name(self, req, error):
        global cont
        cont += 1
        if cont <= 3:
            self.verificar_nome()
        else:
            icon_error = self.ids['error']
            progress = self.ids['progress']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_error)
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
            self.ids.texto_carregando.text = 'Falha ao verificar usuario verifique sua internet'

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
        global cont
        cont += 1
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
            self.add_widget(self.card)
            self.verificar_nome()

    def chamar_trocar(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "Send"

    def cadastroscreen(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'cadastro'
