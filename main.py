from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.screens.login_screen.loginscreen import LoginScreen
from libs.screens.Cadastro.cadastro import Cadastro
from libs.screens.check_code.checkcode import CheckCode
from libs.screens.send_code.sendcode import SendCode

class PrincipalApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = ScreenManager()

        self.screenmanager.add_widget(LoginScreen(name='Login'))
        self.screenmanager.add_widget(Cadastro(name='cadastro'))
        self.screenmanager.add_widget(SendCode(name='Send'))
        self.screenmanager.add_widget(CheckCode(name='Check'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/login_screen/loginscreen.kv')
        Builder.load_file('libs/screens/Cadastro/cadastro.kv')
        Builder.load_file('libs/screens/send_code/sendcode.kv')
        Builder.load_file('libs/screens/check_code/checkcode.kv')


PrincipalApp().run()
