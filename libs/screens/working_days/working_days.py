from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse


from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget


class PizzaWidget(Widget):
    def __init__(self, dias_trabalhados=1, dias_falta=1, **kwargs):
        super().__init__(**kwargs)
        self.dias_trabalhados = dias_trabalhados
        self.dias_falta = dias_falta
        self.calcular_porcentagens()
        self.bind(size=self.redraw_pizza)  # Redesenha o gráfico quando o tamanho muda

    def calcular_porcentagens(self):
        total_dias = self.dias_trabalhados + self.dias_falta
        self.freq_presenca = (self.dias_trabalhados / total_dias) * 100
        self.freq_faltas = 100 - self.freq_presenca

    def redraw_pizza(self, *args):
        self.canvas.clear()  # Limpa o canvas antes de redesenhar
        self.draw_pizza()

    def draw_pizza(self):
        angulo_presenca = (self.freq_presenca / 100) * 360
        angulo_faltas = 360 - angulo_presenca

        with self.canvas:
            # Calcula o tamanho da pizza com base no tamanho do widget
            pizza_size = min(self.size) * 0.8  # 80% do menor lado (largura ou altura)
            center_x = self.center_x - pizza_size / 23
            center_y = self.center_y - pizza_size / 2

            # Desenha a parte verde (presença)
            Color(0, 1, 0, 1)  # Verde
            Ellipse(pos=(center_x, center_y), size=(pizza_size, pizza_size), angle_start=0, angle_end=angulo_presenca)

            # Desenha a parte vermelha (faltas)
            Color(1, 0, 0, 1)  # Vermelho
            Ellipse(pos=(center_x, center_y), size=(pizza_size, pizza_size), angle_start=angulo_presenca, angle_end=360)


class WorkingDays(MDScreen):
    scale = '5x2'
    method_salary = 'Diaria'
    employee_name = 'Helem'
    days_work = 0
    faults = 5
    seg = 0
    terc = 0
    quart = 0
    quint = 0
    sex = 0
    sab = 0


    def on_enter(self):
        if self.scale in '6x1':
            self.faults = 6
        elif self.scale in '5x2':
            self.faults = 5
        else:
            self.faults = 4

        self.upload_days()
        self.upload_graphic()

    def upload_graphic(self):
        # Cria o widget PizzaWidget com as variáveis de dias trabalhados e faltas
        pizza_widget = PizzaWidget(dias_trabalhados=self.days_work, dias_falta=self.faults)

        # Defina o tamanho fixo do widget
        pizza_widget.size = (200, 200)  # Aqui você define o tamanho do PizzaWidget
        pizza_widget.size_hint = None, None  # Isso desabilita o redimensionamento automático

        # Centraliza o widget dentro do layout
        pizza_widget.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Adiciona o PizzaWidget ao layout
        self.ids.graphic.add_widget(pizza_widget)


    def upload_days(self):
        dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado']

        for dia in dias:
            if self.scale in '6x1':
                # Layout principal horizontal
                main_layout = MDBoxLayout(
                    orientation='horizontal',
                    theme_bg_color='Custom',
                    md_bg_color='white',
                    size_hint=(0.86, 0.02),
                    pos_hint={'center_x': 0.5, 'center_y': 0.47},
                    padding=[0, 0, 35, 0]
                )

                # Primeiro MDBoxLayout (para o rótulo "Terça-feira")
                label_layout = MDBoxLayout(
                    theme_bg_color='Custom',
                    md_bg_color='white',
                    spacing=5,
                    padding=[20, 0, 0, 0]
                )

                label = MDLabel(
                    text=dia,
                    theme_text_color='Custom',
                    text_color='black'
                )
                label_layout.add_widget(label)

                # Segundo MDBoxLayout (para o ícone de checkbox)
                icon_layout = MDBoxLayout(
                    theme_bg_color='Custom',
                    md_bg_color='white',
                    spacing=0,
                    size_hint=(None, None),  # Define o tamanho do botão como None para que ele não ocupe todo o espaço
                    size=(48, 48),
                    pos_hint={'center_x': 0.9}
                )

                icon_button = MDIconButton(
                    icon='checkbox-blank-circle-outline',
                    halign='center',
                    size_hint=(None, None),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                )

                self.ids[f"icon_{dia.replace('-', '_')}"] = icon_button
                print(icon_button.id)
                icon_button.bind(on_release=lambda instance, d=dia: self.on_checkbox_press(d))
                icon_layout.add_widget(icon_button)

                # Adicionar os layouts ao layout principal
                main_layout.add_widget(label_layout)
                main_layout.add_widget(icon_layout)
                self.ids.main_scroll.add_widget(main_layout)

            elif self.scale in '5x2':
                if dia not in 'Sabado':
                    # Layout principal horizontal
                    main_layout = MDBoxLayout(
                        orientation='horizontal',
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47},
                        padding=[0, 0, 35, 0]
                    )

                    # Primeiro MDBoxLayout (para o rótulo "Terça-feira")
                    label_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=5,
                        padding=[20, 0, 0, 0]
                    )

                    label = MDLabel(
                        text=dia,
                        theme_text_color='Custom',
                        text_color='black'
                    )
                    label_layout.add_widget(label)

                    # Segundo MDBoxLayout (para o ícone de checkbox)
                    icon_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=0,
                        size_hint=(None, None),
                        # Define o tamanho do botão como None para que ele não ocupe todo o espaço
                        size=(48, 48),
                        pos_hint={'center_x': 0.9}
                    )

                    icon_button = MDIconButton(
                        icon='checkbox-blank-circle-outline',
                        halign='center',
                        size_hint=(None, None),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}
                    )

                    self.ids[f"icon_{dia.replace('-', '_')}"] = icon_button
                    print(icon_button.id)
                    icon_button.bind(on_release=lambda instance, d=dia: self.on_checkbox_press(d))
                    icon_layout.add_widget(icon_button)

                    # Adicionar os layouts ao layout principal
                    main_layout.add_widget(label_layout)
                    main_layout.add_widget(icon_layout)
                    self.ids.main_scroll.add_widget(main_layout)
                else:
                    # Layout principal horizontal
                    main_layout = MDBoxLayout(
                        orientation='horizontal',
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47},
                        padding=[0, 0, 40, 0]
                    )

                    # Primeiro MDBoxLayout (para o rótulo "Terça-feira")
                    label_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=15,
                        padding=[20, 0, 0, 0]
                    )

                    label = MDLabel(
                        text=dia,
                        theme_text_color='Custom',
                        text_color='black'
                    )
                    label_layout.add_widget(label)

                    # Segundo MDBoxLayout (para o ícone de checkbox)
                    icon_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=5,
                        padding=[0, 0, 0, 0]
                    )

                    icon_button = MDLabel(
                        text='Folga',
                        theme_text_color='Custom',
                        text_color=[0.0, 1.0, 0.0, 1.0],
                        pos_hint={'center_x': 0.9, 'center_y': 0.5},
                        halign='right'
                    )

                    self.ids[f"icon_{dia.replace('-', '_')}"] = icon_button
                    print(icon_button.id)
                    icon_button.bind(on_release=lambda instance, d=dia: self.on_checkbox_press(d))
                    icon_layout.add_widget(icon_button)

                    # Adicionar os layouts ao layout principal
                    main_layout.add_widget(label_layout)
                    main_layout.add_widget(icon_layout)
                    self.ids.main_scroll.add_widget(main_layout)
            else:

                if dia not in ('Sexta-feira', 'Sabado'):
                    # Layout principal horizontal
                    main_layout = MDBoxLayout(
                        orientation='horizontal',
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47},
                        padding=[0, 0, 35, 0]
                    )

                    # Primeiro MDBoxLayout (para o rótulo "Terça-feira")
                    label_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=5,
                        padding=[20, 0, 0, 0]
                    )

                    label = MDLabel(
                        text=dia,
                        theme_text_color='Custom',
                        text_color='black'
                    )
                    label_layout.add_widget(label)

                    # Segundo MDBoxLayout (para o ícone de checkbox)
                    icon_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=0,
                        size_hint=(None, None),
                        # Define o tamanho do botão como None para que ele não ocupe todo o espaço
                        size=(48, 48),
                        pos_hint={'center_x': 0.9}
                    )

                    icon_button = MDIconButton(
                        icon='checkbox-blank-circle-outline',
                        halign='center',
                        size_hint=(None, None),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}
                    )

                    self.ids[f"icon_{dia.replace('-', '_')}"] = icon_button
                    print(icon_button.id)
                    icon_button.bind(on_release=lambda instance, d=dia: self.on_checkbox_press(d))
                    icon_layout.add_widget(icon_button)

                    # Adicionar os layouts ao layout principal
                    main_layout.add_widget(label_layout)
                    main_layout.add_widget(icon_layout)
                    self.ids.main_scroll.add_widget(main_layout)
                else:
                    # Layout principal horizontal
                    main_layout = MDBoxLayout(
                        orientation='horizontal',
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47},
                        padding=[0, 0, 40, 0]
                    )

                    # Primeiro MDBoxLayout (para o rótulo "Terça-feira")
                    label_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=5,
                        padding=[20, 0, 0, 0]
                    )

                    label = MDLabel(
                        text=dia,
                        theme_text_color='Custom',
                        text_color='black'
                    )
                    label_layout.add_widget(label)

                    # Segundo MDBoxLayout (para o ícone de checkbox)
                    icon_layout = MDBoxLayout(
                        theme_bg_color='Custom',
                        md_bg_color='white',
                        spacing=5,
                        padding=[0, 0, 0, 0]
                    )

                    icon_button = MDLabel(
                        text='Folga',
                        theme_text_color='Custom',
                        text_color=[0.0, 1.0, 0.0, 1.0],
                        pos_hint={'center_x': 0.9, 'center_y': 0.5},
                        halign='right'
                    )

                    self.ids[f"icon_{dia.replace('-', '_')}"] = icon_button
                    print(icon_button.id)
                    icon_button.bind(on_release=lambda instance, d=dia: self.on_checkbox_press(d))
                    icon_layout.add_widget(icon_button)

                    # Adicionar os layouts ao layout principal
                    main_layout.add_widget(label_layout)
                    main_layout.add_widget(icon_layout)
                    self.ids.main_scroll.add_widget(main_layout)

    def on_checkbox_press(self, dia):
        if dia == 'Segunda-feira':
            if self.seg == 0:
                self.seg += 1
                self.faults -= 1
                self.days_work += 1

                self.ids.icon_Segunda_feira.icon = 'checkbox-blank-circle'
            else:
                self.seg = 0
                self.faults += 1
                self.days_work -= 1

                self.ids.icon_Segunda_feira.icon = 'checkbox-blank-circle-outline'

        elif dia == 'Terça-feira':
            if self.terc == 0:
                self.terc += 1
                self.faults -= 1
                self.days_work += 1

                self.ids.icon_Terça_feira.icon = 'checkbox-blank-circle'
            else:
                self.terc = 0
                self.faults += 1
                self.days_work -= 1

                self.ids.icon_Terça_feira.icon = 'checkbox-blank-circle-outline'

        elif dia == 'Quarta-feira':
            if self.quart == 0:
                self.quart += 1
                self.faults -= 1
                self.days_work += 1

                self.ids.icon_Quarta_feira.icon = 'checkbox-blank-circle'
            else:
                self.quart = 0
                self.faults += 1
                self.days_work -= 1
                self.ids.icon_Quarta_feira.icon = 'checkbox-blank-circle-outline'

        elif dia == 'Quinta-feira':
            if self.quint == 0:
                self.quint += 1
                self.ids.icon_Quinta_feira.icon = 'checkbox-blank-circle'
                self.faults -= 1
                self.days_work += 1

            else:
                self.quint = 0
                self.faults += 1
                self.days_work -= 1

                self.ids.icon_Quinta_feira.icon = 'checkbox-blank-circle-outline'

        elif dia == 'Sexta-feira':
            if self.sex == 0:
                self.sex += 1
                self.ids.icon_Sexta_feira.icon = 'checkbox-blank-circle'
                self.faults -= 1
                self.days_work += 1

            else:
                self.sex = 0
                self.faults += 1
                self.days_work -= 1
                self.ids.icon_Sexta_feira.icon = 'checkbox-blank-circle-outline'

        else:
            if self.sab == 0:
                self.sab += 1
                self.ids.icon_Sabado.icon = 'checkbox-blank-circle'
                self.faults -= 1
                self.days_work += 1

            else:
                self.sab = 0
                self.faults += 1
                self.days_work -= 1
                self.ids.icon_Sabado.icon = 'checkbox-blank-circle-outline'

        self.upload_graphic()

