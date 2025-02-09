from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

from kivymd.app import MDApp


class CirclePerfis(MDCard):
    avatar = StringProperty()
    name = StringProperty()

    def perfil(self):
        # Passa informações para a tela de perfil
        app = MDApp.get_running_app()
        screen_manager = app.root
        perfil_screen = screen_manager.get_screen('outros')
        perfil_screen.avatar = self.avatar
        perfil_screen.username = self.name

        # Muda para a tela de perfil
        screen_manager.current = 'outros'
