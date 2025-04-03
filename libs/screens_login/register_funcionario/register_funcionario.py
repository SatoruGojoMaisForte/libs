import json

import bcrypt
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText


class RegisterFuncionario(MDScreen):
    lobo = ''

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

    def etapa1(self):
        if self.ids.nome.text == '':
            self.ids.nome.focus = True

        else:

            if self.ids.senha.text == '':
                self.ids.senha.focus = True

            else:
                url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/.json'
                UrlRequest(
                    url,
                    method='GET',
                    on_success=self.etapa2,
                )

    def etapa2(self, req, result):
        names = []
        for cargo, nome in result.items():
            if nome['Name'] == self.ids.nome.text:
                MDSnackbar(
                    MDSnackbarText(
                        text='Esse nome de usuario já esta cadastrado',
                        theme_text_color='Custom',
                        text_color='white',
                        bold=True
                    ),
                    y=dp(24),
                    pos_hint={"center_x": 0.5},
                    halign='center',
                    size_hint_x=0.8,
                    theme_bg_color='Custom',
                    background_color='red'
                ).open()
                names.append(nome['Name'])

        if not names:
            self.etapa3()

    def etapa3(self):
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios'
        hashed_password = self.ids.senha.text.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=hashed_password, salt=salt).decode('utf-8')
        data = {"Name": self.ids.nome.text,
                'password': hashed_password,
                'avatar': 'https://res.cloudinary.com/dsmgwupky/image/upload/v1726685784/a8da222be70a71e7858bf752065d5cc3-fotor-20240918154039_dokawo.png',
                'coextistence': 0,
                'contractor': '',
                'day': "",
                'days_work': 0,
                'effiency': 0,
                'email': 'Não definido',
                'function': 'Não definido',
                'method_salary': '',
                'punctuality': '',
                'salary': '',
                'scale': '',
                'skills': "[]",
                'sumary': 'Não definido',
                'telefone': 'Não definido',
                'tot': 0,
                'ultimate': '',
                'valleys': "{}",
                'week_1': 0,
                'week_2': 0,
                'week_3': 0,
                'week_4': 0,
                'work_days_week1': "[]",
                'work_days_week2': "[]",
                'work_days_week3': "[]",
                'work_days_week4': "[]",
                }

        UrlRequest(
            f'{url}/.json',
            method='POST',
            on_success=self.cadastrado,
            req_body=json.dumps(data),
            req_headers={'Content-Type': 'application/json'}
        )

    def cadastrado(self, req, result):
        url = f"https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{result['name']}.json"
        self.lobo = result['name']
        UrlRequest(
            url,
            method='GET',
            on_success=self._next_page_perfil,
        )

    def _next_page_perfil(self, instance, result):
        app = MDApp.get_running_app()
        print(self.lobo)
        screenmanager = app.root
        perfil = screenmanager.get_screen('PrincipalScreenEmployee')
        perfil.employee_name = result['Name']
        perfil.employee_function = result['function']
        perfil.employee_mail = result['email']
        perfil.employee_telephone = result['telefone']
        perfil.avatar = result['avatar']
        perfil.employee_summary = result['sumary']
        perfil.skills = result['skills']
        perfil.key = self.lobo
        self.lobo = ''
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'

    def page(self, instance):
        print('passo')

    def voltar(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'ChoiceAccount'
