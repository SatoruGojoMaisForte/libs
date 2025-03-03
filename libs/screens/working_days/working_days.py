from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemTrailingIcon, \
    MDListItemTrailingSupportingText, MDListItemTrailingCheckbox
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
            Color(0, 1, 0, 1)  # Verde
            Ellipse(pos=(center_x, center_y), size=(pizza_size, pizza_size), angle_start=0, angle_end=angulo_presenca)

            # Desenha a parte vermelha (faltas)
            Color(1, 0, 0, 1)  # Vermelho
            Ellipse(pos=(center_x, center_y), size=(pizza_size, pizza_size), angle_start=angulo_presenca, angle_end=360)


class WorkingDays(MDScreen):
    scale = '5x2'  # Escala padrão
    method_salary = 'Diaria'
    employee_name = 'Helem'
    days_work = 0
    faults = 5  # Padrão para escala 5x2

    # Variáveis de controle dos dias
    seg = 0
    terc = 0
    quart = 0
    quint = 0
    sex = 0
    sab = 0

    def on_enter(self):

        # Limpa widgets existentes para evitar duplicatas ao reentrar na tela
        self.ids.main_scroll.clear_widgets()
        self.ids.graphic.clear_widgets()

        # Inicializa faltas com base na escala de trabalho
        if self.scale == '6x1':
            self.faults = 6
        elif self.scale == '5x2':
            self.faults = 5
        else:  # 4x3
            self.faults = 4

        # Cria a lista de dias e o gráfico
        self.upload_days()
        self.upload_graphic()

    def calcular_porcentagens(self):
        total_dias = self.days_work + self.faults
        if total_dias > 0:  # Previne divisão por zero
            self.freq_presenca = (self.days_work / total_dias) * 100
        else:
            self.freq_presenca = 0
        self.freq_faltas = 100 - self.freq_presenca
        self.ids.faults.text = f'{self.freq_faltas}%'
        self.ids.present.text = f'{self.freq_presenca}%'

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

    def upload_days(self):
        dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado']

        for dia in dias:
            # Verifica se é um dia de folga com base na escala
            is_folga = (self.scale == '5x2' and dia == 'Sabado') or \
                       (self.scale == '4x3' and (dia == 'Sexta-feira' or dia == 'Sabado'))
            list_item = MDListItem(
                MDListItemHeadlineText(
                    text=dia
                ),
                pos_hint={'center_x': 0.5},
                size_hint=(1, None),
                theme_bg_color='Custom',
                md_bg_color='white'
            )
            safe_dia = dia.replace('-', '_')

            if not is_folga:
                # Cria botão de checkbox
                icon_button = MDListItemTrailingCheckbox(

                )

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

            # Atualiza o gráfico após alterar os dados de presença
            self.ids.graphic.clear_widgets()
            self.upload_graphic()

    def back_evaluation(self):
        # Método para lidar com o pressionamento do botão voltar
        # Você precisará implementar isso com base na navegação do seu aplicativo
        pass
