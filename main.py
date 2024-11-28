from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.screens.home_page.homepage import HomePage


class PrincipalApp(MDApp):

    def build(self):
        Window.size = (400, 700)
        self.load_all_kv_files()

        self.screenmanager = ScreenManager()
        self.screenmanager.add_widget(HomePage(name='homepage'))

        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/home_page/homepage.kv')
        Builder.load_file('libs/components/circle_perfil.kv')
        Builder.load_file('libs/components/navigations_buttons,kv')
        Builder.load_file('libs/components/post_cards.kv')
        Builder.load_file('libs/components/story_creator.kv')


PrincipalApp().run()
