from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class Seguidores(MDCard):
    seguidores = StringProperty()


    def atualizar_seguidores(self, novos_seguidores):
        """Método para atualizar a quantidade de seguidores."""
        self.seguidores = novos_seguidores