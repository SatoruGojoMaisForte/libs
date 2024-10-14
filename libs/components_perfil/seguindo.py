from kivymd.uix.card import MDCard
from kivy.properties import StringProperty


class Seguindo(MDCard):
    seguindo = StringProperty()

    def atualizar_seguindo(self, numero_seguindo):
        """Método para atualizar a quantidade de seguidores."""
        self.seguindo = numero_seguindo