from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from time import sleep
from kivy.properties import StringProperty
# Carrega as variáveis de ambiente do arquivo .env
import bcrypt

cont = 0


class WriteCode(MDScreen):
    email = StringProperty()

    def on_enter(self):
        # Definindo o ícone de erro para as telas
        icone_erro = MDIconButton(
            icon='alert-circle',
            theme_font_size='Custom',
            font_size='55sp',
            theme_icon_color='Custom',
            pos_hint={'center_x': .5, 'center_y': .6},
            icon_color='red'  # Cor vermelha para representar o erro
        )
        self.ids['error'] = icone_erro

        # Definindo o ícone de acerto para as telas
        icone_acerto = AsyncImage(
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1730504140/image_yvn8lp.png',
            size_hint= (None, None),
            size=("80dp", "150dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            allow_stretch=True
        )
        self.ids['acerto'] = icone_acerto

        # Definindo o MDCard onde vai ficar todo o corpo do layout
        self.card = MDCard(
            id='carregando',
            style='elevated',
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            md_bg_color=(1, 1, 1, 1),
            theme_bg_color="Custom",
            theme_shadow_offset="Custom",
            shadow_offset=(1, -2),
            theme_shadow_softness="Custom",
            shadow_softness=1,
            theme_elevation_level="Custom",
            elevation_level=2
        )
        self.ids['card'] = self.card

        # Definindo o RelativeLayout onde todo o corpo será posicionado
        relative = MDRelativeLayout()
        self.ids['relative'] = relative

        # Definindo o CircularProgressIndicator onde o usuário vai ter o carregamento visual
        circle = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['progress'] = circle

        # Definindo o Label com texto carregando onde o usuário vai ter o indicador visual
        label = MDLabel(
            text='Carregando...',
            font_style='Title',
            halign='center',
            bold=True,
            text_color='black',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        self.card.add_widget(relative)

    def pegando_usuarios(self):
        self.add_widget(self.card)
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'
        UrlRequest(
            f'{url}.json',
            method='GET',
            on_success=self.etapa1
        )

    def etapa1(self, req, result):
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'
        usuarios = result

        # criando um dataframe com os usuarios

        # pegando codigo com index
        indice_usuario = next((k for k, v in usuarios.items() if v.get('email') == self.email), None)
        #
        UrlRequest(
            url=f'{url}/{indice_usuario}.json',
            method='GET',
            on_success=self.etapa2
        )

    def etapa2(self, req, result):
        # definindo as variaveis
        usuario = result
        codigo = self.ids.codigo.text

        # transformando o codigo criptografado em bytes para comparação
        codigo_criptografado = usuario['verification_code'].encode('utf-8')

        # fazendo comparação
        verificando_code = bcrypt.checkpw(codigo.encode('utf-8'), codigo_criptografado)

        if verificando_code:
            self.ids.erros.text = ''
            progress = self.ids['progress']
            icon_acerto = self.ids['acerto']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_acerto)
            self.ids.texto_carregando.text = 'Codigo verificado'
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
            sleep(2)
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'trocar'

        else:
            self.ids.erros.text = 'O codigo digitado e invalido'
            self.remove_widget(self.card)

    def check_text_length(self):
        # Verifica se o campo de código está vazio
        if self.ids.codigo.text == '':
            self.ids.codigo.focus = True
        else:
            text_field = self.ids.codigo
            max_length = 6

            # Remove espaços e limita o comprimento ao valor máximo
            text = text_field.text.replace(' ', '')
            if len(text) > max_length:
                text = text[:max_length]

            # Formata o texto em grupos de 3 caracteres
            formatted_text = ''.join(
                ''.join(text[i:i + 3]) for i in range(0, len(text), 3)
            )

            # Ajusta o campo de texto
            text_field.text = formatted_text
            text_field.halign = 'center'
            text_field.font_size = 40

    def voltar(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Check'


