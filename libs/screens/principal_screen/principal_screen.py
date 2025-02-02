from kivy.properties import Clock, StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class PerfilScreen(MDScreen):
    username = 'HadesKing'
    avatar = 'https://res.cloudinary.com/dsmgwupky/image/upload/v1731366361/image_o6cbgf.png'
    city = 'Sena Madureira'
    state = 'Acre'
    company = 'Amazon'
    telefone = '(62) 99356-0986'
    email = 'viitiinmec@gmail.com'
    contratando = 'Não'

    def on_enter(self, *args):
        self.ids.name.text = self.username
        self.ids.company.text = self.company
        self.ids.email.text = self.email
        self.ids.telefone.text = self.telefone
        self.ids.locate.text = f'{self.state}  -  {self.city}'
        if self.contratando == 'não':
            self.ids.contratando.text_color = 'red'
        else:
            self.ids.contratando.text_color = 'green'
            self.list_posts()

    def list_posts(self):
        # Simula a carga de postagens
        Clock.schedule_once(lambda dt: self.update_posts())

    def update_posts(self):
        pass

    def page(self):
        self.manager.current = 'Function'

    def functions(self):
        if self.contratando == 'Sim':
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
        self.manager.current = 'EditProfile'

