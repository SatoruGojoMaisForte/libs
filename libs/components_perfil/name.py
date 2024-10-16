from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty


class Name(MDBoxLayout):
    name = StringProperty()

    def atualizar_name(self, novo_nome):
        """Método para atualizar a quantidade de seguidores."""
        self.name = novo_nome