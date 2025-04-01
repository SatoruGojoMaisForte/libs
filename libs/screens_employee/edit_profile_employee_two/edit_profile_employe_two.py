import json

from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import get_color_from_hex, StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDButtonText, MDButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText


class EditEmployeeTwo(MDScreen):
    employee_name = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    avatar = StringProperty()
    key = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty('[]')
    skill_add = 0
    FIREBASE_URL = 'https://obra-7ebd9-default-rtdb.firebaseio.com'
    new_skills = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button = MDButton(
            MDButtonText(
                text=f'Nenhuma habilidade foi adicionada',
                theme_text_color='Custom',
                text_color='white',
                bold=True
            ),
            theme_bg_color='Custom',
            md_bg_color=get_color_from_hex('#0047AB')
        )
        self.ids['not_add'] = self.button

    def on_enter(self):
        self.skill_add += 1

        skills = eval(self.skills)
        if skills:
            for skill in skills:
                self.new_skills.append(f'{skill}')
        if self.employee_summary not in 'Não definido':
            self.ids.sumary.text = self.employee_summary
        if self.skill_add == 1:
            self.add_skills(skills)

        else:
            self.ids.main_scroll.clear_widgets()
            self.skill_add = 0
            self.add_skills(skills)

    def limitate(self, instance, text):
        self.ids.sumary.text = f'{text[:120]}'

    def add_skill(self):
        skill = self.ids.skill.text

        if not skill:
            return
        self.ids.main_scroll.clear_widgets()
        self.new_skills.append(f'{skill}')

        for k in self.new_skills:
            button = MDButton(
                MDButtonText(
                    text=f'{k}',
                    theme_text_color='Custom',
                    text_color='white',
                    bold=True
                ),
                theme_bg_color='Custom',
                md_bg_color=get_color_from_hex('#0047AB')
            )
            self.ids.main_scroll.add_widget(button)
        self.ids.skill.text = ''

    def add_skills(self, skills):
        """ Adicionando as habilidades do funcionario na tela """
        if skills:
            self.ids.main_scroll.clear_widgets()
            for skill in skills:
                button = MDButton(
                    MDButtonText(
                        text=f'{skill}',
                        theme_text_color='Custom',
                        text_color='white',
                        bold=True
                    ),
                    theme_bg_color='Custom',
                    md_bg_color=get_color_from_hex('#0047AB')
                )
                self.ids.main_scroll.add_widget(button)
        else:

            self.ids.main_scroll.add_widget(self.button)

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

    def step_one(self):
        """Validate form fields and submit if valid"""
        skills = eval(self.skills)
        if len(skills) < 3 and len(self.new_skills) < 3:
            self.show_error('Obrigatorio adicionar 3 habilidades')
            return

        if not self.ids.sumary.text:
            self.show_error('Resumo profissional obrigatorio*')
            return

        self.update_database()

    def restart(self):
        """Update the user data in Firebase"""
        url = f'{self.FIREBASE_URL}/Funcionarios/{self.key}'
        data = {
            'skills': f"{self.new_skills}"
        }

        UrlRequest(
            f'{url}/.json',
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.clear_main,
            timeout=10
        )

    def clear_main(self, instance, result):
        self.ids.main_scroll.clear_widgets()
        self.new_skills = []
        self.add_skills([])

    def update_database(self):
        """Update the user data in Firebase"""
        url = f'{self.FIREBASE_URL}/Funcionarios/{self.key}'
        data = {
            'Name': self.employee_name,
            'email': self.employee_mail,
            'avatar': self.avatar,
            'telefone': self.employee_telephone,
            'function': self.employee_function,
            'sumary': self.ids.sumary.text,
            'skills': f"{self.new_skills}"
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
        self.new_skills = []
        screenmanager = app.root
        perfil = screenmanager.get_screen('PrincipalScreenEmployee')
        perfil.employee_name = result['Name']
        perfil.employee_function = result['function']
        perfil.employee_mail = result['email']
        perfil.employee_telephone = result['telefone']
        perfil.employee_summary = result['sumary']
        perfil.skills = result['skills']
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'

    def previous_page(self):
        app = MDApp.get_running_app()
        screenmanager = app.root
        self.new_skills = []
        perfil = screenmanager.get_screen('EditEmployee')
        perfil.employee_name = self.employee_name
        perfil.employee_function = self.employee_function
        perfil.employee_mail = self.employee_mail
        perfil.employee_telephone = self.employee_telephone
        perfil.key = self.key
        perfil.avatar = self.avatar
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'EditEmployee'
