import os
import threading
import cloudinary
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
import matplotlib.pyplot as plt


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cloudinary.config(
            cloud_name="dsmgwupky",
            api_key="256987432736353",
            api_secret="K8oSFMvqA6N2eU4zLTnLTVuArMU"
        )

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
        # Dados
        dias_trabalhados = self.days_work
        faltas = self.faults

        # Criar o gráfico de pizza
        plt.figure(figsize=(6, 6))
        sizes = [dias_trabalhados, faltas]
        colors = [[0.0, 1.0, 0.0, 1.0], 'red']
        explode = (0.1, 0)

        plt.pie(
            sizes,
            explode=explode,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={
                'color': 'black',
                'fontsize': 16,
                'weight': 'bold'
            }
        )
        plt.axis('equal')
        plt.axis('off')

        # Salvar a imagem localmente
        local_image_path = 'chart.png'
        plt.savefig(local_image_path, transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close()

        # Executar o upload em uma thread separada

        threading.Thread(target=self.perform_upload, args=(local_image_path,)).start()

    def perform_upload(self, local_image_path):
        try:
            # Upload da imagem com corte circular
            response = cloudinary.uploader.upload(
                local_image_path,
                public_id=self.employee_name,
                overwrite=True,
                transformation=[
                    {'width': 1000, 'height': 1000, 'crop': 'thumb', 'gravity': 'face', 'radius': 'max'}
                ]
            )

            # Agendar a atualização da interface gráfica no thread principal do Kivy
            Clock.schedule_once(lambda dt: self.update_graphic_source(response['secure_url']))

        except Exception as e:
            print(f"Erro ao enviar imagem para o Cloudinary: {e}")

        finally:
            # Excluir a imagem local após o upload
            if os.path.exists(local_image_path):
                os.remove(local_image_path)
                print("Imagem local excluída.")

    def update_graphic_source(self, image_url):
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
