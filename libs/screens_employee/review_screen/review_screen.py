import ast
import json

from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import SlideTransition
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.chip import MDChipText, MDChip
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from babel.numbers import format_currency


class PaymentCard(MDBoxLayout):
    """
    A card widget that displays payment information with a green indicator,
    payment details, and a "Details" button.
    """
    current_data = StringProperty()
    month = StringProperty()
    payment_status = StringProperty()
    payment_type = StringProperty()
    payment_date = StringProperty()
    payment_amount = StringProperty()
    unpaid_payment_amount = StringProperty()
    color = StringProperty()
    text_color = StringProperty()
    color_line = StringProperty()

    def __init__(self, **kwargs):
        # Extract custom properties
        self.week = kwargs.pop('current_data', 'Semana 1')
        self.month = kwargs.pop('month', 'Janeiro')
        self.payment_status = kwargs.pop('payment_status', 'Pago')
        self.payment_type = kwargs.pop('payment_type', 'semanal')
        self.payment_date = kwargs.pop('payment_date', '13/05/2009')
        self.payment_amount = kwargs.pop('payment_amount', 'R$13.400')


        # Set default card settings
        kwargs.update({
            'orientation': 'horizontal',
            'size_hint_y': None,
            'height': dp(150),
            'theme_bg_color': 'Custom',
        })

        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.clear_widgets()

        # Green indicator box on left
        green_box = MDBoxLayout(
            theme_bg_color='Custom',
            radius=[15, 0, 0, 15],
            md_bg_color=self.color_line
        )
        self.add_widget(green_box)

        # Content area on right
        content_layout = MDBoxLayout(
            orientation='vertical',
            theme_bg_color='Custom',
            radius=[0, 15, 15, 0],
            size_hint_x=None,
            width=dp(290)
        )
        self.add_widget(content_layout)

        # Header area with title and status chip
        header_layout = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            md_bg_color='white',
            spacing=10,
            padding=[2, ]
        )
        content_layout.add_widget(header_layout)

        # Title box
        title_box = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            padding=[5]
        )
        header_layout.add_widget(title_box)

        # Title label
        title_label = MDLabel(
            text=f'{self.week}',
            font_style='Label',
            role='large',
            theme_text_color='Custom',
            text_color='black',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='left'
        )
        title_box.add_widget(title_label)

        # Status chip container
        status_box = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom'
        )
        header_layout.add_widget(status_box)

        # Status chip
        status_layout = MDRelativeLayout()
        status_box.add_widget(status_layout)

        chip_text = MDChipText(
            text=self.payment_status,
            theme_text_color='Custom',
            text_color=get_color_from_hex(self.text_color),
            pos_hint={'center_x': 0.45, 'center_y': 0.5},
            halign='center',
            bold=True
        )

        status_chip = MDChip(
            chip_text,
            size_hint=(0.4, 0.75),
            theme_bg_color='Custom',
            md_bg_color=get_color_from_hex(self.color),
            pos_hint={"right": .9, "center_y": .5}
        )
        status_layout.add_widget(status_chip)

        # Middle info section
        info_layout = MDBoxLayout(
            orientation='horizontal',
            theme_bg_color='Custom',
            padding=[5, 0, 0, 0]
        )
        content_layout.add_widget(info_layout)

        # Type info
        type_box = MDBoxLayout(
            orientation='vertical',
            theme_bg_color='Custom',
            padding=[5]
        )
        info_layout.add_widget(type_box)

        type_label = MDLabel(
            text='Tipo',
            font_style='Body',
            role='small',
            theme_text_color='Custom',
            text_color='grey',
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            halign='left'
        )
        type_box.add_widget(type_label)

        type_value = MDLabel(
            text=self.payment_type,
            font_style='Body',
            role='medium',
            theme_text_color='Custom',
            text_color=get_color_from_hex('#41463D'),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            halign='left'
        )
        type_box.add_widget(type_value)

        # Date info
        date_box = MDBoxLayout(
            orientation='vertical',
            theme_bg_color='Custom',
            padding=[5]
        )
        info_layout.add_widget(date_box)

        date_label = MDLabel(
            text='data',
            font_style='Body',
            role='small',
            theme_text_color='Custom',
            text_color='grey',
            pos_hint={'center_x': 0.4, 'center_y': 0.8},
            halign='right'
        )
        date_box.add_widget(date_label)

        date_value = MDLabel(
            text=self.payment_date,
            font_style='Body',
            role='medium',
            theme_text_color='Custom',
            text_color=get_color_from_hex('#41463D'),
            pos_hint={'center_x': 0.4, 'center_y': 0.4},
            halign='right'
        )
        date_box.add_widget(date_value)

        # Amount section
        amount_box = MDBoxLayout(
            theme_bg_color='Custom',
            padding=[10, 0, 0, 0]
        )
        content_layout.add_widget(amount_box)

        amount_label = MDLabel(
            text=self.payment_amount,
            font_style='Title',
            role='medium',
            theme_text_color='Custom',
            text_color='black',
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            halign='left'
        )
        amount_box.add_widget(amount_label)

        # Details button section
        details_box = MDBoxLayout(
            theme_bg_color='Custom'
        )
        content_layout.add_widget(details_box)

        details_layout = MDRelativeLayout()
        details_box.add_widget(details_layout)

        details_text = MDChipText(
            text="Detalhes",
            theme_text_color='Custom',
            text_color='black',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            bold=True
        )

        details_chip = MDChip(
            details_text,
            theme_bg_color='Custom',
            md_bg_color=[1, 1, 1, 1],
            pos_hint={"center_x": .5, "center_y": .5}
        )
        details_layout.add_widget(details_chip)

        # Bind click event for details button
        details_chip.bind(on_release=self.on_details_click)

    def on_details_click(self, instance):
        """Handle click on the Details button"""
        print(f"Details clicked for payment: {self.week} - {self.month}, {self.payment_amount}")
        # Add additional functionality here as needed


class ReviewScreen(MDScreen):
    current_nav_state = StringProperty('revision')
    key = StringProperty()
    avatar = StringProperty()
    employee_name = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()
    tot_salary = NumericProperty()
    contractor_month = NumericProperty()
    contractor = StringProperty()
    request = BooleanProperty()

    def on_enter(self):
        # Lista fixa dos meses do ano
        self.months_year = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        self.dados_teste = [
            {'Payment Type': 'Mensal', 'Paid Salary': '19000', 'Numb Month': '3', 'Month': 'Janeiro',
             'Data': '31/05/2009'},
            {'Payment Type': 'Semanal', 'Paid Salary': '19000', 'Numb Month': '5', 'Month': 'Maio',
             'Data': '31/05/2009'}
        ]

        from datetime import datetime
        self.month = datetime.today().month
        self.ids.main_scroll.clear_widgets()
        self.upload_payments()

    def upload_payments(self):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{self.key}/.json'
        UrlRequest(
            url,
            on_success=self.add_payments,
            on_error=self.usar_dados_teste,
            on_failure=self.usar_dados_teste
        )

    def add_payments(self, instance, response):
        # Verificar se 'payments' existe no response
        self.contractor_month = response['contractor_month']
        if 'payments' not in response:
            print("Chave 'payments' não encontrada na resposta!")
            return self.usar_dados_teste()

        # Mostrar o valor bruto de 'payments'
        print(f"Valor bruto de 'payments': {response['payments']}")
        print(f"Tipo de 'payments': {type(response['payments'])}")

        # Processar com base no tipo
        if isinstance(response['payments'], str):
            try:
                # Usar ast.literal_eval em vez de eval (mais seguro)
                clean_json = response['payments'].strip()
                print(f"Tentando analisar: {clean_json[:100]}...")  # Mostrar início da string
                payments = ast.literal_eval(clean_json)
            except (SyntaxError, ValueError) as e:
                print(f"Erro ao analisar string: {e}")
                # Se falhar com ast.literal_eval, tente json.loads
                try:
                    payments = json.loads(clean_json)
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    # Se falhar, use os dados de teste
                    return self.usar_dados_teste()
        elif isinstance(response['payments'], list):
            payments = response['payments']
        else:
            print(f"Formato inesperado: {type(response['payments'])}")
            return self.usar_dados_teste()

        # Verificar o conteúdo final de payments
        print(f"Pagamentos processados: {payments}")

        # Processar pagamentos
        self.processar_pagamentos(payments)

    def usar_dados_teste(self):
        print("\nUsando dados de teste como fallback:")
        print(self.dados_teste)
        self.processar_pagamentos(self.dados_teste)

    def processar_pagamentos(self, payments):
        numb = 0
        # Verificar se payments não está vazio
        if not payments:
            print("Nenhum pagamento para processar! Usando dados de teste...")
            payments = self.dados_teste

        # Criar dicionário para rastrear status dos meses
        status_meses = {mes: False for mes in self.months_year}
        month_payment = {
            'Janeiro': [],
            'Fevereiro': [],
            'Março': [],
            'Abril': [],
            'Maio': [],
            'Junho': [],
            'Julho': [],
            'Agosto': [],
            'Setembro': [],
            'Outubro': [],
            'Novembro': [],
            'Dezembro': []
        }

        # Processar cada pagamento
        for payment in payments:
            if isinstance(payment, dict) and 'Month' in payment:
                mes = payment['Month']
                if mes in self.months_year:
                    status_meses[mes] = True
                    print(f"Mês marcado como pago: {mes}")
                    month_payment[f'{mes}'] = payment

        print(month_payment)
        typ = ''
        # Mostrar resultado final
        print("\nStatus Final dos Pagamentos:")
        for mes in self.months_year:
            numb += 1
            if numb <= self.month:
                print('my eggs')
                if numb >= int(self.contractor_month):
                    status = "✅ PAGO" if status_meses[mes] else "❌ PENDENTE"
                    if status == '✅ PAGO':
                        text_numb = f''
                        if month_payment[f'{mes}']['Payment Type'] in 'Mensal':
                            text_numb = f'Mês: {month_payment[f'{mes}']['Numb Month']} - {month_payment[f'{mes}']['Month']}'
                        elif month_payment[f'{mes}']['Payment Type'] in 'Semanal':
                            text_numb = f'Semana: {month_payment[f'{mes}']['Numb Month']} - {month_payment[f'{mes}']['Month']}'

                        print(month_payment[f'{mes}'])
                        self.tot_salary += float(month_payment[f'{mes}']['Paid Salary'])
                        card = PaymentCard(
                            payment_date=month_payment[f'{mes}']['Data'],
                            payment_type=month_payment[f'{mes}']['Payment Type'],
                            payment_amount=f'{format_currency(month_payment[f'{mes}']['Paid Salary'], 'BRL', locale='pt_BR')}',
                            payment_status='Pago',
                            month=month_payment[f'{mes}']['Month'],
                            current_data=text_numb,
                            color_line='#68D89B',
                            text_color='#ffffff',
                            color='#68D89B'
                        )
                        typ = f'{month_payment[f'{mes}']['Payment Type']}'
                        self.ids.main_scroll.add_widget(card)
                    else:
                        text_numb = ''
                        if typ in 'Mensal':
                            text_numb = f'Mês: {self.months_year.index(mes) + 1} - {mes}'
                        elif typ in 'Semanal':
                            text_numb = f'Semana: {self.months_year.index(mes) + 1} - {mes}'
                        card = PaymentCard(
                            payment_date='Aguardando',
                            payment_type=typ,
                            payment_amount=f'R$0.0',
                            payment_status='Pendente',
                            month=f'{mes}',
                            current_data=text_numb,
                            color_line='#E3170A',
                            text_color='#ffffff',
                            color='#E3170A'
                        )
                        self.ids.main_scroll.add_widget(card)
            else:
                numb = 0
                break

        self.ids.received.text = f'{format_currency(self.tot_salary, 'BRL', locale='pt_BR')}'

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
        vac.ids.notification.active = False
        vac.ids.payment.active = False

        self.tot_salary = 0

        # Navega para a tela de vagas
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'VacancyBank'

    def req2(self):
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
        vac.ids.request.active = False
        vac.ids.notification.active = True

        # Navega para a tela de vagas
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'RequestsVacancy'

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
        vac.contractor = self.contractor
        vac.request = self.request

        # Garante que apenas o ícone de vagas esteja ativo
        vac.ids.vacancy.active = False
        vac.ids.perfil.active = False
        vac.ids.request.active = True
        vac.ids.notification.active = True

        self.tot_salary = 0

        # Navega para a tela de vagas
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

    def back(self):
        print('back')
