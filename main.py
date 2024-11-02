from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.screens.login_screen.loginscreen import LoginScreen
from libs.screens.Cadastro.cadastro import Cadastro
from libs.screens.check_code.checkcode import CheckCode
from libs.screens.send_code.sendcode import SendCode
from libs.screens.write_code.writecode import WriteCode
from libs.screens.Trocar_senha.trocarsenha import TrocarSenha
class PrincipalApp(MDApp):

    def build(self):
        Window.size = (400, 800)
        self.load_all_kv_files()
        self.screenmanager = ScreenManager()

        self.screenmanager.add_widget(LoginScreen(name='Login'))
        self.screenmanager.add_widget(Cadastro(name='cadastro'))
        self.screenmanager.add_widget(SendCode(name='Send'))
        self.screenmanager.add_widget(CheckCode(name='Check'))
        self.screenmanager.add_widget(WriteCode(name='Write'))
        self.screenmanager.add_widget(TrocarSenha(name='trocar'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/login_screen/loginscreen.kv')
        Builder.load_file('libs/screens/Cadastro/cadastro.kv')
        Builder.load_file('libs/screens/send_code/sendcode.kv')
        Builder.load_file('libs/screens/check_code/checkcode.kv')
        Builder.load_file('libs/screens/write_code/writecode.kv')
        Builder.load_file('libs/screens/Trocar_senha/trocarsenha.kv')

PrincipalApp().run()
