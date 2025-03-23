from kivy.properties import StringProperty, get_color_from_hex
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class PrincipalScreenEmployee(MDScreen):
    avatar = StringProperty('https://res.cloudinary.com/dsmgwupky/image/upload/v1742650534/Felca.jpg')
    employee_name = StringProperty('Agatha')
    employee_function = StringProperty('Não definido')
    employee_mail = StringProperty('Não definido')
    employee_telephone = StringProperty('Não definido')
    key = StringProperty('-OLzGfiKYkK7FX_X2P4g')
    employee_summary = StringProperty('Desenvolvedor com 5 anos de experiência em projetos webs e móveis')
    skills = StringProperty("['Python', 'PhP']")

    def on_enter(self):
        skills = eval(self.skills)
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