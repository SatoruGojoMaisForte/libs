from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.list import MDListItemTertiaryText, MDListItemSupportingText, MDListItemHeadlineText, \
    MDListItemLeadingIcon, MDListItem
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class FunctionsScreen(MDScreen):
    contractor = 'Solitude'
    infor = False
    key = ''
    value = ''
    local = ''
    occupation = 'Pedreiro'
    salary = ''

    def on_enter(self, *args):
        self.ids.main_scroll.clear_widgets()
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions'
        UrlRequest(
            f'{url}/.json',
            method='GET',
            on_success=self.functions
        )

    def functions(self, req, result):
        print(result)

        for x, y in result.items():
            for item, value in y.items():
                if item == 'Contractor':
                    if y['Option Payment'] == 'Negociar':
                        list_item = MDListItem(
                            MDListItemLeadingIcon(icon="account-tie"),
                            MDListItemHeadlineText(text=f"{y['occupation']}"),
                            MDListItemSupportingText(text=f"{y['Option Payment']}"),
                            MDListItemTertiaryText(text=f"{y['State']}-{y['City']}")
                        )
                        self.ids.main_scroll.add_widget(list_item)
                    else:
                        list_item = MDListItem(
                            MDListItemLeadingIcon(icon="account-tie"),
                            MDListItemHeadlineText(text=f"{y['occupation']}"),
                            MDListItemSupportingText(text=f"{y['Option Payment']}: R${y['Salary']}"),
                            MDListItemTertiaryText(text=f"{y['State']}-{y['City']}")
                        )
                        self.ids.main_scroll.add_widget(list_item)


    def perfil(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Perfil'

    def page_functions(self):
        self.manager.transition = SlideTransition(direction='left')
        step = self.manager.get_screen('Function')
        step.contractor = self.contractor
        self.manager.current = 'Function'