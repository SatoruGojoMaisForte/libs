from kivy.properties import get_color_from_hex
from kivymd.uix.screen import MDScreen


class EditProfileEmployee(MDScreen):

    def on_enter(self, *args):
        media = 0.5  # Exemplo de nota
        full_stars = int(media)  # Quantidade de estrelas cheias
        half_star = media - full_stars >= 0.5  # Verifica se tem meia estrela

        star_icons = []  # La para armazenar os íconesist

        # Adiciona estrelas cheias
        for _ in range(full_stars):
            star_icons.append("star")

        # Adiciona meia estrela (se houver)
        if half_star:
            star_icons.append("star-half-full")

        # Completa o restante com estrelas vazias
        while len(star_icons) < 5:
            star_icons.append("star-outline")
        numb = 0
        if media <= 1:
            self.ids.number_one.icon_color = 'red'
            self.ids.number_two.icon_color = 'red'
            self.ids.number_three.icon_color = 'red'
            self.ids.number_one.icon_color = 'red'
            self.ids.number_two.icon_color = 'red'
            self.ids.number_four.icon_color = 'red'
            self.ids.number_five.icon_color = 'red'

        elif media <= 2:
            self.ids.number_two.icon_color = get_color_from_hex('#FF8000')
            self.ids.number_three.icon_color = get_color_from_hex('#FF8000')
            self.ids.number_one.icon_color = get_color_from_hex('#FF8000')
            self.ids.number_two.icon_color = get_color_from_hex('#FF8000')
            self.ids.number_four.icon_color = get_color_from_hex('#FF8000')
            self.ids.number_five.icon_color = get_color_from_hex('#FF8000')

        elif media <= 3:
            self.ids.number_three.icon_color = get_color_from_hex('#FFE600')
            self.ids.number_one.icon_color = get_color_from_hex('#FFE600')
            self.ids.number_two.icon_color = get_color_from_hex('#FFE600')
            self.ids.number_four.icon_color = get_color_from_hex('#FFE600')
            self.ids.number_five.icon_color = get_color_from_hex('#FFE600')

        elif media <= 4:
            self.ids.number_three.icon_color = get_color_from_hex('#32CD32')
            self.ids.number_one.icon_color = get_color_from_hex('#32CD32')
            self.ids.number_two.icon_color = get_color_from_hex('#32CD32')
            self.ids.number_four.icon_color = get_color_from_hex('#32CD32')
            self.ids.number_five.icon_color = get_color_from_hex('#32CD32')

        else:
            self.ids.number_three.icon_color = get_color_from_hex('#007BFF')
            self.ids.number_one.icon_color = get_color_from_hex('#007BFF')
            self.ids.number_two.icon_color = get_color_from_hex('#007BFF')
            self.ids.number_four.icon_color = get_color_from_hex('#007BFF')
            self.ids.number_five.icon_color = get_color_from_hex('#007BFF')

        for x in star_icons:
            numb += 1
            if numb == 1:
                self.ids.number_one.icon = x
            elif numb == 2:
                self.ids.number_two.icon = x
            elif numb == 3:
                self.ids.number_three.icon = x
            elif numb == 4:
                self.ids.number_four.icon = x
            else:
                self.ids.number_five.icon = x