from kivy.properties import Clock
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen


class PerfilScreen(MDScreen):
    username = 'Senhor messias'
    avatar = 'https://res.cloudinary.com/dsmgwupky/image/upload/v1731366650/image_yljvww.png'
    regiao = 'GO - Aparecida de Goiania'
    empresa = 'Porcelanato Liquido'
    zap = '(62) 99368-3473'
    email = 'viitiinmec@gmail.com'
    contratando = 'Sim'

    def on_enter(self, *args):
        if self.contratando == 'Não':
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

