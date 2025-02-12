from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.list import MDListItemTertiaryText, MDListItemSupportingText, MDListItemHeadlineText, \
    MDListItemLeadingIcon, MDListItem
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class FunctionsScreen(MDScreen):
    contractor = 'Waldir'
    infor = False
    key = ''
    value = ''
    local = ''
    occupation = 'Pedreiro'
    salary = ''
    adicionado = 0

    def on_enter(self, *args):
        self.adicionado += 1
        if self.adicionado == 1:
            url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions'
            UrlRequest(
                f'{url}/.json',
                method='GET',
                on_success=self.functions
            )
        else:
            self.adicionado = 0
            self.ids.main_scroll.clear_widgets()
            url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions'
            UrlRequest(
                f'{url}/.json',
                method='GET',
                on_success=self.functions
            )

    def functions(self, req, result):
        print(result)

        for key, item in result.items():
            if isinstance(item, dict):
                for sub_key, sub_value in item.items():
                    if sub_key == 'contractor':
                        if sub_value == self.contractor:
                            self.infor = True
                    if sub_key == 'value' and self.infor == True:
                        self.value = sub_value

                    if sub_key == 'function' and self.infor == True:
                        self.occupation = sub_value

                    if sub_key == 'wage' and self.infor == True:
                        if sub_value == 'undertakes':
                            self.salary = 'Empreita: '
                        else:
                            if self.infor == True:
                                self.salary = 'Diaria: '

                    if sub_key == 'location' and self.infor == True:
                        self.local = sub_value

                list = MDListItem(
                    MDListItemLeadingIcon(
                        icon="account-tie",
                    ),
                    MDListItemHeadlineText(
                        text=f"{self.occupation}",
                    ),
                    MDListItemSupportingText(
                        text=f"{self.salary}R${self.value}",
                    ),
                    MDListItemTertiaryText(
                        text=f'{self.local}',
                    ),
                )
                self.ids.main_scroll.add_widget(list)

    def perfil(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Perfil'

    def page_functions(self):
        self.manager.transition = SlideTransition(direction='left')
        step = self.manager.get_screen('Function')
        step.contractor = self.contractor
        self.manager.current = 'Function'