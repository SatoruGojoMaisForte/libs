from kivymd.uix.card import MDCard
from kivy.properties import StringProperty


class Bio(MDCard):
    bio = StringProperty()

    def atualizar_bio(self, nova_bio):
        """Método para atualizar a quantidade de seguidores."""
        self.bio = nova_bio