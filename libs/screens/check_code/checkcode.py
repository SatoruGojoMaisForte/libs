from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen


class CheckCode(MDScreen):
    email = StringProperty()

    def call_send_code(self, *args):
        self.manager.current = ("Send")

    def call_write_code(self, *args):
        write = self.manager.get_screen('Write')
        write.email = self.email
        self.manager.current = 'Write'

    def color_background(self):
        if self.theme_cls.theme_style == 'Dark':
            return 1, 1, 1, 0
        else:
            return 1, 1, 1, 1

    def icon_tema(self):
        if self.theme_cls.theme_style == 'Light':
            return "https://raw.githubusercontent.com/SatoruGojoMaisForte/logos/main/images_code/claro.png"
        else:
            return "https://raw.githubusercontent.com/SatoruGojoMaisForte/logos/main/images_code/escuro.png"

