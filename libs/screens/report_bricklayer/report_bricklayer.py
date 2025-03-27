import json
from ast import literal_eval
from datetime import datetime

from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, NumericProperty, get_color_from_hex
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemLeadingIcon, MDListItemSupportingText
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.textfield import MDTextField


class ReportBricklayer(MDScreen):
    avatar = StringProperty('https://res.cloudinary.com/dsmgwupky/image/upload/v1742170012/Helem.jpg')
    valleys = StringProperty("{}")
    key = StringProperty()
    day = StringProperty()
    remainder = StringProperty()
    employee_name = StringProperty('Helem')
    function = StringProperty('Bombeiro')
    tot = NumericProperty(0)
    salary = NumericProperty()
    two_sala = NumericProperty()
    method_salary = StringProperty()
    scale = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textfield = MDTextField()
        self.textfield.input_filter = "float"
        self.textfield.helper_text = "Digite aqui"
        self.textfield.helper_text_mode = "persistent"
        self.ids['text_field'] = self.textfield

        self.dialog = MDDialog()

        # ----------------------------Icon-----------------------------
        icon = MDDialogIcon(
            icon="refresh",
        )

        # -----------------------Headline text-------------------------
        headline = MDDialogHeadlineText(
            text="Adicionar vale",
        )

        # -----------------------Supporting text-----------------------
        supporting = MDDialogSupportingText(
            text="Digite o valor do vale pego pelo funcionario no campo abaixo",
        )

        # -----------------------Custom content------------------------
        container = MDDialogContentContainer(
            MDDivider(),
            self.textfield,
            MDDivider(),
            orientation="vertical",
        )

        # ---------------------Button container------------------------
        container_two = MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(text="Cancelar"),
                style="text",
                focus_behavior=False,
                on_release=lambda x: self.dialog.dismiss(),
            ),
            MDButton(
                MDButtonText(text="Adicionar"),
                style="text",
                focus_behavior=False,
                on_release=lambda x: self.add_valley()
            ),
            spacing="8dp",
        )

        # Add widgets to dialog
        self.dialog.add_widget(icon)
        self.dialog.add_widget(headline)
        self.dialog.add_widget(supporting)
        self.dialog.add_widget(container)
        self.dialog.add_widget(container_two)
        self.two_sala = self.salary

    def show_snackbar(self) -> None:
        """Exibe um Snackbar informativo."""
        self.dialog.dismiss()
        MDSnackbar(
            MDSnackbarText(
                text="Salario insuficiente para cobrir o vale",
                theme_text_color='Custom',
                text_color='black',
                bold=True
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            halign='center',
            size_hint_x=0.8,
            theme_bg_color='Custom',
            background_color=get_color_from_hex('#F3DE8A')
        ).open()

    def on_enter(self, *args):
        # Limpar widgets existentes antes de carregar novos
        self.ids.valleys.clear_widgets()
        self.load_valleys()
        if self.method_salary not in 'Empreita':
            self.ids.remain.text = f'Salario total: {self.salary}'
            self.ids.init.text = f'Escala de trabalho: {self.scale}'
        else:
            self.ids.init.text = f'Prazo inicial: {self.day}'
            self.ids.remain.text = f'Salario total: {self.salary}'

    def get_valleys_dict(self):
        """Método auxiliar para converter a string valleys em um dicionário"""
        try:
            if not self.valleys or self.valleys == "None":
                return {}
            valleys_dict = literal_eval(self.valleys)
            # Verificar se o resultado é realmente um dicionário
            if not isinstance(valleys_dict, dict):
                print(f"Warning: valleys não é um dicionário: {self.valleys}")
                return {}
            return valleys_dict
        except (ValueError, SyntaxError) as e:
            print(f"Erro ao converter valleys para dicionário: {e}, valor: {self.valleys}")
            return {}

    def load_valleys(self):
        valleys_dict = self.get_valleys_dict()
        print(f"Carregando vales: {valleys_dict}")

        total = 0
        for data, valley in valleys_dict.items():
            try:
                valley_value = int(valley)
                total += valley_value
                item = MDListItem(
                    MDListItemLeadingIcon(
                        icon='currency-usd',
                    ),
                    MDListItemHeadlineText(
                        text=f'R$ {valley_value}'
                    ),
                    MDListItemSupportingText(
                        text=f'retirado em {data}'
                    )
                )
                self.ids.valleys.add_widget(item)
            except (ValueError, TypeError) as e:
                print(f"Erro ao processar vale: {e}, data: {data}, valor: {valley}")

        self.tot = total
        self.ids.tot.text = f'Total: R${total}'

    def show_dialog(self):
        # Limpar o campo de texto antes de abrir o diálogo
        self.ids.text_field.text = ''
        self.dialog.open()

    def add_valley(self):
        # Verificar se o campo de texto está vazio
        if not self.ids.text_field.text:
            return

        try:
            # Obter o valor do vale como inteiro
            valley = int(self.ids.text_field.text)
            print('O valor do vale é {}'.format(valley))

            # Verificar se adicionar esse vale ultrapassaria o salário
            # Se o total atual + o novo vale for maior que o salário, mostrar mensagem de erro
            print(self.tot + valley)
            if (valley) > int(self.salary):
                self.show_snackbar()
            else:

                # Se chegou aqui, podemos adicionar o vale
                # Obter a data atual
                today = datetime.today().strftime('%d/%m/%Y-%H:%M:%S')  # Adicionando hora para evitar colisões

                # Obter o dicionário de vales existente
                valleys_dict = self.get_valleys_dict()

                # Adicionar o novo vale ao dicionário
                valleys_dict[today] = valley

                # Criar e adicionar o item à lista
                item = MDListItem(
                    MDListItemLeadingIcon(
                        icon='currency-usd',
                    ),
                    MDListItemHeadlineText(
                        text=f'R$ {valley}'
                    ),
                    MDListItemSupportingText(
                        text=f'retirado em {today}'
                    )
                )
                self.ids.valleys.add_widget(item)

                # Atualizar o total
                self.tot += valley
                self.ids.tot.text = f'Total: R${self.tot}'

                # Atualizar a propriedade valleys como string - IMPORTANTE
                self.valleys = str(valleys_dict)
                print(f"Vales após adicionar: {self.valleys}")

                # Fechar o diálogo e limpar o campo de texto
                self.dialog.dismiss()
                self.ids.text_field.text = ''

                # Atualizar o salário restante
                self.salary = int(self.salary) - valley

                # Enviar os dados atualizados para o Firebase
                self.upload_firebase()

        except ValueError:
            print("Valor inválido. Digite um número inteiro.")

    def upload_firebase(self):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{self.key}/.json'

        # Garantir que estamos enviando um dicionário válido para o Firebase
        valleys_dict = self.get_valleys_dict()

        # Registro para depuração
        print(f"Enviando para Firebase - key: {self.key}, vales: {valleys_dict}")

        data = {}  # Inicializar um dicionário vazio para os dados

        # Adicionar os vales apenas se não estiverem vazios
        if valleys_dict:
            data['valleys'] = f'{valleys_dict}'

        # Adicionar o total
        data['tot'] = self.tot

        # Log para depuração
        print(f"Dados que serão enviados: {data}")

        # Converter para JSON e enviar
        json_data = json.dumps(data)
        print(f"JSON a ser enviado: {json_data}")

        UrlRequest(
            url,
            method='PATCH',
            on_success=self.final_upload,
            on_error=self.error,
            req_body=json_data
        )

    def error(self, instance, erro):
        print(f"Erro ao enviar dados para o Firebase: {erro}")

    def cancel(self):
        app = MDApp.get_running_app()
        screenmanager = app.root
        e = screenmanager.get_screen('Evaluation')
        e.valleys = self.valleys
        e.tot = self.tot
        self.tot = 0
        self.ids.valleys.clear_widgets()
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'Evaluation'

    def final_upload(self, instance, result):
        print(f"Dados enviados com sucesso: {result}")

    def restart_firebase(self):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{self.key}/.json'
        json_data = {
            'tot': 0,
            'valleys': "{}"
        }
        UrlRequest(
            url,
            method='PATCH',
            on_success=self.final_restart,
            on_error=self.error,
            req_body=json.dumps(json_data)
        )

    def final_restart(self, instance, result):
        self.ids.valleys.clear_widgets()
        self.tot = 0
        self.valleys = "{}"
        self.salary = self.two_sala
        self.ids.tot.text = f'Total: R$0'
        self.dont = 'Sim'
        app = MDApp.get_running_app()
        screenmanager = app.root
        e = screenmanager.get_screen('Evaluation')
        e.valleys = "{}"
        e.tot = 0
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Evaluation'
