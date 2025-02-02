from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.edit_profile.edit_profile import EditProfile
from libs.screens.edit_profile_two.edit_profile_two import EditProfileTwo
from libs.screens.principal_screen.principal_screen import PerfilScreen
from kivy.core.window import Window


class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(PerfilScreen(name='Perfil'))
        self.screenmanager.add_widget(EditProfile(name='EditProfile'))
        self.screenmanager.add_widget(EditProfileTwo(name='EditProfileTwo'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/edit_profile/edit_profile.kv')
        Builder.load_file('libs/screens/principal_screen/principal_screen.kv')
        Builder.load_file('libs/screens/edit_profile_two/edit_profile_two.kv')


MainApp().run()
