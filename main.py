from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from libs.screens.Cadastro.cadastro import Cadastro


class PrincipalApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = ScreenManager()
        self.screenmanager.add_widget(Cadastro(name='cadastro'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/Cadastro/cadastro.kv')

PrincipalApp().run()
