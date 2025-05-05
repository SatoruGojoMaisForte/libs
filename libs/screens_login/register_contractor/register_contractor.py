import json
import bcrypt
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar


class RegisterContractor(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Cria o MDCard
        self.card = MDCard(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            line_color=(0.5, 0.5, 0.5, 1),  # Cor da borda
            theme_bg_color='Custom',
            md_bg_color='white',
            md_bg_color_disabled="white",

        )

        # Cria o layout relativo para organizar os elementos dentro do card
        relative_layout = MDRelativeLayout()

        # Adiciona a AsyncImage (imagem assíncrona)
        async_image = AsyncImage(
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1739053352/image_1_hkgebk.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        relative_layout.add_widget(async_image)

        # Adiciona o primeiro MDLabel ("Tudo certo!!")
        label_title = MDLabel(
            text='Tudo certo!!',
            bold=True,
            halign='center',
            font_style='Headline',  # Equivalente a 'Headline'
            pos_hint={'center_x': 0.5, 'center_y': 0.47},
            theme_text_color='Custom',
            text_color=(0, 0, 0, 1)  # Cor preta
        )
        relative_layout.add_widget(label_title)

        # Adiciona o segundo MDLabel (mensagem de sucesso)
        label_message = MDLabel(
            text='Contratante cadastrado com sucesso. clique em ok para acessar sua conta',
            font_style='Label',  # Equivalente a 'Label'
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            padding=(20, 0),
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1)  # Cor cinza
        )
        relative_layout.add_widget(label_message)

        # adiciona o botão para proxima pagina
        button = MDButton(
            MDButtonText(
                text='Ok',
                theme_text_color='Custom',
                text_color='white',
                halign='center',
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                font_style='Title',
                role='medium',
                bold=True
            ),
            theme_width='Custom',
            size_hint_x=.3,
            theme_bg_color='Custom',
            md_bg_color=[0.0, 1.0, 0.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
        )
        self.ids['ok'] = button
        self.ids.ok.on_release = self.login_variables
        relative_layout.add_widget(button)
        # Adiciona o layout relativo ao card
        self.card.add_widget(relative_layout)

    def etapa1(self):
        if self.ids.nome.text == '':
            self.ids.nome.focus = True

        else:

            if self.ids.senha.text == '':
                self.ids.senha.focus = True

            else:
                print('Preenchidos')
                self.pre_step()

    def pre_step(self):
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/.json'
        UrlRequest(
            url,
            on_success=self.get_name
        )

    def get_name(self, req, result):
        nome_digitado = self.ids.nome.text.strip().lower()
        try:
            for _, user_data in result.items():
                nome_atual = user_data.get('name', '').strip().lower()
                if nome_atual == nome_digitado:
                    MDSnackbar(
                        MDSnackbarText(
                            text='Esse nome de usuário já está cadastrado',
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
                    return  # Para aqui pois já achou
            self.etapa2()
        except Exception as e:
            print("Erro ao buscar nomes:", e)
            MDSnackbar(
                MDSnackbarText(
                    text='Erro de conexão. Verifique sua internet.',
                    theme_text_color='Custom',
                    text_color='white',
                    bold=True
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                halign='center',
                size_hint_x=0.8,
                theme_bg_color='Custom',
                background_color=(1, 0.3, 0.3, 1)
            ).open()

    def etapa2(self):
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users'
        hashed_password = self.ids.senha.text.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=hashed_password, salt=salt).decode('utf-8')
        data = {"name": self.ids.nome.text, 'senha': hashed_password,
                'perfil': 'https://res.cloudinary.com/dsmgwupky/image/upload/v1726685784/a8da222be70a71e7858bf752065d5cc3-fotor-20240918154039_dokawo.png',
                'telefone': 'Não definido',
                'state': 'Não definido',
                'city': 'Não definido',
                'company': 'Não definido',
                'email': 'Não definido',
                'function': 'Não definido',
                }
        UrlRequest(
            f'{url}/.json',
            method='POST',
            on_success=self.cadastrado,
            req_body=json.dumps(data),
            req_headers={'Content-Type': 'application/json'}
        )

    def cadastrado(self, req, result):
        k = ''
        for key, x in result.items():
            k = key
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{x}/.json'
        UrlRequest(
            url,
            method='GET',
            on_success=self.next_perfil
        )

    def next_perfil(self, instance, result):
        app = MDApp.get_running_app()
        screen_manager = app.root
        perfil = screen_manager.get_screen('Perfil')
        perfil.function = result['function']
        perfil.username = result['name']
        perfil.avatar = result['perfil']
        perfil.telefone = result['telefone']
        perfil.state = result['state']
        perfil.city = result['city']
        perfil.company = result['company']
        perfil.email = result['email']
        self.add_widget(self.card)

    def page(self, instance):
        print('passo')

    def login_variables(self):
        self.remove_widget(self.card)
        self.manager.current = 'Perfil'

    def voltar(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'ChoiceAccount'
