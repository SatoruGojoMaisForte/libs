from kivy.properties import StringProperty
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class TableScreen(MDScreen):
    cont = 0
    username = StringProperty()
    adicionado = 0
    def on_enter(self):
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
                lista = MDListItem(
                    MDListItemLeadingAvatar(
                        source=info['avatar']
                    ),
                    MDListItemHeadlineText(
                        text=info['Name']
                    ),
                    MDListItemSupportingText(
                        text=info['function']
                    )
                )
                self.ids.main_scroll.add_widget(lista)
                self.cont += 1

        self.ids.counter.text = f'{self.cont} funcionarios contratados'

