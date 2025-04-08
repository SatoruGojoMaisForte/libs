from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class RequestSent(MDScreen):
    current_nav_state = StringProperty('payment')
    request = BooleanProperty()
    avatar = StringProperty()
    employee_name = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    key = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()
    contractor = StringProperty()

    def on_enter(self, *args):
        self.request = bool(self.request)
        print(self.request)

    def _next_screen(self):
        """
        Navega para a tela de solicitações de contratante
        """
        app = MDApp.get_running_app()
        screenmanager = app.root

        # Obtém a tela de perfil
        perfil = screenmanager.get_screen('RequestsVacancy')

        # Transfere os dados do usuário
        perfil.key = self.key
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
        perfil.request = self.request

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
        vac.request = True
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

    def req(self):
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
        vac.current_nav_state = 'notification'
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
        vac.ids.payment.active = False
        vac.ids.notification.active = True

        # Navega para a tela de vagas
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'RequestsVacancy'