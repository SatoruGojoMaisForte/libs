from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.principal_screen.principal_screen import PerfilScreen
from libs.screens.edit_profile.edit_profile import EditProfile

class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(EditProfile(name="EditProfile"))
        self.screenmanager.add_widget(PerfilScreen(name='Perfil'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/principal_screen/principal_screen.kv')
        Builder.load_file('libs/components/post_cards.kv')
        Builder.load_file('libs/components/navigations_buttons.kv')
        Builder.load_file('libs/screens/edit_profile/edit_profile.kv')



MainApp().run()
