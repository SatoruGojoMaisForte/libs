from kivy.uix.screenmanager import SlideTransition
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.navigationbar.navigationbar import MDNavigationBar
from kivymd.app import MDApp


class NavigationsButtons(MDNavigationBar):
    avatar = StringProperty()
    nome = StringProperty()
    table = BooleanProperty()

    def bricklayer(self):
        self.table = True  # Define que o item "table" está ativo
        self.update_navigation()
        app = MDApp.get_running_app()
        screen_manager = app.root
        screen_manager.transition = SlideTransition(direction='right')
        bricklayer = screen_manager.get_screen('Table')
        bricklayer.username = self.nome
        screen_manager.current = 'Table'

    def sign_up(self):
        app = MDApp.get_running_app()
        screen_manager = app.root
        screen_manager.transition = SlideTransition(direction='left')
        sign_up = screen_manager.get_screen('SignUp')
        sign_up.avatar = self.avatar
        sign_up.nome = self.nome
        screen_manager.current = 'SignUp'

    def passo(self):
        self.table = False  # Define que o item "perfil" está ativo
        self.update_navigation()
        app = MDApp.get_running_app()
        screen_manager = app.root
        bricklayer = screen_manager.get_screen('Table')
        bricklayer.table = False
        screen_manager.transition = SlideTransition(direction='left')
        perfil = screen_manager.get_screen('Perfil')
        screen_manager.current = 'Perfil'

    def update_navigation(self):
        # Atualiza o estado de active para refletir o valor atual de self.table
        self.ids.table.active = self.table
        self.ids.perfil.active = not self.table
