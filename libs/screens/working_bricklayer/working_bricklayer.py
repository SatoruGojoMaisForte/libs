import json
from datetime import datetime

from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbarText, MDSnackbar


class WorkingBricklayer(MDScreen):
    key = StringProperty('-OKmtfC8Am5v51vjif3L')
    salary = NumericProperty(1500)
    function = StringProperty('Analista de Sistemas')
    ultimate = StringProperty('31/03/2025')
    observations = StringProperty('Sem observações')

    def on_enter(self, *args):
        """ Criando os principais elementos dessa tela """
        # Carregando os dados
        self.ids.data_picker.text = f'{self.ultimate}'
        self.ids.text_work.text = f'{self.function}'
        self.ids.salary.text = f'{self.salary}'

        # Criando o data picker para gerenciar a data
        self.date_dialog = MDModalDatePicker()
        self.date_dialog.bind(on_ok=self.on_ok)

        # Criando o elemento de trabalhos
        self.load_function()
        self.days_work()

    def days_work(self):
        # Obtendo a data atual
        try:
            data_atual = datetime.today()
            data_atual = f'{data_atual.day}/{data_atual.month}/{data_atual.year}'

            data_init = datetime.strptime(data_atual, "%d/%m/%Y")
            data_ult = datetime.strptime(self.ids.data_picker.text, '%d/%m/%Y')
            days_work = data_ult - data_init
            print('Numero', days_work)
            return {'day': data_atual, 'days_work': int(days_work.days)}
        except:
            print('zero')
            return {'day': '01/03/2025', 'days_work': 0}

    def load_function(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['Abacaxicultor', 'Administrador', 'Advogado', 'Agricultor', 'Analista de Sistemas', 'Apicultor',
                  'Arquiteto', 'Artista', 'Ator', 'Auditor', 'Auxiliar de Enfermagem', 'Babá', 'Barbeiro',
                  'Bibliotecário', 'Biologista', 'Bombeiro', 'Cabeleireiro', 'Caixa', 'Camareiro', 'Carregador',
                  'Carpinteiro', 'Carteiro', 'Chefe de Cozinha', 'Cientista', 'Cozinheiro', 'Corretor de Imóveis',
                  'Costureira', 'Dançarino', 'Dentista', 'Designer', 'Detetive', 'Diarista', 'Diretor de Cinema',
                  'Eletricista', 'Empresário', 'Enfermeiro', 'Engenheiro', 'Engenheiro Agrônomo', 'Engenheiro Civil',
                  'Engenheiro de Alimentos', 'Engenheiro de Automação', 'Engenheiro de Bioprocessos',
                  'Engenheiro de Controle e Automação', 'Engenheiro de Dados', 'Engenheiro de Energia',
                  'Engenheiro de Hardware', 'Engenheiro de Machine Learning', 'Engenheiro de Manutenção',
                  'Engenheiro de Materiais', 'Engenheiro de Minas', 'Engenheiro de Petróleo', 'Engenheiro de Produção',
                  'Engenheiro de Processos', 'Engenheiro de Projetos', 'Engenheiro de Qualidade', 'Engenheiro de Redes',
                  'Engenheiro de Segurança do Trabalho', 'Engenheiro de Software', 'Engenheiro de Sistemas',
                  'Engenheiro de Telecomunicações', 'Engenheiro de Transportes', 'Engenheiro Elétrico',
                  'Engenheiro Florestal', 'Engenheiro Mecânico', 'Engenheiro Químico', 'Escritor', 'Estilista',
                  'Estudante', 'Farmacêutico', 'Ferramenteiro', 'Físico', 'Fisioterapeuta', 'Fotógrafo', 'Frentista',
                  'Garçom', 'Geólogo', 'Gerente', 'Guia Turístico', 'Heroi', 'Historiador', 'Jardineiro', 'Jornalista',
                  'Juiz', 'Lavrador', 'Locutor', 'Maçom', 'Maqueiro', 'Marceneiro', 'Marinheiro', 'Massagista',
                  'Mecânico', 'Mediador', 'Médico', 'Meteorologista', 'Motorista', 'Músico', 'Nutricionista',
                  'Oceanógrafo', 'Operador de Caixa', 'Operador de Máquinas', 'Pedagogo', 'Pedreiro',
                  'Personal Trainer', 'Pescador', 'Piloto', 'Pintor', 'Pizzaiolo', 'Policial', 'Porteiro',
                  'Professor', 'Programador', 'Psicólogo', 'Publicitário', 'Químico', 'Recepcionista',
                  'Redator', 'Repórter', 'Secretário', 'Segurança', 'Servente', 'Sociólogo', 'Tatuador',
                  'Taxista', 'Técnico de Informática', 'Técnico de Laboratório', 'Técnico de Radiologia',
                  'Técnico de Som', 'Técnico em Eletrônica', 'Técnico em Enfermagem', 'Técnico em Mecânica',
                  'Técnico em Segurança do Trabalho', 'Tradutor', 'Veterinário', 'Vigilante', 'Web Designer',
                  'Zelador', 'Zootecnista']

        menu_itens = []
        position = 0
        for state in states:
            position += 1
            row = {'text': state, 'on_release': lambda x=state: self.replace_function(x)}
            menu_itens.append(row)

        self.menu = MDDropdownMenu(
            caller=self.ids.work,
            items=menu_itens,
            position='bottom',
            width_mult=8,
            max_height='240dp',
            pos_hint={'center_x': 0.5}
        )

    def replace_function(self, text):
        self.menu.dismiss()
        self.ids.text_work.text = text

    def on_ok(self, instance_date_picker):
        try:
            instance_date_picker.dismiss()
            data_obj = instance_date_picker.get_date()[0]
            data_formatada = data_obj.strftime("%d/%m/%Y")
            self.ids.data_picker.text = data_formatada
        except:
            print('Erro ao carregar a data')

    def show_modal_date_picker(self, *args):
        """Cria e exibe um novo DatePicker toda vez que for chamado"""
        self.date_dialog.open()

    def limit_text_length(self, instance, text):
        max_length = 120
        text_field = self.ids.text_field
        if len(text_field.text) > max_length:
            text_field.text = text_field.text[:max_length]

    def show_snackbar(self) -> None:
        """Exibe um Snackbar informativo."""
        MDSnackbar(
            MDSnackbarText(
                text="Apresente novos dados para atualização",
                theme_text_color='Custom',
                text_color='black',
                bold=True
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            halign='center',
            size_hint_x=0.8,
            theme_bg_color='Custom',
            background_color='cyan'
        ).open()

    def verification_data(self):
        """ Verificando se algum dos dados foi alterado """
        if (self.ultimate != self.ids.data_picker.text
                or self.function != self.ids.text_work.text
                or float(self.salary) != float(self.ids.salary.text)
                or self.ids.text_field.text != self.observations):

            self.load_firebase()

        else:
            self.show_snackbar()

    def load_firebase(self):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Funcionarios/{self.key}/.json'
        info = self.days_work()
        print(info)
        data = {
            'function': self.ids.text_work.text,
            'ultimate': self.ids.data_picker.text,
            'observations': self.ids.text_field.text,
            'salary': float(self.ids.salary.text),
            'days_work': info['days_work'],
            'day': info['day']
        }

        UrlRequest(
            url,
            method='PATCH',
            on_success=self.success_upload,
            req_body=json.dumps(data)
        )

    def success_upload(self, instance, result):
        app = MDApp.get_running_app()
        screenmanager = app.root
        evaluation = screenmanager.get_screen('Evaluation')
        evaluation.salary = self.ids.salary.text
        day = self.days_work()
        evaluation.day = f'{day['day']}'
        evaluation.employee_function = f"{result['function']}"
        evaluation.days_work = f'{int(day['days_work'])}'
        evaluation.ultimate = f'{self.ids.data_picker.text}'
        evaluation.observations = f'{self.ids.text_field}'
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'Evaluation'

    def cancel(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Evaluation'

