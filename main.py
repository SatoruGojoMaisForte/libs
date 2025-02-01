from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
#from libs.screens.permission_denied.permission_denied import PermissionDenied
#from libs.screens.permission_screen.permission_screen import PermissionScreen
#from libs.screens.confirm_permissions.confirm_permissions import ConfirmPermissions
from libs.screens.edit_profile.edit_profile import EditProfile


class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        Window.keyboard_mode = 'pan'
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(EditProfile(name='EditProfile'))
        #self.screenmanager.add_widget(PermissionScreen(name='Permission'))
        #self.screenmanager.add_widget(PermissionDenied(name='Denied'))
        #self.screenmanager.add_widget(ConfirmPermissions(name='Confirm'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/permission_denied/permission_denied.kv')
        Builder.load_file('libs/screens/permission_screen/permission_screen.kv')
        Builder.load_file('libs/screens/confirm_permissions/confirm_permissions.kv')
        Builder.load_file('libs/screens/edit_profile/edit_profile.kv')


MainApp().run()
