import json
import re

import cloudinary
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, get_color_from_hex
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from plyer import filechooser


class EditEmployee(MDScreen):
    employee_name = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    avatar = StringProperty()
    key = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()
    dont = 'Sim'
    # Constants
    FIREBASE_URL = 'https://obra-7ebd9-default-rtdb.firebaseio.com'
    CLOUDINARY_CONFIG = {
        "cloud_name": "dsmgwupky",
        "api_key": "256987432736353",
        "api_secret": "K8oSFMvqA6N2eU4zLTnLTVuArMU"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cloudinary configuration
        cloudinary.config(**self.CLOUDINARY_CONFIG)
        self.menu_functions()

    def on_enter(self):
        self.ids.name_user.text = f'{self.employee_name}'
        self.ids.perfil.source = self.avatar
        ids = {'email': self.employee_mail,
                'telefone': self.employee_telephone,
                'function': self.employee_function
               }
        print(self.ids)
        for key, valor in ids.items():
            if valor not in 'Não definido':
                print(valor)
                self.ids[key].text = f'{valor}'


    def menu_functions(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['Mestre de obra', 'Engenheiro-civil', 'Pedreiro', 'Servente', 'Eletricista', 'Encanador']

        menu_itens = []
        position = 0
        for state in states:
            position += 1
            row = {'text': state, 'on_release': lambda x=state: self.replace_function(x)}
            menu_itens.append(row)

        self.menu2 = MDDropdownMenu(
            caller=self.ids.card_function,
            items=menu_itens,
            position='bottom',
            width_mult=5,
            max_height='400dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            # Adicionando personalizações estéticas
            elevation=8,
            radius=[10, 10, 10, 10],
            border_margin=12,
            ver_growth="down",
            hor_growth="right",
        )

        # Estilizando os itens do menu
        for item in menu_itens:
            item["font_style"] = "Subtitle1"
            item["height"] = dp(56)
            # Adicione ícones aos itens
            if "icon" not in item:
                item["icon"] = "checkbox-marked-circle-outline"
            item["divider"] = "Full"

    def replace_function(self, text):
        self.ids.function.text = text
        self.ids.function.text_color = get_color_from_hex('#FFFB46')
        self.menu2.dismiss()

    # form database
    def step_one(self):
        """Validate form fields and submit if valid"""
        # Check for empty fields
        if self.ids.function.text in 'Selecione uma profissão':
            self.menu2.open()
            return

        for field_id, name in [('telefone', 'telefone'), ('email', 'e-mail'), ('name_user', 'Nome')]:
            if not self.ids[field_id].text:
                self.ids[field_id].focus = True
                self.show_error(f"Por favor, preencha o campo {name}")
                return

        # Validate email
        if not self.is_email_valid(self.ids.email.text):
            self.ids.email.focus = True
            self.show_error("Por favor, insira um e-mail válido")
            return

        # Check for changes in any field
        if (self.ids.email.text != self.employee_mail or
                self.ids.telefone.text != self.employee_telephone or
                self.ids.name_user.text != self.employee_name or
                self.ids.function.text != self.employee_function or
                self.avatar != self.ids.perfil.source):
            self.update_database()
        else:
            self.show_message("Apresente novos dados para atualização", color='#00b894')

    def update_database(self):
        """Update the user data in Firebase"""
        url = f'{self.FIREBASE_URL}/Funcionarios/{self.key}'
        data = {
            'Name': str(self.ids.name_user.text).replace(' ', ''),
            'email': self.ids.email.text,
            'avatar': self.ids.perfil.source,
            'telefone': self.ids.telefone.text,
            'function': self.ids.function.text
        }

        UrlRequest(
            f'{url}/.json',
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.database_success,
            timeout=10
        )

    def database_success(self, req, result):
        """ Agora que está salvo no banco de dados vou chamar a proxima tela"""
        app = MDApp.get_running_app()
        screenmanager = app.root
        perfil = screenmanager.get_screen('PrincipalScreenEmployee')
        perfil.employee_name = self.ids.name_user.text
        perfil.employee_function = self.ids.function.text
        perfil.employee_mail = self.ids.email.text
        perfil.avatar = self.ids.perfil.source
        perfil.employee_telephone = self.ids.telefone.text
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'

    def is_email_valid(self, text):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, text) is not None

    # Image handling
    def recortar_imagem_circular(self, imagem_path):
        """Upload and crop image to circular shape using Cloudinary"""
        try:
            response = cloudinary.uploader.upload(
                imagem_path,
                public_id=self.employee_name,
                overwrite=True,
                transformation=[
                    {'width': 1000, 'height': 1000, 'crop': 'thumb', 'gravity': 'face', 'radius': 'max'}
                ]
            )
            self.ids.perfil.source = response['secure_url']
            self.step_one()
            return response['secure_url']
        except Exception as e:
            self.show_error(f"Erro ao cortar a imagem: {e}")
            return None

    def open_gallery(self):
        """Open gallery to select an image"""
        if self.dont == 'Não':
            self.show_message('Galeria não disponível')
            return

        try:
            filechooser.open_file(
                filters=["*.jpg", "*.png", "*.jpeg"],
                on_selection=self.select_path
            )
        except Exception as e:
            self.show_error(f"Erro ao abrir a galeria: {e}")

    def show_message(self, message, color='#2196F3'):
        """Display a snackbar message"""
        MDSnackbar(
            MDSnackbarText(
                text=message,
                theme_text_color='Custom',
                text_color='white',
                bold=True
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            halign='center',
            size_hint_x=0.8,
            theme_bg_color='Custom',
            background_color=get_color_from_hex(color)
        ).open()

    def show_error(self, error_message):
        """Display an error message"""
        self.show_message(error_message, color='#FF0000')
        print(f"Error: {error_message}")

    def select_path(self, selection):
        """Handle selected image file"""
        if selection:
            path = selection[0]
            self.recortar_imagem_circular(path)
            self.show_message(f"Arquivo selecionado: {path}")

    def on_text_two(self, instance, numero):
        """Format phone number"""
        numero = re.sub(r'\D', '', numero)
        if len(numero) == 11:
            self.ids.telefone.text = f"({numero[0:2]}) {numero[2:7]}-{numero[7:]}"
            self.ids.telefone.focus = False
        else:
            self.ids.telefone.error = True

    def next_page(self):
        """ Passa os dados e chama a tela de editar perfil"""
        self.on_pre_leave()
        app = MDApp.get_running_app()
        screenmanager = app.root
        perfil = screenmanager.get_screen('EditEmployeeTwo')
        perfil.employee_name = self.employee_name
        perfil.employee_function = self.employee_function
        perfil.employee_mail = self.employee_mail
        perfil.employee_telephone = self.employee_telephone
        perfil.key = self.key
        perfil.avatar = self.avatar
        perfil.employee_summary = self.employee_summary
        perfil.skills = self.skills
        screenmanager.transition = SlideTransition(direction='left')
        screenmanager.current = 'EditEmployeeTwo'

    def login(self):
        self.on_pre_leave()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'PrincipalScreenEmployee'

    def on_pre_leave(self, *args):
        self.ids.scroll_view.scroll_y = 1