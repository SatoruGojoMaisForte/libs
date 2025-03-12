import ast
import json
from datetime import datetime, timedelta
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import MDListItemHeadlineText, MDListItem, MDListItemTrailingCheckbox, \
    MDListItemTrailingSupportingText, MDListItemTertiaryText
from kivymd.uix.screen import MDScreen


class ThirdWeek(MDScreen):
    work_days_week3 = StringProperty()

    employee_name = StringProperty('Ayanokoji')
    contractor = StringProperty('Solitude')
    scale = '5x2'
    # Variáveis de controle dos dias
    seg = 0
    terc = 0
    quart = 0
    quint = 0
    sex = 0
    sab = 0
    faults = 5
    days_work = 0
    days = 0
    s = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.week = None

    def on_enter(self):
        self.s += 1
        self.ids.main_scroll.clear_widgets()

        # Resetar contadores
        self.days = 0
        self.days_work = 0
        self.seg = 0
        self.terc = 0
        self.quart = 0
        self.quint = 0
        self.sex = 0
        self.sab = 0

        if self.scale in '6x1':
            self.faults = 6
        elif self.scale in '5x2':
            self.faults = 5
        else:
            self.faults = 4

        self.upload_days()
        self.upload_days_work_week()
        current_week = self.get_week_dates()
        self.ids.week.text = f"{current_week['next_week_start_date']} a {current_week['next_week_end_date']}"

        # Atualizar label inicial
        self.ids.label.text = f'Total de {self.days_work} dias presentes, {self.faults} dias ausentes'

    def upload_days_work_week(self):
        dataframe = ast.literal_eval(self.work_days_week3)
        # Dictionary mapping day names to their variables
        day_mapping = {
            'Segunda-feira': 'seg',
            'Terça-feira': 'terc',
            'Quarta-feira': 'quart',
            'Quinta-feira': 'quint',
            'Sexta-feira': 'sex',
            'Sabado': 'sab'
        }

        if not dataframe:
            print('Semana vazia')
        else:
            for dia in dataframe:
                if dia in day_mapping:
                    # Get the variable name for this day
                    var_name = day_mapping[dia]
                    # Set the variable to 1 to mark it as active
                    setattr(self, var_name, 1)
                    # Increment days_work counter
                    self.days_work += 1
                    self.faults -= 1
                    # Mark the checkbox as active
                    dia_seguro = dia.replace('-', '_')
                    if f"icon_{dia_seguro}" in self.ids:
                        self.ids[f"icon_{dia_seguro}"].active = True
                        self.ids[f"icon_{dia_seguro}"].icon = 'checkbox-blank-circle'

    def upload_week(self, start_date=None):
        """
        Retorna todas as datas de uma semana específica (segunda-feira a domingo)
        no formato brasileiro (dd/mm/aaaa).
        """
        if start_date is None:
            start_date = datetime.now()

        # Encontra a segunda-feira da semana
        week_start = start_date - timedelta(days=start_date.weekday())

        # Lista para armazenar os dias da semana formatados
        week_days = [(week_start + timedelta(days=i, weeks=1)).strftime("%d/%m/%Y") for i in range(7)]

        return week_days

    def get_week_dates(self, start_date=None):
        """Calcula as datas de início e término da semana seguinte e retorna no formato brasileiro (dd/mm/yyyy)."""

        if start_date is None:
            start_date = datetime.now()

        # Encontra o primeiro dia da semana (segunda-feira) para o start_date
        week_start = start_date - timedelta(days=start_date.weekday())

        # Calcula o último dia da semana (domingo) para o start_date
        week_end = week_start + timedelta(days=6)

        # Semana seguinte
        next_week_start = week_start + timedelta(weeks=1)
        next_week_end = week_end + timedelta(weeks=1)

        # Formatar as datas da semana seguinte no formato brasileiro (dd/mm/yyyy)
        formatted_next_week_start = next_week_start.strftime('%d/%m/%Y')
        formatted_next_week_end = next_week_end.strftime('%d/%m/%Y')

        return {
            'next_week_start_date': formatted_next_week_start,  # Data formatada (próxima semana)
            'next_week_end_date': formatted_next_week_end,  # Data formatada (próxima semana)
            'next_week_start_datetime': next_week_start,  # Objeto datetime (próxima semana)
            'next_week_end_datetime': next_week_end  # Objeto datetime (próxima semana)
        }

    def upload_days(self):
        # Lista de dias da semana com seus respectivos índices
        dias_semana = [
            ('Segunda-feira', 0),
            ('Terça-feira', 1),
            ('Quarta-feira', 2),
            ('Quinta-feira', 3),
            ('Sexta-feira', 4),
            ('Sabado', 5),
            ('Domingo', 6)
        ]

        # Obtém os dias da semana
        week = self.upload_week()

        for dia, indice in dias_semana:
            # Verifica se é um dia de folga com base na escala
            is_folga = (self.scale == '6x1' and dia in ('Domingo') or
                        (self.scale == '5x2' and dia in ('Sabado', 'Domingo')) or
                        (self.scale == '4x3' and (dia in ('Sexta-feira', 'Sabado', 'Domingo'))))

            # Obtém a data correspondente
            day_week = str(week[indice]) if indice < len(week) else 'Data não disponível'

            # Cria o item da lista
            list_item = MDListItem(
                MDListItemHeadlineText(
                    text=dia
                ),
                MDListItemTertiaryText(
                    text=day_week
                ),
                pos_hint={'center_x': 0.5},
                size_hint=(1, None),
                theme_bg_color='Custom',
                theme_focus_color='Custom',
                md_bg_color=[1, 1, 1, 1],
                md_bg_color_disabled=[1, 1, 1, 1],
                ripple_color=(1, 1, 1, 1),
                focus_behavior=False,
            )

            safe_dia = dia.replace('-', '_')

            if not is_folga:
                # Cria botão de checkbox
                icon_button = MDListItemTrailingCheckbox(
                    padding=[0, 0, 0, 0],
                    theme_focus_color='Custom',
                    color_active='blue',
                    color_disabled='black',
                    _current_color='purple',
                    focus_behavior=False
                )
                icon_button.icon = 'checkbox-blank-circle-outline'

                # Armazena referência e vincula evento
                self.ids[f"icon_{safe_dia}"] = icon_button
                icon_button.bind(on_release=lambda instance, d=dia: self.on_checkbox_press(d))
                list_item.add_widget(icon_button)
                self.ids.main_scroll.add_widget(list_item)
            else:
                # Cria rótulo "Folga" para dias de folga
                folga_label = MDListItemTrailingSupportingText(
                    text='Folga',
                    theme_text_color='Custom',
                    text_color=[0.0, 1.0, 0.0, 1.0],  # Verde
                    halign='right',
                    padding=[0, 0, 15, 0],
                    valign='center'
                )

                # Armazena referência
                self.ids[f"icon_{safe_dia}"] = folga_label
                list_item.add_widget(folga_label)
                self.ids.main_scroll.add_widget(list_item)

    def on_checkbox_press(self, dia):
        # Mapeamento dos nomes dos dias para suas variáveis de controle
        mapa_dias = {
            'Segunda-feira': 'seg',
            'Terça-feira': 'terc',
            'Quarta-feira': 'quart',
            'Quinta-feira': 'quint',
            'Sexta-feira': 'sex',
            'Sabado': 'sab'
        }

        # Obtém o valor atual para este dia
        var_dia = mapa_dias.get(dia)
        if var_dia:
            valor_atual = getattr(self, var_dia)
            dia_seguro = dia.replace('-', '_')

            if valor_atual == 0:
                # Marca como trabalhado
                setattr(self, var_dia, 1)
                self.days_work += 1
                self.faults -= 1
                self.ids[f"icon_{dia_seguro}"].icon = 'checkbox-blank-circle'
            else:
                # Marca como não trabalhado
                setattr(self, var_dia, 0)
                self.days_work -= 1
                self.faults += 1
                self.ids[f"icon_{dia_seguro}"].icon = 'checkbox-blank-circle-outline'

        self.ids.label.text = f'Total de {self.days_work} dias presentes, {self.faults} dias ausentes'

    def database_step_one(self):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{self.key}/.json'

        # Create a list of tuples with day names and their values
        days_info = [
            ('seg', self.seg),
            ('terc', self.terc),
            ('quart', self.quart),
            ('quint', self.quint),
            ('sex', self.sex),
            ('sab', self.sab)
        ]

        week = []
        mapa_dias = {
            'seg': 'Segunda-feira',
            'terc': 'Terça-feira',
            'quart': 'Quarta-feira',
            'quint': 'Quinta-feira',
            'sex': 'Sexta-feira',
            'sab': 'Sabado'
        }

        # Check each day's value and append the day name to week if the value is >= 1
        for day_key, day_value in days_info:
            if day_value >= 1:
                # Get the full day name from mapa_dias
                var_dia = mapa_dias.get(day_key)
                print(var_dia)
                # Append the day name to the week list
                week.append(var_dia)

        data = {
            'week_3': self.days_work,
            'work_days_week3': f'{week}'
        }

        UrlRequest(
            url,
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.database_step_two
        )

    def database_step_two(self, req, result):
        '''Voltar para a tela de mes e passar os dias trabalhados dessa semana para ela'''
        app = MDApp.get_running_app()
        screen_manager = app.root
        working = screen_manager.get_screen('WorkingMonth')
        working.week_3 = self.days_work
        working.work_days_week3 = result['work_days_week3']
        # Reset day counters
        self.seg = 0
        self.terc = 0
        self.quart = 0
        self.quint = 0
        self.sex = 0
        self.sab = 0
        # Reset work counters
        self.days_work = 0
        self.days = 0
        # Use SlideTransition for consistency
        screen_manager.transition = SlideTransition(direction='right')
        screen_manager.current = 'WorkingMonth'

    def back_working_month(self):
        app = MDApp.get_running_app()
        screen_manager = app.root
        working = screen_manager.get_screen('WorkingMonth')
        working.week_3 = self.days_work
        # Reset counters
        self.seg = 0
        self.terc = 0
        self.quart = 0
        self.quint = 0
        self.sex = 0
        self.sab = 0
        self.days_work = 0
        self.days = 0
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'WorkingMonth'

    def cancel(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.5)
        self.manager.current = 'WorkingMonth'