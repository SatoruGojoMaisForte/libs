from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.permission_screen.permission_screen import PermissionScreen

class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(PermissionScreen(name='Permission'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/permission_screen/permission_screen.kv')



MainApp().run()
