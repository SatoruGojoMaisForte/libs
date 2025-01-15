from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.confirm_permissions.confirm_permissions import ConfirmPermissions


class MainApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(ConfirmPermissions(name='Confirm'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/confirm_permissions/confirm_permissions.kv')


MainApp().run()
