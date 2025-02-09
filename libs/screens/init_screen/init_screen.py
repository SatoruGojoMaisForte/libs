import bcrypt
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.card import MDCard


class InitScreen(MDScreen):
    carregado = False
    name = False
    senha = ''

    def on_enter(self, *args):
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
        icone_acerto = AsyncImage(
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1732733742/image_1_blzg3r.png',
            size_hint=(None, None),
            size=("100dp", "150dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            allow_stretch=True
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
        self.card.bind(on_release=self.page)

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

    def etapa1(self):
        if self.ids.nome.text == '':
            self.ids.nome.focus = True
            return
        else:

            if self.ids.senha.text == '':
                self.ids.senha.focus = True
                return
            else:
                print('Ambos')
                self.verificar_senha()

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
                    progress = self.ids['progress']
                    icon_acerto = self.ids['acerto']
                    self.ids['relative'].remove_widget(progress)
                    self.ids['relative'].add_widget(icon_acerto)
                    self.ids.texto_carregando.text = 'Login completo'
                    self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
                    self.add_widget(self.card)
                else:
                    print('senha está errada seu acefalo burro do caralho')
                    self.ids.senha.error = True
                    self.ids.senha_errada.text = 'A senha inserida está incorreta'
                break
            else:
                self.ids.nome_errado.text = 'Pessoa não cadastrado'
                self.ids.nome.error = True

    def page(self, instance):
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'Bricklayer'
