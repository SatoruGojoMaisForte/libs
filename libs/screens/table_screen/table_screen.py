from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar, MDListItemHeadlineText, MDListItemSupportingText, \
    MDListItemTertiaryText

from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class TableScreen(MDScreen):
    cont = 0
    username = StringProperty()
    adicionado = 0
    table = BooleanProperty()

    def on_enter(self):
        self.ids.navigation.table = True
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios'
        self.adicionado += 1
        if self.adicionado == 1:
            UrlRequest(
                f'{url}/.json',
                method='GET',
                on_success=self.load_employees
            )
        else:
            self.ids.main_scroll.clear_widgets()
            self.cont = 0
            UrlRequest(
                f'{url}/.json',
                method='GET',
                on_success=self.load_employees
            )

    def load_employees(self, req, result):
        # Definindo o mdlist -------------------------------

        for employees, info in result.items():
            if info['contractor'] == self.username:
                self.cont += 1
                lista = MDListItem(
                    MDListItemLeadingAvatar(
                        source=info['avatar']
                    ),
                    MDListItemHeadlineText(
                        text=info['Name']
                    ),
                    MDListItemSupportingText(
                        text=info['function']
                    ),
                    MDListItemTertiaryText(
                        text=info['method_salary']
                    )
                )
                inf = info
                lista.bind(on_release=lambda instance, info=inf: self.show_employee_details(info))
                self.ids.main_scroll.add_widget(lista)
        self.ids.counter.text = f'{self.cont} funcionarios contratados'

    def show_employee_details(self, info):
        # Obtendo o gerenciador de telas
        print(info)
        detail_screen = self.manager.get_screen("Evaluation")
        detail_screen.employee_name = info['Name']
        detail_screen.employee_function = info['function']
        detail_screen.avatar = info['avatar']
        detail_screen.salary = info['salary']
        detail_screen.method_salary = info['method_salary']
        detail_screen.punctuality = info['punctuality']
        detail_screen.coexistence = info['coexistence']
        detail_screen.efficiency = info['efficiency']
        detail_screen.scale = info['scale']
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "Evaluation"

    # chama a tela de cadastrar funcionarios
    def add_screen(self):
        self.manager.transition = SlideTransition(direction='left')
        app = MDApp.get_running_app()
        screen_manager = app.root
        perfil = screen_manager.get_screen('Add')
        perfil.contractor = self.username
        self.manager.current = 'Add'
