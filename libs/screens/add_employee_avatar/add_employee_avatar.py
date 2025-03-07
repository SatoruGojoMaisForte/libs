import json
import cloudinary
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from plyer import filechooser


class EmployeeAvatar(MDScreen):
    name_employee = StringProperty()
    function = StringProperty()
    contractor = StringProperty()
    method_salary = StringProperty()
    salary = StringProperty()
    scale = StringProperty()
    dont = 'Sim'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('FUnção', self.function)
        print('Metodo de recebimento', self.method_salary)
        print('Valor do salario', self.salary)
        print('Escala do trabalho', self.scale)
        cloudinary.config(
            cloud_name="dsmgwupky",
            api_key="256987432736353",
            api_secret="K8oSFMvqA6N2eU4zLTnLTVuArMU"
        )
        # Cria o MDCard
        self.card = MDCard(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            line_color=(0.5, 0.5, 0.5, 1),  # Cor da borda
            theme_bg_color='Custom',
            md_bg_color='white',
            md_bg_color_disabled="white",

        )

        # Cria o layout relativo para organizar os elementos dentro do card
        relative_layout = MDRelativeLayout()

        # Adiciona a AsyncImage (imagem assíncrona)
        async_image = AsyncImage(
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1739053352/image_1_hkgebk.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        relative_layout.add_widget(async_image)

        # Adiciona o primeiro MDLabel ("Tudo certo!!")
        label_title = MDLabel(
            text='Tudo certo!!',
            bold=True,
            halign='center',
            font_style='Headline',  # Equivalente a 'Headline'
            pos_hint={'center_x': 0.5, 'center_y': 0.47},
            theme_text_color='Custom',
            text_color=(0, 0, 0, 1)  # Cor preta
        )
        relative_layout.add_widget(label_title)

        # Adiciona o segundo MDLabel (mensagem de sucesso)
        label_message = MDLabel(
            text='O funcionário foi adicionado com sucesso. Verifique na sua tabela.',
            font_style='Label',  # Equivalente a 'Label'
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            padding=(20, 0),
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1)  # Cor cinza
        )
        relative_layout.add_widget(label_message)

        # adiciona o botão para proxima pagina
        button = MDButton(
            MDButtonText(
                text='Ok',
                theme_text_color='Custom',
                text_color='white',
                halign='center',
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                font_style='Title',
                role='medium',
                bold=True
            ),
            theme_width='Custom',
            size_hint_x=.3,
            theme_bg_color='Custom',
            md_bg_color=[0.0, 1.0, 0.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
        )
        self.ids['ok'] = button
        self.ids.ok.on_release = self.back_table
        relative_layout.add_widget(button)
        # Adiciona o layout relativo ao card
        self.card.add_widget(relative_layout)

    def back_employee(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Add'

    # Funções de imagem ------------------------------------------------------------------------------------------------

    def recortar_imagem_circular(self, imagem_path):
        try:
            # Upload da imagem com corte circular
            response = cloudinary.uploader.upload(
                imagem_path,
                public_id=self.name_employee,
                overwrite=True,
                transformation=[
                    {'width': 1000, 'height': 1000, 'crop': 'thumb', 'gravity': 'face', 'radius': 'max'}
                ]
            )
            self.ids.perfil.source = response['secure_url']  # Retorna o URL da imagem cortada
            self.post_employee()
        except Exception as e:
            print(f"Erro ao cortar a imagem: {e}")
            return None

    def open_gallery(self):
        if self.dont == 'Não':
            print('Galeria não atualizada')
        else:
            '''Abre a galeria para selecionar uma imagem.'''
            try:
                filechooser.open_file(
                    filters=["*.jpg", "*.png", "*.jpeg"],  # Filtra por tipos de arquivo de imagem
                    on_selection=self.select_path  # Chama a função de callback ao selecionar o arquivo
                )
            except Exception as e:
                print("Erro ao abrir a galeria:", e)

    def select_path(self, selection):
        '''
        Callback chamada quando um arquivo é selecionado.

        :param selection: lista contendo o caminho do arquivo selecionado.
        '''
        if selection:
            path = selection[0]  # Obtém o caminho do arquivo
            self.recortar_imagem_circular(path)
            MDSnackbar(
                MDSnackbarText(
                    text=f"Arquivo selecionado: {path}",
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
            ).open()

    # manipulando o banco de dados -------------------------------------------------------------------------------------
    def post_employee(self):
        print('Começando cadastro')
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios'
        data = {
            'Name': self.name_employee,
            'function': self.function,
            'salary': self.salary,
            'avatar': self.ids.perfil.source,
            'contractor': self.contractor,
            'efficiency': 0,
            'method_salary': self.method_salary,
            'scale': self.scale,
            'feedback': 0,
            'frequency': 0,
            'punctuality': 0,
            'coexistence': 0,
            'week_1': 0,
            'week_2': 0,
            'week_3': 0,
            'week_4': 0,
            'days_work': 0,
            'work_days_week1': '[]',
            'work_days_week2': '[]',
            'work_days_week3': '[]',
            'work_days_week4': '[]'
        }

        UrlRequest(
            f'{url}/.json',
            req_body=json.dumps(data),
            method='POST',
            on_success=self.added_successfully
        )

    def added_successfully(self, req, result):
        self.add_widget(self.card)

    def post_employ_no_avatar(self):
        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios'
        data = {
            'Name': self.name_employee,
            'function': self.function,
            'salary': self.salary,
            'avatar': 'https://res.cloudinary.com/dsmgwupky/image/upload/v1731970845/image_3_uiwlog.png',
            'contractor': self.contractor,
            'efficiency': 0,
            'method_salary': self.method_salary,
            'scale': self.scale,
            'feedback': 0,
            'frequency': 0,
            'punctuality': 0,
            'work_days_week1': '[]',
            'work_days_week2': '[]',
            'work_days_week3': '[]',
            'work_days_week4': '[]'
        }

        UrlRequest(
            f'{url}/.json',
            req_body=json.dumps(data),
            method='POST',
            on_success=self.added_successfully
        )

    def back_table(self):
        self.manager.transition = SlideTransition(direction='left')
        self.remove_widget(self.card)
        self.manager.current = 'Table'
