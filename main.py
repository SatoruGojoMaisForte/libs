from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.screens.login_screen.loginscreen import LoginScreen


class PrincipalApp(MDApp):

    def build(self):
        Window.size = (400, 700)
        self.load_all_kv_files()

        self.screenmanager = ScreenManager()
        self.screenmanager.add_widget(LoginScreen(name='Login'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/login_screen/loginscreen.kv')



PrincipalApp().run()
