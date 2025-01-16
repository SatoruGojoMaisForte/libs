from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.confirm_permissions.confirm_permissions import ConfirmPermissions
from libs.screens.edit_profile.edit_profile import EditProfile
from libs.screens.permission_denied.permission_denied import PermissionDenied
from libs.screens.permission_screen.permission_screen import PermissionScreen


class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(PermissionScreen(name='Permission'))
        self.screenmanager.add_widget(ConfirmPermissions(name='Confirm'))
        self.screenmanager.add_widget(EditProfile(name='EditProfile'))
        self.screenmanager.add_widget(PermissionDenied(name='Denied'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/edit_profile/edit_profile.kv')
        Builder.load_file('libs/screens/confirm_permissions/confirm_permissions.kv')
        Builder.load_file('libs/screens/permission_denied/permission_denied.kv')
        Builder.load_file('libs/screens/permission_screen/permission_screen.py')


MainApp().run()
