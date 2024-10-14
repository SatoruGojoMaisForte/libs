import requests
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from libs.screens.home_page.homepage import HomePage
from libs.screens.Cadastro.cadastro import Cadastro
from libs.screens.perfil_page.perfilpage import PerfilPage
from libs.screens.outros_perfis_page.outrospage import OutrosPage

class PrincipalApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = ScreenManager()
        self.screenmanager.add_widget(Cadastro(name=''))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/Cadastro/cadastro.kv')

PrincipalApp().run()
