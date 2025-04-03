from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, get_color_from_hex
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButtonText, MDButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.screen import MDScreen


class RequestsVacancy(MDScreen):
    current_nav_state = StringProperty('notification')
    avatar = StringProperty()
    employee_name = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    key = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()
    tab_nav_state = StringProperty()

    def on_enter(self, *args):
        self.ids.main_scroll.clear_widgets()
        self.upload_requests()

    def workflow(self, screen):
        self.ids.main_scroll.clear_widgets()
        if screen in 'decline':
            self.tab_nav_state = 'decline'
            self.ids.main_scroll.clear_widgets()
            if not self.ids.main_scroll.children:
                self.ids.main_scroll.clear_widgets()
            self.upload_requests()
        else:
            if not self.ids.main_scroll.children:
                self.ids.main_scroll.clear_widgets()

            self.tab_nav_state = 'request'
            self.ids.main_scroll.clear_widgets()
            self.upload_requests()

    def upload_requests(self):
        self.ids.main_scroll.clear_widgets()
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions/.json'
        UrlRequest(
            url,
            method='GET',
            on_success=self.add_requests
        )

    def add_requests(self, req, requests):
        for key, request in requests.items():
            reqs = eval(request['requests'])
            decline = eval(request['decline'])
            if self.key in reqs and self.tab_nav_state == 'request':
                self.requests(
                    request['occupation'], 'yellow', 'clock-outline',
                    request['company'], request['Option Payment'], request['Salary'],
                    request['email'], request['telephone']
                )
            elif self.tab_nav_state == 'decline':
                if self.key in decline:
                    self.requests(
                        request['occupation'], 'red', 'cancel',
                        request['company'], request['Option Payment'], request['Salary'],
                        request['email'], request['telephone']
                    )
        if not self.ids.main_scroll.children:
            self.ids.main_scroll.clear_widgets()
            label = MDLabel(
                text='\nNenhuma solicitação',
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint_x=0.8,
                halign='center',
                theme_text_color='Custom',
                text_color='grey'
            )
            self.ids.main_scroll.add_widget(label)

    def requests(self, function, color, icon, company, method, salary, email, telephone):

        # Create a card to be added to the scroll view
        card_layout = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            md_bg_color=(1, 1, 1, 1),
            size_hint_y=None,
            size_hint_x=1,
            height='170dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding="5dp",
            spacing="5dp"
        )

        # Barra amarela à esquerda
        yellow_box = MDBoxLayout(
            size_hint_x=0.03,
            theme_bg_color='Custom',
            md_bg_color=f'{color}'
        )
        card_layout.add_widget(yellow_box)

        # Layout de conteúdo
        content_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.95,
            theme_bg_color='Custom',
            md_bg_color=(1, 1, 1, 1)
        )
        card_layout.add_widget(content_layout)

        # Seção do título
        title_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='30dp',
            theme_bg_color='Custom',
            md_bg_color=(1, 1, 1, 1)
        )
        content_layout.add_widget(title_layout)

        # Box para o título
        title_box = MDBoxLayout(
            size_hint_x=0.8,
            padding=[10, 0]
        )
        title_layout.add_widget(title_box)

        # Label do título
        title_label = MDLabel(
            text=f'{function}',
            font_style='Title',
            role='medium',
            bold=True,
            pos_hint={'center_y': 0.5}
        )
        title_box.add_widget(title_label)

        # Box para o ícone de relógio
        clock_box = MDBoxLayout(
            size_hint_x=0.2,
            padding=[10, 0]
        )
        title_layout.add_widget(clock_box)

        # Ícone de relógio
        clock_icon = MDIcon(
            icon=f'{icon}',
            theme_icon_color='Custom',
            icon_color=color,
            pos_hint={'center_y': 0.5}
        )
        clock_box.add_widget(clock_icon)

        # Box para empresa
        company_box = MDBoxLayout(
            size_hint_y=None,
            height='20dp',
            theme_bg_color='Custom',
            md_bg_color=(1, 1, 1, 1),
            padding=[10, 0]
        )
        content_layout.add_widget(company_box)

        # Label da empresa
        company_label = MDLabel(
            text=f'{company}',
            theme_text_color='Custom',
            text_color='grey',
            font_style='Title',
            role='small',
            pos_hint={'center_y': 0.5}
        )
        company_box.add_widget(company_label)

        # Box para informações
        info_box = MDBoxLayout(
            orientation='vertical',
            padding=[10, 0],
            theme_bg_color='Custom',
            md_bg_color=(1, 1, 1, 1)
        )
        content_layout.add_widget(info_box)

        # Box para método de pagamento
        payment_box = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            spacing=5,
            md_bg_color=(1, 1, 1, 1)
        )
        info_box.add_widget(payment_box)

        # Ícone de pagamento
        payment_icon = MDIcon(
            icon='credit-card-outline',
            theme_icon_color='Custom',
            icon_color=(0.0, 1.0, 0.0, 1.0)
        )
        payment_box.add_widget(payment_icon)

        # Label de pagamento
        payment_label = MDLabel(
            text=f'Método de Pagamento: {method}',
            font_style='Label',
            role='medium'
        )
        payment_box.add_widget(payment_label)

        # Box para salário
        salary_box = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            spacing=5,
            md_bg_color=(1, 1, 1, 1)
        )
        info_box.add_widget(salary_box)

        # Ícone de salário
        salary_icon = MDIcon(
            icon='credit-card-outline',
            theme_icon_color='Custom',
            icon_color='purple',
            pos_hint={'center_y': 0.5}
        )
        salary_box.add_widget(salary_icon)

        # Label de salário
        salary_label = MDLabel(
            text=f'Salário: R${salary}',
            font_style='Label',
            role='medium'
        )
        salary_box.add_widget(salary_label)

        # Box para email
        email_box = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            spacing=5,
            md_bg_color=(1, 1, 1, 1)
        )
        info_box.add_widget(email_box)

        # Ícone de email
        email_icon = MDIcon(
            icon='email',
            theme_icon_color='Custom',
            icon_color=get_color_from_hex('#5BC0EB'),
            pos_hint={'center_y': 0.5}
        )
        email_box.add_widget(email_icon)

        # Label de email
        email_label = MDLabel(
            text=f'Email: {email}',
            font_style='Label',
            role='medium'
        )
        email_box.add_widget(email_label)

        # Box para telefone
        phone_box = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            spacing=5,
            md_bg_color=(1, 1, 1, 1)
        )
        info_box.add_widget(phone_box)

        # Ícone de telefone
        phone_icon = MDIcon(
            icon='phone',
            theme_icon_color='Custom',
            icon_color=get_color_from_hex('#FF01FB'),
            pos_hint={'center_y': 0.5}
        )
        phone_box.add_widget(phone_icon)

        # Label de telefone
        phone_label = MDLabel(
            text=f'Telefone: {telephone}',
            font_style='Label',
            role='medium'
        )
        phone_box.add_widget(phone_label)

        # Add the complete card to the scroll view
        self.ids.main_scroll.add_widget(card_layout)

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

        # Define o estado de navegação global
        self.current_nav_state = 'vacancy'

        # Garante que apenas o ícone de vagas esteja ativo
        vac.ids.vacancy.active = True
        vac.ids.perfil.active = False
        vac.ids.notification.active = False

        # Navega para a tela de vagas
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'VacancyBank'

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
        perfil.current_nav_state = 'perfil'
        perfil.ids.notification.active = False

        # Navega para a tela de perfil
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'
