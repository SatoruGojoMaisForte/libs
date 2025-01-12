from kivy.properties import Clock, StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen


class PerfilScreen(MDScreen):
    username = StringProperty()
    avatar = StringProperty()
    regiao = StringProperty()
    empresa = StringProperty()
    zap = StringProperty()
    email = StringProperty()
    contratando = StringProperty()

    def on_enter(self, *args):
        if self.contratando == 'não':
            self.ids.contratando.text_color = 'red'
        else:
            self.ids.contratando.text_color = 'green'
            self.list_posts()

    def list_posts(self):
        # Simula a carga de postagens
        Clock.schedule_once(lambda dt: self.update_posts())

    def update_posts(self):
        pass

    def page(self):
        self.manager.current = 'Function'

    def functions(self):
        if self.contratando == 'Sim':
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'Functions'

    def edit_profile(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'EditProfile'

