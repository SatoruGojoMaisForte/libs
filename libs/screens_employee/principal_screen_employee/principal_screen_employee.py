from kivy.properties import StringProperty, get_color_from_hex, BooleanProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class PrincipalScreenEmployee(MDScreen):
    current_nav_state = StringProperty('perfil')
    avatar = StringProperty()
    request = BooleanProperty()
    employee_name = StringProperty()
    contractor = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    key = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()

    def on_enter(self):
        # Garantir que apenas o ícone de perfil esteja ativo
        self.current_nav_state = 'perfil'
        self.ids.perfil.active = True
        self.ids.vacancy.active = False

        try:
            skills = eval(self.skills)

        except:
            skills = []

        self.ids.main_scroll.clear_widgets()
        self.skill_add = 0
        self.add_skills(skills)

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
            self.ids.main_scroll.clear_widgets()
            button = MDButton(
                MDButtonText(
                    text=f'Nenhuma habilidade adicionada',
                    theme_text_color='Custom',
                    text_color='white',
                    bold=True
                ),
                theme_bg_color='Custom',
                md_bg_color=get_color_from_hex('#0047AB')
            )
            self.ids.main_scroll.add_widget(button)

    def _next_profile_edit(self):
        """ Passa os dados e chama a tela de editar perfil"""
        app = MDApp.get_running_app()
        screenmanager = app.root
        perfil = screenmanager.get_screen('EditEmployee')
        perfil.employee_name = self.employee_name
        perfil.employee_function = self.employee_function
        perfil.employee_mail = self.employee_mail
        perfil.employee_telephone = self.employee_telephone
        perfil.key = self.key
        perfil.avatar = self.avatar
        perfil.employee_summary = self.employee_summary
        perfil.skills = self.skills
        screenmanager.transition = SlideTransition(direction='left')
        screenmanager.current = 'EditEmployee'

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

    def requests(self):
        print(self.request)
        if not self.contractor:

            if not self.request:
                app = MDApp.get_running_app()
                screen = app.root
                without = screen.get_screen('WithoutContractor')
                # Transfere os dados do usuário
                without.key = self.key
                without.tab_nav_state = 'request'
                without.employee_name = self.employee_name
                without.employee_function = self.employee_function
                without.employee_mail = self.employee_mail
                without.employee_telephone = self.employee_telephone
                without.ids.vacancy.active = False
                without.ids.perfil.active = False
                without.ids.payment.active = True
                without.ids.notification.active = False
                without.avatar = self.avatar
                without.request = self.request
                without.contractor = self.contractor
                without.employee_summary = self.employee_summary
                without.skills = self.skills
                screen.current = 'WithoutContractor'

            else:
                app = MDApp.get_running_app()
                screen = app.root
                without = screen.get_screen('RequestSent')
                # Transfere os dados do usuário
                without.key = self.key
                without.tab_nav_state = 'request'
                without.employee_name = self.employee_name
                without.employee_function = self.employee_function
                without.employee_mail = self.employee_mail
                without.employee_telephone = self.employee_telephone
                without.ids.vacancy.active = False
                without.ids.perfil.active = False
                without.ids.payment.active = True
                without.ids.notification.active = False
                without.avatar = self.avatar
                without.employee_summary = self.employee_summary
                without.skills = self.skills
                without.request = self.request
                without.contractor = self.contractor
                screen.current = 'RequestSent'

        else:
            app = MDApp.get_running_app()
            screen = app.root
            without = screen.get_screen('ReviewScreen')
            # Transfere os dados do usuário
            without.key = self.key
            without.employee_name = self.employee_name
            without.employee_function = self.employee_function
            without.employee_mail = self.employee_mail
            without.employee_telephone = self.employee_telephone
            without.avatar = self.avatar
            without.employee_summary = self.employee_summary
            without.skills = self.skills
            without.ids.vacancy.active = False
            without.ids.perfil.active = False
            without.ids.payment.active = True
            without.ids.notification.active = False
            without.request = self.request
            without.contractor = self.contractor
            without.current_nav_state = 'payment'
            screen.current = 'ReviewScreen'
