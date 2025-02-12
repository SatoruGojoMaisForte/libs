import json

from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen


class StepFour(MDScreen):
    contratante = StringProperty()
    nome = StringProperty()
    cpf = StringProperty()
    pix = StringProperty()
    contratado = StringProperty()
    idade = StringProperty()
    competencias = StringProperty()
    cargo = StringProperty()
    diaria = False
    empreita = False

    def on_enter(self, *args):
        print(self.contratante, self.nome, self.cpf, self.pix, self.contratado, self.idade, self.competencias,
              self.cargo)
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
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1730504140/image_yvn8lp.png',
            size_hint=(None, None),
            size=("80dp", "150dp"),
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
        if self.ids.diaria.text == '':
            self.ids.diaria.focus = True
        else:
            try:
                number = int(self.ids.diaria.text)
                print(number)
                self.etapa_1()
            except:
                print('Forneça um numero valido')

    def page_return(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'StepThree'

    def etapa_1(self):

        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios'
        data = {}
        if self.diaria:
            data = {
                'Full name': self.nome,
                "Employee's CPF": self.cpf,
                "Employee's Pix": self.pix,
                'Data de contratação': self.contratado,
                'Hiring Date': self.idade,
                'Employer:': self.contratante,
                'Salary:': str(self.ids.diaria.text),
                'wage': 'Diaria'
            }

        if self.empreita:
            data = {
                'Full name': self.nome,
                "Employee's CPF": self.cpf,
                "Employee's Pix": self.pix,
                'Data de contratação': self.contratado,
                'Hiring Date': self.idade,
                'Employer:': self.contratante,
                'Salary:': str(self.ids.diaria.text),
                'wage': 'Empreita'
            }

        UrlRequest(
            f'{url}/.json',
            req_body=json.dumps(data),
            req_headers={'Content-Type': 'application/json'},
            on_success=self.etapa2
        )

    def etapa2(self, req, result):
        self.funcionario = result['name']
        progress = self.ids['progress']
        icon_acerto = self.ids['acerto']
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_acerto)
        self.ids.texto_carregando.text = 'Funcionario Cadastrado'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
        self.add_widget(self.card)

    def daily(self):
        self.diaria = True
        self.ids.undertakes.md_bg_color = 'white'
        self.ids.daily.md_bg_color = [0.0, 1.0, 0.0, 1.0]

    def undertakes(self):
        self.empreita = True
        self.ids.daily.md_bg_color = 'white'
        self.ids.undertakes.md_bg_color = [0.0, 1.0, 0.0, 1.0]
