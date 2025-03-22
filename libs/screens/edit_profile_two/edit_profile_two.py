import json

from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, get_color_from_hex
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from libs.screens.edit_profile_two.citys import *


class EditProfileTwo(MDScreen):
    name_user = StringProperty('Solitude')
    city = StringProperty('brasilia')
    state = StringProperty('distrito federal')
    company = StringProperty()
    avatar = StringProperty()
    function = StringProperty('Mestre de obra')
    email = StringProperty()
    telefone = StringProperty()
    # Inicalizando o programa e carregando as variaveis

    def on_enter(self, *args):
        self.ids.company.text = self.company
        self.ids.state.text = self.state
        self.ids.state.text_color = 'white'
        self.ids.function.text = f'{self.function}'
        self.ids.city.text = self.city
        self.ids.city.text_color = 'white'
        self.menu_states()
        self.menu_citys()
        self.menu_functions()
        self.screen_finalize()

    def menu_functions(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['Mestre de obra', 'Engenheiro-civil', 'Pedreiro', 'Servente', 'Eletricista', 'Encanador']

        menu_itens = []
        position = 0
        for state in states:
            position += 1
            row = {'text': state, 'on_release': lambda x=state: self.replace_function(x)}
            menu_itens.append(row)

        self.menu2 = MDDropdownMenu(
            caller=self.ids.card_function,
            items=menu_itens,
            position='bottom',
            width_mult=5,
            max_height='400dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            # Adicionando personalizações estéticas
            elevation=8,
            radius=[10, 10, 10, 10],
            border_margin=12,
            ver_growth="down",
            hor_growth="right",
        )

        # Estilizando os itens do menu
        for item in menu_itens:
            item["font_style"] = "Subtitle1"
            item["height"] = dp(56)
            # Adicione ícones aos itens
            if "icon" not in item:
                item["icon"] = "checkbox-marked-circle-outline"
            item["divider"] = "Full"

    def replace_function(self, text):
        self.ids.function.text = text
        self.ids.function.text_color = get_color_from_hex('#FFFB46')
        self.menu2.dismiss()

    # Finalizando tela
    def screen_finalize(self):
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
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1736292941/true-fotor-20250107203414-removebg-preview_ajd1xd.png',
            size_hint=(None, None),
            size=("100dp", "150dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
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
            pos_hint={'center_x': .5, 'center_y': .7}
        )
        self.ids['progress'] = circle

        # Definindo o Label com texto carregando onde o usuário vai ter o indicador visual
        label = MDLabel(
            text='Carregando...',
            font_style='Headline',
            role='medium',
            halign='center',
            bold=True,
            text_color='black',
            pos_hint={'center_x': .5, 'center_y': .9}
        )
        label_2 = MDLabel(
            text='Os dados do seu perfil ja foram devidamene alterados',
            font_style='Title',
            role='small',
            halign='center',
            bold=False,
            text_color='gray',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        botton = MDButton(
            MDButtonText(
                text='Ok',
                theme_text_color='Custom',
                text_color='black',
                font_style='Title',
                role='medium',
                halign='center',
                bold=True,
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
            ),
            theme_bg_color='Custom',
            md_bg_color=(0.0, 1.0, 0.0, 1.0),
            pos_hint={'center_x': .5, 'center_y': .35},
            style='tonal',
            theme_width='Custom',
            size_hint_x=.4,

        )
        self.ids['ok'] = botton
        self.ids.ok.on_release = self.login_variables
        relative.add_widget(botton)
        relative.add_widget(icone_acerto)
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        relative.add_widget(label_2)
        self.card.add_widget(relative)

    # variaveis
    def menu_states(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará',
                  'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso',
                  'Mato Grosso do Sul',
                  'Minas Gerais', 'Pará', 'Paraíba', 'Paraná',
                  'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte',
                  'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo',
                  'Sergipe', 'Tocantins']

        menu_itens = []
        position = 0
        for state in states:
            position += 1
            row = {'text': state, 'on_release': lambda x=state: self.replace_state(x)}
            menu_itens.append(row)

        self.menu = MDDropdownMenu(
            caller=self.ids.card_state,
            items=menu_itens,
            position='bottom',
            width_mult=1,
            max_height='300dp',
            pos_hint={'center_x': 0.5}
        )

    def menu_citys(self):
        menu_itens = []
        payments = ['Cidades indisponiveis']
        for payment in payments:
            row = {'text': payment, 'text_color': 'red'}
            menu_itens.append(row)

        self.menu_city = MDDropdownMenu(
            caller=self.ids.card_city,
            items=menu_itens,
            position='bottom',
            width_mult=3,
            max_height='400dp',
            pos_hint={'center_x': 0.5}
        )

    def create_menu(self, state):

        menu_items = []

        state_functions = {
            'Acre': acre,
            'Alagoas': alagoas,
            'Amapá': amapa,
            'Amazonas': amazonas,
            'Bahia': bahia,
            'Ceará': ceara,
            'Distrito Federal': distrito_federal,
            'Espírito Santo': espirito_santo,
            'Goiás': goias,
            'Maranhão': maranhao,
            'Mato Grosso': mato_grosso,
            'Mato Grosso do Sul': mato_grosso_do_sul,
            'Minas Gerais': minas_gerais,
            'Pará': para,
            'Paraíba': paraiba,
            'Paraná': parana,
            'Pernambuco': pernambuco,
            'Piauí': piaui,
            'Rio de Janeiro': rio_de_janeiro,
            'Rio Grande do Norte': rio_grande_do_norte,
            'Rio Grande do Sul': rio_grande_do_sul,
            'Rondônia': rondonia,
            'Roraima': roraima,
            'Santa Catarina': santa_catarina,
            'São Paulo': sao_paulo,
            'Sergipe': sergipe,
            'Tocantins': tocantins,
        }

        if state in state_functions:
            cities = state_functions[state]()
            for city in cities:
                row = {'text': city, 'on_release': lambda x=city: self.replace_city(x)}
                menu_items.append(row)
        else:
            print(f"Estado '{state}' não encontrado!")

        self.menu_city.clear_widgets()
        self.menu_city = MDDropdownMenu(
            caller=self.ids.card_city,
            items=menu_items,
            position='bottom',
            width_mult=2,
            max_height='400dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

    # Ações dos widgets
    def replace_state(self, state):
        self.ids.city.text_color = get_color_from_hex('#FFFB46')
        self.ids.city.text = 'Selecione uma Cidade'
        self.ids.state.text_color = get_color_from_hex('#FFFB46')
        self.ids.state.text = f'{state}'
        self.menu.dismiss()
        self.create_menu(state)

    def replace_city(self, city):
        self.ids.city.text_color = get_color_from_hex('#FFFB46')
        self.ids.city.text = city
        self.menu_city.dismiss()

    # manipulando o banco de dados
    def step_one(self):
        # Get all the information
        state = self.ids.state.text
        city = self.ids.city.text
        function = self.ids.function.text
        company = self.ids.company.text
        if function in 'Selecione uma profissão':
            self.menu2.open()
            return

        if state in 'Selecione um Estado':
            self.menu.open()
            return

        if city in 'Selecione uma Cidade':
            self.menu_city.open()
            return

        if not company:
            self.ids.company.focus = True
            return

        def show_snackbar():
            MDSnackbar(
                MDSnackbarText(
                    text="Apresente novos dados para atualização",
                    theme_text_color='Custom',
                    text_color='white',
                    bold=True
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                halign='center',
                size_hint_x=0.85,
                theme_bg_color='Custom',
                background_color=get_color_from_hex('#00b894')
            ).open()

        # Verificação otimizada
        if self.state == state and self.city == city and self.company == self.ids.company.text and self.ids.function.text == self.function:
            show_snackbar()
            return

        self.step_two()

    def step_two(self):
        '''Pegando todos os usuarios do banco de dados'''

        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users'
        UrlRequest(
            url=f'{url}/.json',
            on_success=self.list_users,
        )

    def list_users(self, req, users):
        print('Verificando os dados')
        name = str(self.name_user).replace(' ', '')
        print(users)
        for key, value in users.items():

            if value['name'] == self.name_user:
                print(value['name'])
                print('achei')
                self.key = key
                self.update_database(key)
            else:
                print(value['name'])

    def update_database(self, key):
        print('update')
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{key}'

        if not self.ids.company.text:
            data = {
                'city': self.ids.city.text,
                'state': self.ids.state.text
            }
        else:
            data = {
                'city': self.ids.city.text,
                'state': self.ids.state.text,
                'company': self.ids.company.text,
                'function': self.ids.function.text
            }
            print('Compania')

        UrlRequest(
            url=f'{url}/.json',
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.database,
        )

    def database(self, req, result):
        print(result)
        progress = self.ids['progress']
        self.ids['relative'].remove_widget(progress)
        self.ids.texto_carregando.text = 'Tudo certo!'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .6}
        self.add_widget(self.card)

    # Definindo a tela anterior
    def previous(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'EditProfile'

    def login_variables(self):
        app = MDApp.get_running_app()
        screen_manager = app.root
        perfil = screen_manager.get_screen('Perfil')
        perfil.username = self.name_user
        perfil.company = self.ids.company.text
        perfil.state = self.ids.state.text
        perfil.city = self.ids.city.text
        perfil.email = self.email
        perfil.telefone = self.telefone
        perfil.avatar = self.avatar
        self.remove_widget(self.card)
        self.manager.current = 'Perfil'

