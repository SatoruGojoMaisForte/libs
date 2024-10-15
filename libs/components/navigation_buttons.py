from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

from KivyMD.kivymd.app import MDApp
from libs.screens.login_screen.loginscreen import LoginScreen


class NavigationsButtons(MDBoxLayout):
    avatar = StringProperty()

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

