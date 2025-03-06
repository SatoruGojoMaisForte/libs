import datetime
import locale

from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import SlideTransition
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class EvaluationScreen(MDScreen):
    employee_name = StringProperty("")
    employee_function = StringProperty("")
    avatar = StringProperty("")
    contractor = StringProperty("")
    method_salary = StringProperty("")
    salary = NumericProperty()
    assess = StringProperty("8.4")
    coexistence = NumericProperty(0)
    punctuality = NumericProperty(0)
    efficiency = NumericProperty(0)
    scale = StringProperty("")
    days_work = NumericProperty(0)
    week_1 = NumericProperty()
    week_2 = NumericProperty()
    week_3 = NumericProperty()
    week_4 = NumericProperty()
    s = ''

    # Dicionário para mapear escalas a dias úteis no mês
    SCALE_WORKDAYS = {
        "6x1": {"day": 6, "week": 6, "biweekly": 12, "month": 24},
        "5x2": {"day": 5, "week": 5, "biweekly": 10, "month": 20},
        "4x3": {"day": 4, "week": 4, "biweekly": 8, "month": 16}
    }

    # Dicionário para avaliações de funcionários
    ASSESSMENT_LEVELS = {
        "coexistence": {
            1: {"text": "Conflituoso(a)", "color": "#FF0000"},
            2: {"text": "Tolerável(a)", "color": "#E06666"},
            3: {"text": "Neutro(a)", "color": "#808080"},
            4: {"text": "Colaborativa(a)", "color": "#008000"},
            5: {"text": "Excelente(a)", "color": "#0044CC"}
        },
        "efficiency": {
            1: {"text": "Ineficiente(a)", "color": "#FF0000"},
            2: {"text": "Baixa Eficiência(a)", "color": "#E06666"},
            3: {"text": "Razoável(a)", "color": "#808080"},
            4: {"text": "Eficiente(a)", "color": "#008000"},
            5: {"text": "Altamente Eficiente(a)", "color": "#0044CC"}
        },
        "punctuality": {
            1: {"text": "Muito Atrasado(a)", "color": "#FF0000"},
            2: {"text": "Frequentemente Atrasado(a)", "color": "#E06666"},
            3: {"text": "Pontualidade Regular(a)", "color": "#808080"},
            4: {"text": "Pontual(a)", "color": "#008000"},
            5: {"text": "Sempre Pontual/Adiantado(a)", "color": "#0044CC"}
        }
    }

    def on_enter(self, *args):
        """Inicialização da tela quando ela é exibida"""
        self.days_work = self.week_1 + self.week_2 + self.week_3 + self.week_4
        self.ids.value_salary.text = '{:.0f}'.format(self.salary)
        self._update_profile_info()
        self._update_components()
        self._calculate_salary()
        self._finally_work()

    def _finally_work(self):
        """Verificar forma de recebimento e finalizar o pagamento com base nisso"""
        if self.method_salary in ('Diaria', 'Semanal'):

            data_atual = datetime.date.today()
            numero_dia = data_atual.weekday()

            dias_semana = {
                0: "Segunda-feira",
                1: "Terça-feira",
                2: "Quarta-feira",
                3: "Quinta-feira",
                4: "Sexta-feira",
                5: "Sábado",
                6: "Domingo"
            }
            dia_hoje = dias_semana[numero_dia]

            if self.scale in '6x1' and dia_hoje in 'Sábado':
                print('Finalizar semana 6x1')
                return

            if self.scale in '5x2' and dia_hoje in 'Sexta-feira':
                print('Finalizar semana 5x2')
                return

            if self.scale in '4x3' and dia_hoje in 'Quinta-feira':
                print('Finalizar semana 4x3')
                return

        elif self.method_salary in 'Quinzenal':

            # Obter a data atual
            data_atual = datetime.date.today()

            # Obter apenas o dia do mês
            dia_do_mes = data_atual.day

            if dia_do_mes == 15:
                print('Finalizar quinzenal')

        else:
            # Obter a data atual
            data_atual = datetime.date.today()

            # Obter apenas o dia do mês
            dia_do_mes = data_atual.day

            if dia_do_mes == 3:
                print('Finalizar Mensal')

    def _update_profile_info(self):
        """Atualiza informações de perfil na interface"""
        self.ids.perfil.source = self.avatar
        self.ids.name.text = self.employee_name
        self.ids.function.text = self.employee_function

    def _calculate_salary(self):
        """Calcula o salário com base no método de pagamento e escala"""
        salary_calculators = {
            "Diaria": self._calculate_day,
            "Semanal": self._calculate_week,
            "Quinzenal": self._calculate_biweekly,
            "Mensal": self._calculate_month,
            "Empreita": self._calculate_undertakes
        }

        calculator = salary_calculators.get(self.method_salary)
        if calculator:
            calculator()
        else:
            self.ids.text_salary.text = self.method_salary

    def _get_percentage_and_day_value(self, period_type):
        """Retorna a porcentagem de dias trabalhados e o valor diário"""
        if not self.scale in self.SCALE_WORKDAYS:
            return 0, 0

        workdays = self.SCALE_WORKDAYS[self.scale][period_type]
        percentage = (self.days_work / workdays) * 100

        if period_type == "day":
            day_value = int(self.salary)
        else:
            day_value = int(self.salary) / workdays

        return percentage, day_value

    def _calculate_day(self):
        """Calcula o salário diário"""
        percentage, day_value = self._get_percentage_and_day_value("day")
        self.ids.percentage.text = f"{percentage:.2f}%"
        salary = day_value * self.days_work
        self.ids.value_salary.text = f"R${int(salary):,}"

    def _calculate_week(self):
        """Calcula o salário semanal"""
        percentage, day_value = self._get_percentage_and_day_value("week")
        self.ids.percentage.text = f"{percentage:.2f}%"
        salary = day_value * self.days_work
        self.ids.value_salary.text = f"R${int(salary):,}"

    def _calculate_biweekly(self):
        """Calcula o salário quinzenal"""
        percentage, day_value = self._get_percentage_and_day_value("biweekly")
        self.ids.percentage.text = f"{percentage:.2f}%"
        salary = day_value * self.days_work
        self.ids.value_salary.text = f"R${salary:,.2f}"

    def _calculate_month(self):
        """Calcula o salário mensal"""
        percentage, day_value = self._get_percentage_and_day_value("month")
        self.ids.percentage.text = f"{percentage:.2f}%"
        salary = day_value * self.days_work
        self.ids.value_salary.text = f"R${salary:,.2f}"

    def _calculate_undertakes(self):
        """Calcula o salário por empreita"""
        self.ids.frequency.text = "Prazo"
        self.ids.percentage.text = f"{self.days_work}"

    def _update_components(self):
        """Atualiza os componentes de avaliação na interface"""
        self._update_assessment("coexistence")
        self._update_assessment("efficiency")
        self._update_assessment("punctuality")
        self._update_salary_display()

    def _update_assessment(self, assessment_type):
        """Atualiza um componente específico de avaliação"""
        value = getattr(self, assessment_type)

        if not value:
            self.ids[assessment_type].text_color = "red"
            self.ids[f"text_{assessment_type}"].text = "Não definido"
            return
        else:
            self.ids[assessment_type].text_color = 'green'

        level = int(value)
        assessment_info = self.ASSESSMENT_LEVELS[assessment_type].get(level, {})

        if assessment_info:
            self.ids[f"text_{assessment_type}"].text_color = get_color_from_hex(assessment_info["color"])
            self.ids[f"text_{assessment_type}"].text = assessment_info["text"]

    def _update_salary_display(self):
        """Atualiza a exibição do salário na interface"""
        if not self.salary:
            self.ids.salary.text_color = "red"
            self.ids.text_salary.text = "Não definido"
        else:
            self.ids.text_salary.text = f"{self.method_salary}: R$ {int(self.salary):,}"

    def _navigate_to_screen(self, screen_name):
        """Navega para uma tela específica, transferindo dados do funcionário"""
        app = MDApp.get_running_app()
        screen_manager = app.root

        target_screen = screen_manager.get_screen(screen_name)

        # Transfere todos os dados relevantes
        attributes = [
            "employee_name", "employee_function", "avatar", "contractor",
            "method_salary", "assess", "coexistence", "punctuality",
            "efficiency", "scale", "week_1", "week_2", "week_3", "week_4"
        ]
        if screen_name == 'WorkingMonth':
            attributes.append('days_work')

        for attr in attributes:
            setattr(target_screen, attr, getattr(self, attr))

        screen_manager.current = screen_name

    def value(self):
        return '{:.2f}'.format(self.salary)

    def back_table(self):
        """Volta para a tela de tabela"""
        self.manager.transition = SlideTransition(direction="right")
        self._navigate_to_screen('Table')

    def next_punctuality(self):
        """Navega para a tela de avaliação de pontualidade"""
        self.manager.transition = SlideTransition(direction="left")
        self._navigate_to_screen("AssesPunctuality")

    def next_efficiency(self):
        """Navega para a tela de avaliação de eficiência"""
        self.manager.transition = SlideTransition(direction="left")
        self._navigate_to_screen("AssesEfficiency")

    def next_coexistence(self):
        """Navega para a tela de avaliação de convivência"""
        self.manager.transition = SlideTransition(direction="left")
        self._navigate_to_screen("AssesCoexistence")

    def next_working_days(self):
        """Navega para a tela de trabalho semanal"""
        if self.method_salary in ('Semanal', 'Diaria'):
            self._navigate_to_screen('WorkingDays')
        elif self.method_salary in 'Quinzenal':
            pass
        else:
            self.manager.transition = SlideTransition(direction="left")
            self._navigate_to_screen('WorkingMonth')
