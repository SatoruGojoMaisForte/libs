from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import SlideTransition
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp


class PizzaWidget(Widget):
    def __init__(self, dias_trabalhados=1, dias_falta=0, total_dias=0, **kwargs):
        super().__init__(**kwargs)
        self.dias_trabalhados = dias_trabalhados
        self.dias_falta = dias_falta
        self.total_dias = total_dias
        self.calcular_porcentagens()
        self.bind(size=self.redraw_pizza)
        self.bind(pos=self.redraw_pizza)  # Redesenha quando a posição muda também

    def calcular_porcentagens(self):
        total_dias = self.total_dias
        if total_dias > 0:  # Previne divisão por zero
            self.freq_presenca = (self.dias_trabalhados / total_dias) * 100
        else:
            self.freq_presenca = 0
        self.freq_faltas = 100 - self.freq_presenca

    def redraw_pizza(self, *args):
        self.canvas.clear()
        self.draw_pizza()

    def draw_pizza(self):
        angulo_presenca = (self.freq_presenca / 100) * 360
        angulo_faltas = 360 - angulo_presenca

        with self.canvas:
            # Calcula o tamanho da pizza apropriadamente com base nas dimensões do widget
            pizza_size = min(self.width, self.height) * 0.8
            center_x = self.center_x - pizza_size / 2  # Centraliza a pizza horizontalmente
            center_y = self.center_y - pizza_size / 2  # Centraliza a pizza verticalmente

            # Desenha a parte verde (presença)
            Color(46/255, 249/255, 255/255, 1)  # Verde
            Ellipse(pos=(center_x, center_y), size=(pizza_size, pizza_size), angle_start=0, angle_end=angulo_presenca)

            # Desenha a parte vermelha (faltas)
            Color(234/255, 43/255, 31/255, 1)  # Vermelho
            Ellipse(pos=(center_x, center_y), size=(pizza_size, pizza_size), angle_start=angulo_presenca, angle_end=360)


class WorkingMonth(MDScreen):
    employee_name = StringProperty()
    contractor = StringProperty()
    week_1 = NumericProperty()
    week_2 = NumericProperty()
    week_3 = NumericProperty()
    week_4 = NumericProperty()
    scale = StringProperty()
    avatar = StringProperty()
    days_work = NumericProperty()
    cont_pizza = NumericProperty()

    def on_enter(self):
        print(self.employee_name, self.contractor, self.scale)
        print(self.employee_name, self.contractor, self.scale)
        self.cont_pizza += 1
        self.days_work = self.week_1 + self.week_2 + self.week_3 + self.week_4
        self.ids.graphic.clear_widgets()
        self.upload_graphic()
        self.upload_percenteges()

    def upload_percenteges(self):
        """Calcular a porcentagem de dias trabalhados de cada funcionario"""
        numb_days = 0
        if self.scale in '6x1':
            numb_days = 6
        elif self.scale in '5x2':
            numb_days = 20 / 4
        else:
            numb_days = 16 / 4

        freq_week1 = (self.week_1 / numb_days) * 100
        freq_week2 = (self.week_2 / numb_days) * 100
        freq_week3 = (self.week_3 / numb_days) * 100
        freq_week4 = (self.week_4 / numb_days) * 100
        self.ids.week_1.text = '{:.2f}%'.format(freq_week1)
        self.ids.week_2.text = '{:.2f}%'.format(freq_week2)
        self.ids.week_3.text = '{:.2f}%'.format(freq_week3)
        self.ids.week_4.text = '{:.2f}%'.format(freq_week4)

    def get_days_month(self):
        """Retorna quantos dias um mes possui"""
        import datetime
        from calendar import monthrange

        year = datetime.date.today().year
        month = datetime.date.today().month

        s, tot_day = monthrange(year, month)
        return tot_day

    def calculate_work_days(self, total_days, work_schedule):
        """ Calcular quantos dias o funcionario vai trabalhar de acordo com
        a escala de trabalho e o total de dias do mes

        :param total_days:
        :param work_schedule:
        :return: days_work
        """
        schedule_base_days = {
            '6x1': 26 if total_days == 24 else 24 if total_days == 30 else 24,
            '5x2': 20 if total_days == 31 else 20 if total_days == 30 else 20,
            'default': 16 if total_days == 31 else 16 if total_days == 30 else 16
        }

        # Return the calculated working days based on schedule
        return schedule_base_days.get(work_schedule, schedule_base_days['default'])

    def calcular_porcentagens(self):
        tot_day_work = self.calculate_work_days(self.get_days_month(), self.scale)
        print(tot_day_work)

        if tot_day_work > 0:  # Previne divisão por zero
            self.freq_presenca = (self.days_work / tot_day_work) * 100
        else:
            self.freq_presenca = 0
        self.freq_faltas = 100 - self.freq_presenca
        self.ids.percentege_present.text = '{:.2f}%'.format(self.freq_presenca)
        self.ids.percentege_faults.text = '{:.2f}%'.format(self.freq_faltas)

    def upload_graphic(self):
        # Cria o widget do gráfico de pizza
        tot_day_work = self.calculate_work_days(self.get_days_month(), self.scale)
        pizza_widget = PizzaWidget(dias_trabalhados=self.days_work, dias_falta=22 - self.days_work, total_dias=tot_day_work)

        # Define tamanho fixo e desativa redimensionamento automático
        pizza_widget.size_hint = (None, None)
        pizza_widget.size = (dp(180), dp(180))  # Tamanho ajustado para melhores proporções

        # Centraliza o widget no layout
        pizza_widget.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Adiciona ao layout
        self.ids.graphic.add_widget(pizza_widget)
        # Calcular a porra das porcentagens
        self.calcular_porcentagens()

    def back_evaluation(self):
        app = MDApp.get_running_app()
        root = app.root
        evaluation = root.get_screen('Evaluation')
        evaluation.week_1 = self.week_1
        evaluation.week_2 = self.week_2
        evaluation.week_3 = self.week_3
        evaluation.week_4 = self.week_4
        root.transition = SlideTransition(direction='right')
        root.current = 'Evaluation'

    def _next_first_week(self):
        app = MDApp.get_running_app()
        root = app.root
        first = root.get_screen('FirstWeek')
        first.scale = self.scale
        first.employee_name = self.employee_name
        first.contractor = self.contractor
        root.transition = SlideTransition(direction='left')
        root.current = 'FirstWeek'

    def _next_second_week(self):
        app = MDApp.get_running_app()
        root = app.root
        first = root.get_screen('SecondWeek')
        first.scale = self.scale
        first.employee_name = self.employee_name
        first.contractor = self.contractor
        root.transition = SlideTransition(direction='left')
        root.current = 'SecondWeek'

    def _next_third_week(self):
        app = MDApp.get_running_app()
        root = app.root
        first = root.get_screen('ThirdWeek')
        first.scale = self.scale
        first.employee_name = self.employee_name
        first.contractor = self.contractor
        root.transition = SlideTransition(direction='left')
        root.current = 'ThirdWeek'

    def _next_fourth_week(self):
        app = MDApp.get_running_app()
        root = app.root
        first = root.get_screen('FourthWeek')
        first.scale = self.scale
        first.employee_name = self.employee_name
        first.contractor = self.contractor
        root.transition = SlideTransition(direction='left')
        root.current = 'FourthWeek'
