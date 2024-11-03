import json
import re
from urllib.parse import urlencode
import string
import random
import bcrypt
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from time import sleep


class SendCode(MDScreen):
    cont_email = 0  # Contador para tentativas de verificação de e-mail
    cont_envio = 0  # Contador para tentativas de envio de código

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.code = None

    def on_enter(self, *args):
        self.code = ''
        # Definindo o ícone de erro para as telas
        icone_erro = MDIconButton(
            icon='alert-circle',
            theme_font_size='Custom',
            font_size='55sp',
            theme_icon_color='Custom',
            pos_hint={'center_x': .5, 'center_y': .6},
            icon_color='red'  # Cor vermelha para representar o erro
        )
        self.ids['error'] = icone_erro

        # Definindo o ícone de acerto para as telas
        icone_acerto = MDIconButton(
            icon='check',
            theme_font_size='Custom',
            font_size='50sp',
            theme_icon_color='Custom',
            pos_hint={'center_x': .5, 'center_y': .6},
            icon_color='green'  # Cor verde para representar o acerto
        )
        self.ids['acerto'] = icone_acerto

        # Definindo o MDCard onde vai ficar todo o corpo do layout
        self.card = MDCard(
            id='carregando',
            style='elevated',
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            md_bg_color=(1, 1, 1, 1),
            theme_bg_color="Custom",
            theme_shadow_offset="Custom",
            shadow_offset=(1, -2),
            theme_shadow_softness="Custom",
            shadow_softness=1,
            theme_elevation_level="Custom",
            elevation_level=2
        )
        self.ids['card'] = self.card

        # Definindo o RelativeLayout onde todo o corpo será posicionado
        relative = MDRelativeLayout()
        self.ids['relative'] = relative

        # Definindo o CircularProgressIndicator onde o usuário vai ter o carregamento visual
        circle = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['progress'] = circle

        # Definindo o Label com texto carregando onde o usuário vai ter o indicador visual
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

    def set_email(self):
        self.verificar_email = self.ids.verificar_email.text

    def chama_login(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Login'

    def is_email_valid(self, text: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, text) is not None

    def email_existir(self, email):
        if not self.is_email_valid(email):
            self.remove_widget(self.card)
            self.ids.erro_email.text = 'Formato de email inválido'
            self.ids.erro_email.text_color = 'red'
            return

        nome = self.ids.verificar_email.text
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
            on_success=self.existir,
            method='GET',
        )

    def existir(self, req, result):
        if result:
            for usuario_id, usuario_data in result.items():
                if usuario_data.get('email') == self.ids.verificar_email.text:
                    self.ids.erros.text = ''
                    self.ids.verificar_email.error = False
                    self.patch(result)
                    return

        self.ids.erros.text = 'Email não cadastrado'
        self.ids.erros.text_color = 'red'
        self.ids.verificar_email.error = True
        self.remove_widget(self.card)
        print('email não cadastrado')

    def criar(self):
        # criando um codigo
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choices(caracteres, k=6))

    def patch(self, result):
        codigo_aleatorio = self.criar()
        self.code = codigo_aleatorio
        usuarios = result
        mail = self.ids.verificar_email.text
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'

        # Encontra o primeiro índice onde o email do usuário corresponde ao email fornecido
        indice_usuario = next((k for k, v in usuarios.items() if v.get('email') == mail), None)

        # Se o índice foi encontrado, continua o processo
        if indice_usuario is not None:
            hashed_code = codigo_aleatorio.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_code = bcrypt.hashpw(password=hashed_code, salt=salt).decode('utf-8')
            dados = {'verification_code': hashed_code}

            print('fazendo a requisição')
            self.ids.erros.text = ''
            self.ids.verificar_email.error = False
            UrlRequest(
                url=f'{url}/{indice_usuario}.json',
                req_body=json.dumps(dados),
                on_success=self.codigo_alterado,
                req_headers={'Content-Type': 'application/json'},
                method='PATCH'
            )
        else:
            self.remove_widget(self.card)
            self.ids.erros.text = 'Email não cadastrado'
            self.ids.verificar_email.error = True

    def codigo_alterado(self, req, result):
        self.enviar_email()

    def enviar_email(self):
        code = self.code
        email = self.ids.verificar_email.text
        url = f'https://api-email-5a79.onrender.com/send_verification_code?email={email}&code={code}'
        UrlRequest(
            url,
            method='POST',
            on_success=self.ultima_etapa
        )

    def error(self, req, error):
        print(error)

    def ultima_etapa(self, req, result):
        progress = self.ids['progress']
        icon_acerto = self.ids['acerto']
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_acerto)
        self.ids.texto_carregando.text = 'Verificação enviada'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
        sleep(2)
        self.remove_widget(self.card)
        self.chamar_pagina()

    def chamar_pagina(self):
        check = self.manager.get_screen('Check')
        check.email = self.ids.verificar_email.text
        self.manager.current = 'Check'

    def enviar_codigo(self):
        texto = self.ids.verificar_email.text

        if texto:
            if self.is_email_valid(texto):
                self.ids.verificar_email.error = False
                self.ids.erros.text = ''
                self.add_widget(self.card)
                self.cont_email = 0  # Reseta o contador ao iniciar a verificação
                self.email_existir(texto)
            else:
                self.remove_widget(self.card)
                self.ids.erros.text = 'O formato do email é inválido'
                self.ids.verificar_email.error = True
        else:
            self.ids.verificar_email.focus = True
