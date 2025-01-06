import json
import urllib

import requests
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.label import MDLabel
from kivy.network.urlrequest import UrlRequest
from pyUFbr.baseuf import ufbr
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
        payments = ['Diaria', 'semanal', 'mensal']
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
        self.ids.text_payment.text = f'{payment}'
        self.ids.options_payment.pos_hint = {'center_x': 0.8, 'center_y': 0.33}

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

    def replace_city(self, city):
        self.ids.city.text_color = 'green'
        self.ids.city.text = city

    def page(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Functions'
