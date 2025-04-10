from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class PerfilScreen(MDScreen):
    username = StringProperty()
    avatar = StringProperty()
    city = StringProperty()
    state = StringProperty()
    company = StringProperty()
    telefone = StringProperty()
    email = StringProperty()
    contratando = 'Sim'
    function = StringProperty()
    adicionado = 0
    cont = 0
    table = BooleanProperty(False)

    def on_enter(self, *args):
        self.ids.navigation.table = False
        self.ids.perfil.source = self.avatar
        self.ids.username.text = self.username
        self.ids.company.text = self.company
        if 'Não definido' in (self.city, self.state):
            self.ids.locate.text = f'Não definido'
        else:
            self.ids.locate.text = f'{self.city}, {self.state}'
        self.ids.function.text = f'{self.function}'
        self.ids.telefone.text = f'{self.telefone}'
        self.ids.email.text = f'{self.email}'

    def page(self):
        self.manager.current = 'Function'

    def functions(self):
        if self.contratando == 'Sim':
            self.manager.transition = SlideTransition(direction='left')
            app = MDApp.get_running_app()
            screen_manager = app.root
            edit = screen_manager.get_screen('Functions')
            edit.contractor = self.username
            edit.occupation = self.function
            edit.email = self.email
            edit.telephone = self.telefone
            edit.company = self.company
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'Functions'

    def edit_profile(self):
        self.manager.transition = SlideTransition(direction='left')
        app = MDApp.get_running_app()
        screen_manager = app.root
        edit = screen_manager.get_screen('EditProfile')
        edit.name_user = self.username
        edit.email = self.email
        edit.telefone = self.telefone
        edit.state = self.state
        edit.city = self.city
        edit.company = self.company
        edit.avatar = self.avatar
        edit.function = self.function
        self.manager.current = 'EditProfile'
