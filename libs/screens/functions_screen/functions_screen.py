from functools import partial

from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItemTertiaryText, MDListItemSupportingText, MDListItemHeadlineText, \
    MDListItemLeadingIcon, MDListItem, MDListItemTrailingIcon, MDListItemTrailingCheckbox
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class FunctionsScreen(MDScreen):
    contractor = StringProperty()
    email = StringProperty()
    telephone = StringProperty()
    company = StringProperty()
    infor = False
    key = ''
    value = ''
    local = ''
    occupation = 'Pedreiro'
    oc = ''
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

        try:
            for x, y in result.items():
                for item, value in y.items():
                    if item == 'Contractor':
                        if y['Contractor'] == self.contractor:
                            if 'label' in self.ids:
                                self.remove_widget(self.ids.label)
                            check = MDListItemTrailingCheckbox(
                                    )

                            print(x)
                            self.ids[y['occupation']] = check
                            check.icon = 'trash-can-outline'
                            check.bind(on_release=partial(self.click, y['occupation'], x))
                            if y['Option Payment'] == 'Negociar':
                                list_item = MDListItem(
                                    MDListItemLeadingIcon(
                                        icon="account-tie"
                                    ),
                                    MDListItemHeadlineText(
                                        text=f"{y['occupation']}",
                                        bold=True,
                                        font_style='Headline',
                                        role='small'
                                    ),
                                    MDListItemSupportingText(
                                        text=f"{y['Option Payment']}"
                                    ),
                                    MDListItemTertiaryText(
                                        text=f"{y['State']}-{y['City']}"
                                    )
                                )
                                self.ids.main_scroll.add_widget(list_item)
                            else:
                                list_item = MDListItem(
                                    MDListItemLeadingIcon(
                                        icon="account-tie"
                                    ),
                                    MDListItemHeadlineText(
                                        text=f"{y['occupation']}",
                                        bold=True,
                                        font_style='Title',
                                        role='medium'
                                    ),
                                    MDListItemSupportingText(
                                        text=f"{y['Option Payment']}: R${y['Salary']}",
                                        font_style='Label',
                                        role='large',
                                        theme_text_color='Custom',
                                        text_color='black'
                                    ),
                                    MDListItemTertiaryText(
                                        text=f"{y['State']} - {y['City']}",
                                        font_style='Label',
                                        role='large',
                                        theme_text_color='Custom',
                                        text_color='black'
                                    ),
                                    check
                                )
                                self.ids.main_scroll.add_widget(list_item)

            if self.ids.main_scroll.children:
                print("O MDBoxLayout tem widgets dentro!")
            else:
                label = MDLabel(
                        text='O contratante não requisitou nenhuma função',
                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                        size_hint_x=0.8,
                        halign='center',
                        theme_text_color='Custom',
                        text_color='grey'
                    )

                self.ids['label'] = label
                self.add_widget(
                    label
                )
        except:
            label = MDLabel(
                text='O contratante não requisitou nenhuma função',
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint_x=0.8,
                halign='center',
                theme_text_color='Custom',
                text_color='grey'
            )

            self.ids['label'] = label
            self.add_widget(
                label
            )

    def click(self, occupation, key, *args):
        self.ids[f'{occupation}'].icon = 'trash-can-outline'
        self.oc = self.ids[f'{occupation}']
        self.delete_function(key)

    def delete_function(self, key):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions/{key}'
        UrlRequest(
            f'{url}/.json',
            method='DELETE',
            on_success=self.final_delete
        )

    def final_delete(self, instance, result):
        self.ids.main_scroll.clear_widgets()
        self.on_enter()


    def perfil(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Perfil'

    def page_functions(self):
        self.manager.transition = SlideTransition(direction='left')
        step = self.manager.get_screen('Function')
        step.contractor = self.contractor
        step.email = self.email
        step.telephone = self.telephone
        step.company = self.company
        self.manager.current = 'Function'