from kivy.network.urlrequest import UrlRequest
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class WorkingDays(MDScreen):
    scale = '6x1'
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

        self.upload_graphic()
        self.upload_days()

    def upload_graphic(self):
        url = f'https://api-graphic.onrender.com/graphic?days_work={self.days_work}&faults={self.faults}&employee_name={self.employee_name}'
        UrlRequest(
            url,
            method='GET',
            on_success=self.graphic_update
        )

    def graphic_update(self, isntance, image_url):
        """
        Atualiza a fonte da imagem no widget graphic.
        Esta função é chamada no thread principal do Kivy.
        """

        self.ids.graphic.source = image_url

    def upload_days(self):
        dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado']

        for dia in dias:
            if self.scale in '6x1':
                # Layout principal horizontal
                main_layout = MDBoxLayout(
                    orientation='horizontal',
                    theme_bg_color='Custom',
                    md_bg_color='black',
                    size_hint=(0.86, 0.02),
                    pos_hint={'center_x': 0.5, 'center_y': 0.47}
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
                    padding=[60, 0, 0, 0]
                )

                icon_button = MDIconButton(
                    icon='checkbox-blank-circle-outline',
                    halign='center',
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
                        md_bg_color='black',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47}
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
                        padding=[60, 0, 0, 0]
                    )

                    icon_button = MDIconButton(
                        icon='checkbox-blank-circle-outline',
                        halign='center',
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
                        md_bg_color='black',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47}
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
                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                        halign='center'
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
                        md_bg_color='black',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47}
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
                        padding=[60, 0, 0, 0]
                    )

                    icon_button = MDIconButton(
                        icon='checkbox-blank-circle-outline',
                        halign='center',
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
                        md_bg_color='black',
                        size_hint=(0.86, 0.02),
                        pos_hint={'center_x': 0.5, 'center_y': 0.47}
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
                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                        halign='center'
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
