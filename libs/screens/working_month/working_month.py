from kivy.properties import StringProperty, NumericProperty
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp

class PizzaWidget(Widget):
    def __init__(self, dias_trabalhados=1, dias_falta=1, **kwargs):
        super().__init__(**kwargs)
        self.dias_trabalhados = dias_trabalhados
        self.dias_falta = dias_falta
        self.calcular_porcentagens()
        self.bind(size=self.redraw_pizza)
        self.bind(pos=self.redraw_pizza)  # Redesenha quando a posição muda também

    def calcular_porcentagens(self):
        total_dias = self.dias_trabalhados + self.dias_falta
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
    avatar = StringProperty('https://res.cloudinary.com/dsmgwupky/image/upload/v1740073423/Ariah.jpg')
    days_work = 2
    faults = NumericProperty(22)

    def on_enter(self):
        self.upload_graphic()

    def calcular_porcentagens(self):
        total_dias = self.days_work + self.faults
        if total_dias > 0:  # Previne divisão por zero
            self.freq_presenca = (self.days_work / total_dias) * 100
        else:
            self.freq_presenca = 0
        self.freq_faltas = 100 - self.freq_presenca

    def upload_graphic(self):
        # Cria o widget do gráfico de pizza
        pizza_widget = PizzaWidget(dias_trabalhados=self.days_work, dias_falta=self.faults)

        # Define tamanho fixo e desativa redimensionamento automático
        pizza_widget.size_hint = (None, None)
        pizza_widget.size = (dp(180), dp(180))  # Tamanho ajustado para melhores proporções

        # Centraliza o widget no layout
        pizza_widget.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Adiciona ao layout
        self.ids.graphic.add_widget(pizza_widget)
        # Calcular a porra das porcentagens
        self.calcular_porcentagens()

