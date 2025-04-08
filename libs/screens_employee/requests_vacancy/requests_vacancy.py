import json

from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, get_color_from_hex, BooleanProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButtonText, MDButton
from kivymd.uix.chip import MDChip
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText


class RequestsVacancy(MDScreen):
    current_nav_state = StringProperty('notification')
    avatar = StringProperty()
    employee_name = StringProperty()
    employee_function = StringProperty()
    contractor = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    key = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()
    tab_nav_state = StringProperty()
    request = BooleanProperty()
    click = 0

    def on_enter(self, *args):
        self.ids.main_scroll.clear_widgets()
        if self.tab_nav_state in 'received':
            self.receiveds()
            return

        self.upload_requests()

    def workflow(self, screen):
        self.click += 1

        # Impede recarregar widgets se já estiver na aba certa
        if screen == self.tab_nav_state:
            return

        # Atualiza o estado da aba atual
        self.tab_nav_state = screen
        self.ids.main_scroll.clear_widgets()

        # Chama a função correta conforme a aba
        if screen == 'received':
            self.receiveds()

        elif screen == 'decline':
            self.upload_requests()

        elif screen == 'request':
            self.upload_requests()

        # Reinicia o contador de clique
        self.click = 0

    def receiveds(self):
        self.ids.main_scroll.clear_widgets()
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{self.key}/.json'
        print(self.key)
        UrlRequest(
            url,
            method='GET',
            on_success=self.add_received
        )

    def add_received(self, instance, req):
        added_any = False

        try:
            received = eval(req['receiveds'])

        except:
            received = []

        for contractor in received:
            UrlRequest(
                f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{contractor}/.json',
                on_success=self.cont
            )
            added_any = True

        if not added_any and not self.ids.main_scroll.children:
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

    def cont(self, instance, result):

        card = self.create_profile_card(result['name'], result['function'], 5, result['perfil'])
        self.ids.main_scroll.add_widget(card)

    def upload_requests(self):
        self.ids.main_scroll.clear_widgets()
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions/.json'
        UrlRequest(
            url,
            method='GET',
            on_success=self.add_requests
        )

    import json

    def add_requests(self, req, requests):
        added_any = False

        for key, request in requests.items():
            try:
                reqs = json.loads(request['requests'])  # deve ser uma string JSON, tipo '["key1", "key2"]'
                decline = json.loads(request['decline'])
            except Exception as e:
                print(f"Erro ao carregar requests/decline: {e}")
                continue

            if self.key in reqs and self.tab_nav_state == 'request':
                self.requests(
                    request['occupation'], 'yellow', 'clock-outline',
                    request['company'], request['Option Payment'], request['Salary'],
                    request['email'], request['telephone']
                )
                added_any = True

            elif self.key in decline and self.tab_nav_state == 'decline':
                self.requests(
                    request['occupation'], 'red', 'cancel',
                    request['company'], request['Option Payment'], request['Salary'],
                    request['email'], request['telephone']
                )
                added_any = True

        if not added_any or not self.ids.main_scroll.children:
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

    def create_profile_card(self, name, profession, rating, avatar):
        # Card principal com bordas arredondadas
        card_layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height="180dp",
            padding="15dp",
            radius=20,
            theme_line_color='Custom',
            line_color='grey',
            md_bg_color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5}
        )

        # Layout para informações e foto
        info_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=0.8,
            spacing="5dp",
            pos_hint={'center_y': 0.8}
        )
        card_layout.add_widget(info_layout)

        # Foto de perfil
        profile_box = MDBoxLayout(
            size_hint_x=0.5,
            padding="5dp"
        )
        info_layout.add_widget(profile_box)

        # Imagem circular
        profile_image = MDRelativeLayout(
            size_hint=(1, 1)
        )

        # Avatar - usando FitImage para imagem circular
        avatar = FitImage(
            source=f"{avatar}",  # Substitua pelo caminho da sua imagem
            size_hint=(1, 0.95),
            radius=[100, ]  # Valor para tornar a imagem circular
        )
        profile_image.add_widget(avatar)
        profile_box.add_widget(profile_image)

        # Informações do profissional
        text_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.75,
            spacing="5dp",
            padding=["5dp", 0, 0, 0],
            pos_hint={'center_y': 0.6}
        )
        info_layout.add_widget(text_layout)

        # Nome do profissional
        name_label = MDLabel(
            text=name,
            font_style='Title',
            role='medium',
            bold=True,
            adaptive_height=True
        )
        text_layout.add_widget(name_label)

        # Profissão
        profession_label = MDLabel(
            text=profession,
            font_style='Title',
            role='medium',
            theme_text_color="Secondary",
            adaptive_height=True
        )
        text_layout.add_widget(profession_label)

        # Layout para estrelas
        stars_layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing="2dp"
        )
        text_layout.add_widget(stars_layout)

        # Adicionar estrelas com base na avaliação (de 0 a 5)
        for i in range(5):
            star_icon = MDIcon(
                icon="star",
                theme_icon_color="Custom",
                icon_color=(1, 0.8, 0, 1) if i < rating else (0.7, 0.7, 0.7, 1)
                # Amarelo para estrelas preenchidas, cinza para vazias
            )
            stars_layout.add_widget(star_icon)

        # Layout para o botão
        button_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=0.3,
            padding=[0, "10dp", 0, 0],
            pos_hint={'right': 1}
        )
        card_layout.add_widget(button_layout)

        # Espaço vazio à esquerda para alinhar o botão à direita
        spacer = MDBoxLayout(
            size_hint_x=0.6
        )
        button_layout.add_widget(spacer)

        # Botão "Ver perfil"
        profile_button = MDButton(
            MDButtonText(
                text="Ver perfil",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
            ),
            theme_bg_color='Custom',
            md_bg_color=(0.16, 0.44, 0.95, 1),  # Azul como na imagem
            size_hint_x=0.4,
            pos_hint={'center_y': 0.4}
        )
        button_layout.add_widget(profile_button)

        return card_layout

    # Exemplo de uso:
    # Adicione este código onde você deseja exibir o perfil, por exemplo, no método build() ou em um método específico
    def show_profiles(self):
        # Limpar o contêiner primeiro (se necessário)
        self.ids.profiles_container.clear_widgets()

        # Criar e adicionar o perfil
        profile = self.create_profile_card("Anderson Silva", "Eletricista", 5)
        self.ids.profiles_container.add_widget(profile)

        # Você pode adicionar mais perfis conforme necessário
        # profile2 = self.create_profile_card("Marcos Almeida", "Pedreiro", 4)
        # self.ids.profiles_container.add_widget(profile2)

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
        vac.request = self.request
        vac.contractor = self.contractor

        # Define o estado de navegação global
        self.current_nav_state = 'vacancy'

        # Garante que apenas o ícone de vagas esteja ativo
        vac.ids.vacancy.active = True
        vac.ids.perfil.active = False
        vac.ids.payment.active = False
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
        perfil.request = self.request
        perfil.contractor = self.contractor

        # Define o estado de navegação global
        perfil.current_nav_state = 'vacancy'
        perfil.ids.notification.active = False
        perfil.ids.vacancy.active = False
        perfil.ids.payment.active = False
        perfil.ids.perfil.active = True

        # Navega para a tela de perfil
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'

    def req(self):
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
                without.employee_summary = self.employee_summary
                without.skills = self.skills
                without.request = self.request
                without.contractor = self.contractor
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
                without.request = self.request
                without.avatar = self.avatar
                without.employee_summary = self.employee_summary
                without.contractor = self.contractor
                without.skills = self.skills
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
            without.contractor = self.contractor
            without.request = self.request
            without.avatar = self.avatar
            without.employee_summary = self.employee_summary
            without.skills = self.skills
            without.ids.vacancy.active = False
            without.ids.perfil.active = False
            without.ids.payment.active = True
            without.ids.notification.active = False
            without.request = self.request

            without.current_nav_state = 'payment'
            screen.current = 'ReviewScreen'
