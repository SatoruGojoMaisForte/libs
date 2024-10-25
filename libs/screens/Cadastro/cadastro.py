from kivy.network.urlrequest import UrlRequest
import re

from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar, MDSnackbarCloseButton
from kivymd.material_resources import dp
cont = 0

class Cadastro(MDScreen):
    cadastrar = False
    email = False

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
    def verificar_nome_sucesso(self, req, result):
        data = result
        print(f'response nome: {data}')
        if not data['exists']:
            self.ids.erro_nome.text = ''
            self.verificar_email(self.ids.email.text)
            self.email = True
        else:
            self.remove_widget(self.card)
            self.ids.erro_nome.text = 'Usuário já cadastrado'
            self.ids.erro_nome.text_color = 'red'
            self.verificar_email(self.ids.email.text)
            self.email = False
            self.remove_widget(self.card)

    def verificar_email(self, email):
        if not self.verificar_formato(email):
            self.remove_widget(self.card)
            self.ids.erro_email.text = 'Formato de email inválido'
            self.ids.erro_email.text_color = 'red'
            return
        url = f"https://api-email-5a79.onrender.com/check-email?email={email}"
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
            self.remove_widget(self.card)
            self.ids.erro_email.text = 'Email já cadastrado'
            self.ids.erro_email.text_color = 'red'
        else:
            self.ids.erro_email.text = ''
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
            self.ids.nome.text = ''
            self.ids.email.text = ''
            self.ids.senha.text = ''
            progress = self.ids['progress']
            icon_acerto = self.ids['acerto']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_acerto)
            self.ids.texto_carregando.text = 'Usuario cadastrado com sucesso'
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
        else:
            icon_error = self.ids['error']
            progress = self.ids['progress']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_error)
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
            self.ids.texto_carregando.text = 'Falha ao cadastrar usuario'

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
        self.add_widget(self.card)

