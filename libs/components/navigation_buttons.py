from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

from kivymd.app import MDApp


class NavigationsButtons(MDBoxLayout):
    avatar = StringProperty()
    nome = StringProperty()

    def perfil(self):
        app = MDApp.get_running_app()
        screen_manager = app.root
        perfil_screen = screen_manager.get_screen('perfilpage')
        perfil_screen.avatar = self.avatar
        screen_manager.current = 'perfilpage'

    def home(self):
        app = MDApp.get_running_app()
        screen_manager = app.root
        screen_manager.current = 'homepage'

    def bricklayer(self):
        print(self.nome)
        app = MDApp.get_running_app()
        screen_manager = app.root
        bricklayer = screen_manager.get_screen('Bricklayer')
        bricklayer.avatar = self.avatar
        bricklayer.nome = self.nome
        screen_manager.current = 'Bricklayer'

    def sign_up(self):
        app = MDApp.get_running_app()
        screen_manager = app.root
        screen_manager.transition = SlideTransition(direction='left')
        sign_up = screen_manager.get_screen('SignUp')
        sign_up.avatar = self.avatar
        sign_up.nome = self.nome
        screen_manager.current = 'SignUp'
