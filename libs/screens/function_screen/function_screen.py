import json
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest
from libs.screens.function_screen.citys import *


class FunctionScreen(MDScreen):
    contractor = StringProperty()
    dialy = 0
    undertakes = 0
    encargo = False
    salario = False
    local = False

    def on_enter(self, *args):
        self.menu_states()
        self.menu_payments()
        self.menu_citys()
        self.screen_finalize()

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
            text='A solicitação para esta profissão já foi devidamente registrada. Solicitamos que aguarde',
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
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            ),
            theme_bg_color='Custom',
            md_bg_color=(0.0, 1.0, 0.0, 1.0),
            pos_hint={'center_x': .5, 'center_y': .35},
            style='tonal',
            theme_width='Custom',
            size_hint_x=.4,
        )
        relative.add_widget(botton)
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        relative.add_widget(label_2)
        self.card.add_widget(relative)

    def menu_citys(self):
        menu_itens = []
        payments = ['Cidades indisponiveis']
        for payment in payments:
            row = {'text': payment, 'text_color': 'red'}
            menu_itens.append(row)

        self.menu_city = MDDropdownMenu(
            caller=self.ids.card_city,
            items=menu_itens,
            position='bottom'
        )

    def menu_payments(self):
        menu_itens = []
        payments = ['Diaria', 'semanal', 'mensal', 'Negociar']
        for payment in payments:
            row = {'text': payment, 'on_release': lambda x=payment: self.replace_payment(x)}
            menu_itens.append(row)

        self.menu_payment = MDDropdownMenu(
            caller=self.ids.options_payment,
            items=menu_itens,
            position='bottom'
        )

    def replace_payment(self, payment):
        self.ids.text_payment.text_color = 'green'
        self.ids.text_payment.bold = True
        self.ids.text_payment.text = f'{payment}'
        self.ids.options_payment.pos_hint = {'center_x': 0.8, 'center_y': 0.33}

        if payment in 'Negociar':
            self.ids.text_payment.text_color = 'orange'
            self.ids.remunaration.disabled = True

        else:
            self.menu_payment.dismiss()
            self.ids.remunaration.disabled = False


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
            position='bottom'
        )

    def replace_state(self, state):
        self.ids.city.text_color = 'red'
        self.ids.city.text = 'Ausente'
        self.ids.state.text_color = 'green'
        self.ids.state.text = f'{state}'
        self.menu.dismiss()
        self.create_menu(state)

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
            position='bottom'
        )

    def step_one(self):
        # Get all the information
        state = self.ids.state.text
        city = self.ids.city.text
        profession = self.ids.encargo.text
        option_payment = self.ids.text_payment.text
        remunaration = self.ids.remunaration.text

        if state in 'Ausente':
            self.menu.open()
            self.ids.state.text = 'Obrigatorio *'
            return

        if city in 'Ausente':
            self.menu_city.open()
            self.ids.city.text = 'Obrigatorio *'
            return

        if profession in '':
            self.ids.encargo.focus = True
            return

        if option_payment in 'Opções de pagamento':
            self.menu_payment.open()
            return
        else:
            if option_payment in 'Negociar':

                self.step_two()
            else:
                if self.ids.remunaration.text in '':
                    self.ids.remunaration.focus = True
                    return
                else:
                    try:
                        number = self.ids.remunaration.text
                        self.step_two()
                        print('Deu certo')
                    except:
                        self.ids.erro3.text = 'O salario deve ser informado por numeros'

    def step_two(self):
        # Get all the information
        state = self.ids.state.text
        city = self.ids.city.text
        option_payment = self.ids.text_payment.text
        remunaration = self.ids.remunaration.text
        salary = 0
        if option_payment not in 'Negociar':
            salary = int(remunaration)

        # Pass the information to a database
        data = {
            'Contractor': self.contractor,
            'State': state,
            'City': city,
            'Option Payment': option_payment,
            'Salary': salary
        }
        # Make a request to the database passing the dictionary
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions/.json'
        UrlRequest(
            url,
            method='POST',
            req_body=json.dumps(data),
            req_headers={'Content-Type': 'Application/json'},
            on_success=self.finalize
        )

    def finalize(self, req, result):
        progress = self.ids['progress']
        icon_acerto = self.ids['acerto']
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_acerto)
        self.ids.texto_carregando.text = 'Tudo certo!'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .6}
        self.add_widget(self.card)

    def replace_city(self, city):
        self.ids.city.text_color = 'green'
        self.ids.city.text = city
        self.menu_city.dismiss()

    def page(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Functions'
