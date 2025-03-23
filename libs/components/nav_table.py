from kivy.properties import StringProperty
from kivymd.uix.navigationbar.navigationbar import MDNavigationBar


class Navigations(MDNavigationBar):
    avatar = StringProperty()
    nome = StringProperty()
    table = False

    def perfil(self):
        pass
    def home(self):
        pass

    def bricklayer(self):
        pass

    def sign_up(self):
        pass

    def passo(self):
        pass
