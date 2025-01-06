from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.function_screen.function_screen import FunctionScreen


class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(FunctionScreen(name='Function'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/function_screen/function_screen.kv')



MainApp().run()
