import json
import re
import cloudinary
import cloudinary.uploader
import cloudinary.api
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from android.permissions import request_permissions, check_permission, Permission
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from plyer import filechooser


class EditProfile(MDScreen):
    telefone = '62993683473'
    email = 'viitiinmec@gmail.com'
    company = 'rjporcelanatoliquido'
    name_user = 'Vein do grau'
    dont = 'Não'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        cloudinary.config(
            cloud_name="dsmgwupky",
            api_key="256987432736353",
            api_secret="K8oSFMvqA6N2eU4zLTnLTVuArMU"
        )
        self.key = ''
        self.screen_finalize()

    def on_enter(self, *args):
        self.ids.name_user.text = self.name_user
        self.ids.telefone.text = self.telefone
        self.ids.email.text = self.email
        self.ids.company.text = self.company
        self.check_permissions()

    def check_permissions(self):
        permissions = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]

        def callback(permissions, results):
            if all(results):
                self.on_permissions_granted()
            else:
                self.on_permissions_denied()
    
        if not all(check_permission(p) for p in permissions):
            request_permissions(permissions, callback)
        else:
            self.on_permissions_granted()



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
            self.upload_image(path)
            MDSnackbar(
                MDSnackbarText(
                    text=f"Arquivo selecionado: {path}",
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
            ).open()

    def upload_image(self, image_path):
        try:
            # Upload da imagem
            response = cloudinary.uploader.upload(
                image_path,
                public_id=self.name_user,  # Nome personalizado
                overwrite=True
            )
            # URL da imagem hospedada
            print("URL da imagem:", response['secure_url'])
            self.ids.perfil.source = response['secure_url']
            return response

        except Exception as e:
            print("Erro ao fazer upload:", e)
            return None

    def is_email_valid(self, text: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, text) is not None

    def on_text(self, instance, text):
        email_valid = self.is_email_valid(text)
        if email_valid:
            self.ids.erro2.text = ''
            self.ids.correct2.icon_color = 'green'
            self.ids.correct2.icon = 'check'

        else:
            self.ids.erro2.text = 'Formato invalido!!'
            self.ids.correct2.icon_color = 'red'
            self.ids.correct2.icon = 'alert'

    def on_text_two(self, instance, numero):
        # Remove tudo que não for número
        numero = re.sub(r'\D', '', numero)

        if len(numero) == 11:  # Número com código do país
            self.ids.telefone.text = f"({numero[0:2]}) {numero[2:7]}-{numero[7:]}"
            self.ids.erro1.text = ""
            self.ids.erro1.text = ""
            self.ids.correct1.icon_color = 'green'
            self.ids.correct1.icon = 'check'
        else:
            self.ids.erro1.text = "Número inválido"
            self.ids.correct1.icon_color = 'red'
            self.ids.correct1.icon = 'alert'

    def on_text_three(self, instance, company):
        if company != '':
            self.ids.correct3.icon_color = 'green'
            self.ids.correct3.icon = 'check'

    def on_text_four(self, instance, name):
        if name != '':
            self.ids.erro4.text = ''
            self.ids.correct4.icon_color = 'green'
            self.ids.correct4.icon = 'check'
        else:
            self.ids.erro4.text = 'Campo obrigatorio'
            self.ids.correct4.icon_color = 'red'
            self.ids.correct4.icon = 'alert'

    def step_one(self):
        """Verificar se algum dos campos não estão corretos"""
        print('test')
        if self.ids.telefone.text in '':
            self.ids.telefone.focus = True
            return

        if self.ids.email.text in '':
            self.ids.email.focus = True
            return

        if self.ids.name_user.text in '':
            self.ids.name_user.focus = True
            return

        if self.ids.erro1.text != '':
            self.ids.telefone.focus = True
            return

        if self.ids.erro2.text != '':
            self.ids.email.focus = True
            return

        if self.ids.erro4.text != '':
            self.ids.name_user.focus = True
            return

        self.update_database()

    def update_database(self):
        ''' Agora vamos puxar os dados do firebase'''

        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users'
        UrlRequest(
            url=f'{url}/.json',
            on_success=self.update_database_2,

        )

    def update_database_2(self, req, users):
        for key, value in users.items():

            if value['name'] == self.name_user:
                self.key = key
                self.update_database_3(key)

    def update_database_3(self, key):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{key}'
        if self.ids.company.text in '':
            self.ids.company.text = 'Autonomo'
        data = {'name': self.ids.name_user.text,
                'telefone': self.ids.telefone.text,
                'email': self.ids.email.text,
                'company': self.ids.company.text,
                'perfil': self.ids.perfil.source
                }

        UrlRequest(
            f'{url}/.json',
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.database_sucess
        )

    def database_sucess(self, req, result):
        print(result)
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
        # Passando as informações para a outra tela
        app = MDApp.get_running_app()
        screen_manager = app.root
        perfil = screen_manager.get_screen('Perfil')
        perfil.username = result['name']
        perfil.avatar = result['perfil']
        perfil.regiao = f'{result["state"]}: {result["city"]}'
        perfil.empresa = result['company']
        perfil.zap = result['telefone']
        perfil.email = result['email']
        perfil.contratando = result['hiring']

    def login(self):
        self.manager.transition = SlideTransition(direction='right')
        self.remove_widget(self.card)
        self.manager.current = 'Perfil'
