from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.permission_screen.permission_screen import PermissionScreen
from libs.screens.permission_denied.permission_denied import PermissionDenied
from libs.screens.edit_profile.edit_profile import EditProfile


class MainApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(PermissionScreen(name='Permission'))
        self.screenmanager.add_widget(PermissionDenied(name='Denied'))
        self.screenmanager.add_widget(EditProfile(name='EditProfile'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/permission_screen/permission_screen.kv')
        Builder.load_file('libs/screens/permission_denied/permission_denied.kv')
        Builder.load_file('libs/screens/edit_profile/edit_profile.kv')



MainApp().run()
