import json
import os
import re
import cloudinary
import cloudinary.uploader
import cloudinary.api
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from plyer import filechooser
from PIL import Image, ImageDraw
from kivy.core.window import Window


class EditProfile(MDScreen):
    telefone = '62993683473'
    email = 'viitiinmec@gmail.com'
    company = 'rjporcelanatoliquido'
    name_user = 'KingHades'
    dont = 'Sim'
    avatar = 'https://res.cloudinary.com/dsmgwupky/image/upload/v1731366361/image_o6cbgf.png'

    # Funções de inicialização -----------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.softinput_mode = 'below_target'
        Window.bind(on_keyboard=self.events)
        Window.bind(on_keyboard_height=self.on_keyboard_height)
        self.keyboard_height = 0
        self.manager_open = False
        cloudinary.config(
            cloud_name="dsmgwupky",
            api_key="256987432736353",
            api_secret="K8oSFMvqA6N2eU4zLTnLTVuArMU"
        )
        self.key = ''
        self.screen_finalize()

    def on_enter(self):
        self.on_text_two(self, self.telefone)

    # Inicializando tela de finalização de atualização dos dados -------------------------------------------------------
    def screen_finalize(self):
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
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1736292941/true-fotor-20250107203414-removebg-preview_ajd1xd.png',
            size_hint=(None, None),
            size=("100dp", "150dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
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
            pos_hint={'center_x': .5, 'center_y': .7}
        )
        self.ids['progress'] = circle

        # Definindo o Label com texto carregando onde o usuário vai ter o indicador visual
        label = MDLabel(
            text='Carregando...',
            font_style='Headline',
            role='medium',
            halign='center',
            bold=True,
            text_color='black',
            pos_hint={'center_x': .5, 'center_y': .9}
        )
        label_2 = MDLabel(
            text='Os dados do seu perfil ja foram devidamene alterados',
            font_style='Title',
            role='small',
            halign='center',
            bold=False,
            text_color='gray',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        botton = MDButton(
            MDButtonText(
                text='Ok',
                theme_text_color='Custom',
                text_color='black',
                font_style='Title',
                role='medium',
                halign='center',
                bold=True,
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
            ),
            theme_bg_color='Custom',
            md_bg_color=(0.0, 1.0, 0.0, 1.0),
            pos_hint={'center_x': .5, 'center_y': .35},
            style='tonal',
            theme_width='Custom',
            size_hint_x=.4,

        )
        self.ids['ok'] = botton
        self.ids.ok.on_release = self.login
        relative.add_widget(botton)
        relative.add_widget(icone_acerto)
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        relative.add_widget(label_2)
        self.card.add_widget(relative)

    # Funções de teclado -----------------------------------------------------------------------------------------------

    def on_keyboard_height(self, window, height):
        """
        Método chamado quando a altura do teclado muda.
        """
        self.keyboard_height = height
        if height == 0:  # Teclado fechado
            self.pos = (0, 0)  # Volta a interface para a posição original
        else:  # Teclado aberto
            # Aumenta a posição vertical dos elementos, deslocando-os para cima
            self.pos = (0, height * 0.1)

    def on_touch_down(self, touch):
        """
        Fecha o teclado quando o usuário toca fora do campo de texto.
        """
        if self.keyboard_height > 0:  # Teclado está aberto
            # Verifica se o toque foi fora do campo de texto
            if not self.ids.email.collide_point(*touch.pos) and not self.ids.name_user.collide_point(*touch.pos):
                self.ids.email.focus = False
                self.ids.name_user.focus = False
                self.pos = (0, 0)  # Volta a interface para a posição original
        return super().on_touch_down(touch)

    def events(self, window, key, scancode, codepoint, modifier):
        """
        Método chamado quando uma tecla é pressionada.
        """
        if key == 27:  # Tecla ES C (fechar teclado)
            self.pos = (0, 0)  # Volta a interface para a posição original
            return True
        return False

    def scroll_to_widget(self, widget):
        """Rola a tela para mostrar o widget ao focar nele."""

        def _scroll(*args):
            scrollview = self.ids.get("scroll")
            if scrollview:
                # Calcula a altura do teclado
                keyboard_height = Window.keyboard_height * Window.height
                widget_y = widget.to_window(*widget.pos)[1]  # Posição do widget na tela

                # Se o widget estiver abaixo do teclado, rola para cima
                if widget_y < keyboard_height + dp(50):
                    scrollview.scroll_y = max(0, 1 - (keyboard_height / Window.height))

        Clock.schedule_once(_scroll, 0.1)

    # Funções de imagem ------------------------------------------------------------------------------------------------

    def recortar_imagem_circular(self, imagem_path):
        try:
            # Upload da imagem com corte circular
            response = cloudinary.uploader.upload(
                imagem_path,
                public_id=self.name_user,
                overwrite=True,
                transformation=[
                    {'width': 1000, 'height': 1000, 'crop': 'thumb', 'gravity': 'face', 'radius': 'max'}
                ]
            )
            self.ids.perfil.source = response['secure_url']  # Retorna o URL da imagem cortada
        except Exception as e:
            print(f"Erro ao cortar a imagem: {e}")
            return None

    def open_gallery(self):
        if self.dont == 'Não':
            print('Galeria não atualizada')
        else:
            '''Abre a galeria para selecionar uma imagem.'''
            try:
                filechooser.open_file(
                    filters=["*.jpg", "*.png", "*.jpeg"],  # Filtra por tipos de arquivo de imagem
                    on_selection=self.select_path  # Chama a função de callback ao selecionar o arquivo
                )
            except Exception as e:
                print("Erro ao abrir a galeria:", e)

    def select_path(self, selection):
        '''
        Callback chamada quando um arquivo é selecionado.

        :param selection: lista contendo o caminho do arquivo selecionado.
        '''
        if selection:
            path = selection[0]  # Obtém o caminho do arquivo
            self.recortar_imagem_circular(path)
            MDSnackbar(
                MDSnackbarText(
                    text=f"Arquivo selecionado: {path}",
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
            ).open()

    # Funções de permissão ---------------------------------------------------------------------------------------------
    def on_permissions_granted(self):
        """
        Ações a serem executadas se as permissões forem concedidas.
        """
        print("Permissões concedidas, execute a funcionalidade necessária.")
        self.ids.image_perfil.text = 'Editar foto de perfil'
        self.ids.perfil.source = 'https://res.cloudinary.com/dsmgwupky/image/upload/c_crop,g_face,w_300,h_300/r_max/v1736891104/Vein%20do%20grau.jpg'

    def on_permissions_denied(self):
        """
        Ações a serem executadas se as permissões forem negadas.
        """
        print("Permissões negadas, mostre uma mensagem ou desative a funcionalidade.")
        self.ids.image_perfil.text = 'Função bloqueada'
        self.ids.perfil.source = 'https://res.cloudinary.com/dsmgwupky/image/upload/v1726685784/a8da222be70a71e7858bf752065d5cc3-fotor-20240918154039_dokawo.png'
        self.ids.botton_perfil.disabled = True

    # Funções de formatação --------------------------------------------------------------------------------------------
    def is_email_valid(self, text: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, text) is not None


    def on_text_two(self, instance, numero):
        # Remove tudo que não for número
        numero = re.sub(r'\D', '', numero)

        if len(numero) == 11:  # Número com código do país
            self.ids.telefone.text = f"({numero[0:2]}) {numero[2:7]}-{numero[7:]}"
            self.ids.erro1.text = ""
            self.ids.erro1.text = ""
            self.ids.telefone.focus = False
        else:
            self.ids.erro1.text = "Número inválido"

    def step_one(self):
        """Verificar se algum dos campos não estão corretos"""

        if self.ids.telefone.text in '' or self.ids.erro1.text != '':
            self.ids.telefone.focus = True
            return

        if self.ids.email.text in '':
            self.ids.email.focus = True
            return

        if self.ids.name_user.text in '':
            self.ids.name_user.focus = True
            return

        if self.ids.erro2.text != '' and self.ids.erro2.text != 'Formato de email invalido':
            self.ids.email.focus = True
            return

        if self.ids.erro4.text != '':
            self.ids.name_user.focus = True
            return

        email = self.ids.email.text
        valid = self.is_email_valid(email)
        print(valid)
        if valid:
            self.ids.erro2.text = ''
            print('Chamando Função')
            self.update_database()
        else:
            self.ids.erro2.text = 'Formato de email invalido'

    # Manipulando banco de dados ---------------------------------------------------------------------------------------
    def update_database(self):
        ''' Agora vamos puxar os dados do firebase'''
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users'
        UrlRequest(
            url=f'{url}/.json',
            on_success=self.update_database_2,
        )

    def update_database_2(self, req, users):
        print('Verificando os dados')
        for key, value in users.items():

            if value['name'] == self.name_user:
                self.key = key
                self.update_database_3(key)
            else:
                print('Usuario encontrado')

    def update_database_3(self, key):
        print('update')
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{key}'

        data = {'name': self.ids.name_user.text,
                'email': self.ids.email.text,
                'perfil': self.ids.perfil.source,
                'telefone': self.ids.telefone.text
                }

        UrlRequest(
            f'{url}/.json',
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.database_sucess
        )

    def database_sucess(self, req, result):
        print(result)
        print('data')
        progress = self.ids['progress']
        self.ids['relative'].remove_widget(progress)
        self.ids.texto_carregando.text = 'Tudo certo!'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .6}
        self.add_widget(self.card)
        self.data()

    def data(self):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{self.key}'
        UrlRequest(
            url=f'{url}/.json',
            on_success=self.get_data,
        )

    def get_data(self, req, result):
        print('Ola')

    # Retornando a tela a de Login -------------------------------------------------------------------------------------
    def login(self):
        self.manager.transition = SlideTransition(direction='right')
        self.remove_widget(self.card)
        self.manager.current = 'Perfil'
