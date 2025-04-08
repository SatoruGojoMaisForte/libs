import json

from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar


class WithoutContractor(MDScreen):
    current_nav_state = StringProperty()
    request = BooleanProperty()
    avatar = StringProperty()
    contractor = StringProperty()
    employee_name = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    key = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()

    def on_enter(self):
        self.request = False

    def add_request(self):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/requets/.json'
        data = {'avatar': f'{self.avatar}',
                'employee_name': f'{self.employee_name}',
                'employee_function': f'{self.employee_function}',
                'email': f'{self.employee_mail}',
                'telephone': f'{self.employee_telephone}',
                'key': f'{self.key}',
                'receiveds': "[]",
                'employee_summary': f'{self.employee_summary}',
                'skills': f'{self.skills}',
                'requests': f"[]"
                }
        print(f'Resumo profissional {self.employee_summary} \n Telefone {self.employee_telephone} \n Email {self.employee_mail} \n Habilidades {self.skills}')
        if 'Não definido' in self.employee_mail or 'Não definido' in self.employee_telephone or 'Não definido' in self.employee_mail or 'Não definido' in self.employee_summary or not self.skills:
            MDSnackbar(
                MDSnackbarText(
                    text='Por favor, preencha todo o perfil profissional antes',
                    theme_text_color='Custom',
                    text_color='white',
                    bold=True
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                halign='center',
                size_hint_x=0.9,
                theme_bg_color='Custom',
                background_color='red'
            ).open()
        else:
            UrlRequest(
                url,
                method='POST',
                req_body=json.dumps(data),
                on_success=self.save,
                on_error=self.error
            )

    def error(self, instance, error):
        print(error)

    def save(self, req, result):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{self.key}/.json'
        data = {'request': 'True'}
        self.request = True
        UrlRequest(
            url,
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.finally_screen
        )

    def finally_screen(self, instance, result):
        """
        Navega para a tela de solicitações de contratante
        """
        print(result)
        app = MDApp.get_running_app()
        screenmanager = app.root

        # Obtém a tela de perfil
        perfil = screenmanager.get_screen('RequestSent')

        # Transfere os dados do usuário
        perfil.key = '-OM3T1g_ejEMjv_LKlNQ'
        perfil.employee_name = self.employee_name
        perfil.employee_function = self.employee_function
        perfil.employee_mail = self.employee_mail
        perfil.employee_telephone = self.employee_telephone
        perfil.avatar = self.avatar
        perfil.employee_summary = self.employee_summary
        perfil.skills = self.skills
        perfil.request = self.request
        perfil.tab_nav_state = 'received'

        # Define o estado de navegação global
        perfil.current_nav_state = 'perfil'
        perfil.ids.vacancy.active = False
        perfil.ids.perfil.active = False
        perfil.ids.payment.active = True
        perfil.ids.notification.active = False

        # Navega para a tela de perfil
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'RequestSent'

    def _next_screen(self):
        """
        Navega para a tela de solicitações de contratante
        """
        app = MDApp.get_running_app()
        screenmanager = app.root

        # Obtém a tela de perfil
        perfil = screenmanager.get_screen('RequestsVacancy')

        # Transfere os dados do usuário
        perfil.key = '-OM3T1g_ejEMjv_LKlNQ'
        perfil.employee_name = self.employee_name
        perfil.employee_function = self.employee_function
        perfil.employee_mail = self.employee_mail
        perfil.employee_telephone = self.employee_telephone
        perfil.avatar = self.avatar
        perfil.employee_summary = self.employee_summary
        perfil.skills = self.skills
        perfil.tab_nav_state = 'received'
        perfil.request = self.request

        # Define o estado de navegação global
        perfil.current_nav_state = 'perfil'
        perfil.ids.vacancy.active = False
        perfil.ids.perfil.active = False
        perfil.ids.payment.active = False
        perfil.ids.notification.active = True

        # Navega para a tela de perfil
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'RequestsVacancy'

    def perfil(self):
        """
        Navega para a tela de perfil e ajusta o estado global de navegação
        """
        app = MDApp.get_running_app()
        screenmanager = app.root

        # Obtém a tela de perfil
        perfil = screenmanager.get_screen('PrincipalScreenEmployee')

        # Transfere os dados do usuário
        perfil.key = self.key
        perfil.employee_name = self.employee_name
        perfil.employee_function = self.employee_function
        perfil.employee_mail = self.employee_mail
        perfil.employee_telephone = self.employee_telephone
        perfil.avatar = self.avatar
        perfil.employee_summary = self.employee_summary
        perfil.skills = self.skills

        # Define o estado de navegação global
        perfil.ids.payment.active = False
        perfil.ids.vacancy.active = False
        perfil.ids.notification.active = False
        perfil.ids.perfil.active = True
        perfil.current_nav_state = 'perfil'

        self.tot_salary = 0
        # Navega para a tela de perfil
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'

    def vacancy(self):
        """
        Navega para a tela de vagas e ajusta o estado global de navegação
        """
        app = MDApp.get_running_app()
        screenmanager = app.root

        # Obtém a tela de vagas
        vac = screenmanager.get_screen('VacancyBank')

        # Transfere os dados do usuário
        vac.key = self.key
        print(self.key)
        vac.employee_name = self.employee_name
        vac.employee_function = self.employee_function
        vac.employee_mail = self.employee_mail
        vac.employee_telephone = self.employee_telephone
        vac.avatar = self.avatar
        vac.employee_summary = self.employee_summary
        vac.skills = self.skills
        vac.contractor = self.contractor
        vac.request = self.request
        # Define o estado de navegação global
        self.current_nav_state = 'vacancy'

        # Garante que apenas o ícone de vagas esteja ativo
        vac.ids.vacancy.active = True
        vac.ids.perfil.active = False
        vac.ids.notification.active = False
        vac.ids.payment.active = False

        # Navega para a tela de vagas
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'VacancyBank'

    def request(self):
        """
        Navega para a tela de vagas e ajusta o estado global de navegação
        """
        app = MDApp.get_running_app()
        screenmanager = app.root

        # Obtém a tela de vagas
        vac = screenmanager.get_screen('RequestsVacancy')

        # Transfere os dados do usuário
        vac.key = self.key
        vac.tab_nav_state = 'request'
        vac.employee_name = self.employee_name
        vac.employee_function = self.employee_function
        vac.employee_mail = self.employee_mail
        vac.employee_telephone = self.employee_telephone
        vac.avatar = self.avatar
        vac.employee_summary = self.employee_summary
        vac.skills = self.skills
        vac.request = self.request
        vac.contractor = self.contractor

        # Garante que apenas o ícone de vagas esteja ativo
        vac.ids.vacancy.active = False
        vac.ids.perfil.active = False
        vac.ids.request.active = True
        vac.ids.notification.active = True

        # Navega para a tela de vagas
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'RequestsVacancy'