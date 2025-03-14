from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen


class AddEmployee(MDScreen):
    contractor = StringProperty()

    def on_enter(self):
        self.load_salary()
        self.load_function()
        self.load_scale()

    def load_salary(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['Diaria', 'Semanal', 'Quinzenal', 'Mensal', 'Empreita']

        menu_itens = []
        position = 0
        for state in states:
            position += 1
            row = {'text': state, 'on_release': lambda x=state: self.replace_salary(x)}
            menu_itens.append(row)

        self.menu = MDDropdownMenu(
            caller=self.ids.card_salary,
            items=menu_itens,
            position='bottom',
            width_mult=5,
            max_height='400dp',
            pos_hint={'center_x': 0.5}
        )

    def load_scale(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['6x1', '5x2', '4x3']

        menu_itens = []
        position = 0
        for state in states:
            position += 1
            row = {'text': state, 'on_release': lambda x=state: self.replace_scale(x)}
            menu_itens.append(row)

        self.menu_scale = MDDropdownMenu(
            caller=self.ids.card_scale,
            items=menu_itens,
            position='bottom',
            width_mult=5,
            max_height='400dp',
            pos_hint={'center_x': 0.5}
        )

    def replace_scale(self, text):
        self.ids.scale.text = text
        self.ids.scale.text_color = 'green'
        self.menu_scale.dismiss()

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

        self.menu2 = MDDropdownMenu(
            caller=self.ids.card_function,
            items=menu_itens,
            position='bottom',
            width_mult=2,
            max_height='200dp',
            pos_hint={'center_x': 0.5}
        )

    def replace_function(self, text):
        self.ids.function.text = text
        self.ids.function.text_color = 'green'
        self.menu2.dismiss()

    def replace_salary(self, texto):
        self.ids.salary.text = texto
        self.ids.salary.text_color = 'green'
        self.menu.dismiss()

    def table_screen(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Table'

    def checking_empty_fields(self):
        if self.ids.name.text == '':
            self.ids.name.focus = True
            return

        if not self.ids.value_salary.text:
            self.ids.value_salary.focus = True
            return

        if self.ids.salary.text in ('Ausente', 'Obrigatorio'):
            self.ids.salary.text = 'Obrigatorio'
            self.ids.salary.text_color = 'red'
            self.menu.open()
            return

        if self.ids.function.text in ('Ausente', 'Obrigatorio'):
            self.ids.function.text = 'Obrigatorio'
            self.ids.function.text_color = 'red'
            self.menu2.open()
            return

        if self.ids.scale.text in ('Ausente', 'Obrigatorio'):
            self.ids.scale.text = 'Obrigatorio'
            self.ids.scale.text_color = 'red'
            self.menu_scale.open()
            return

        self.avatar_employee()

    def avatar_employee(self):
        self.manager.transition = SlideTransition(direction='left')
        app = MDApp.get_running_app()
        screen_manager = app.root
        employee_avatar = screen_manager.get_screen('EmployeeAvatar')
        employee_avatar.name_employee = self.ids.name.text
        employee_avatar.function = self.ids.function.text
        employee_avatar.salary = self.ids.value_salary.text
        employee_avatar.contractor = self.contractor
        employee_avatar.method_salary = self.ids.salary.text
        employee_avatar.scale = self.ids.scale.text
        self.ids.name.text = ''
        self.ids.function.text = 'Ausente'
        self.ids.function.text_color = 'red'
        self.ids.salary.text = 'Ausente'
        self.ids.salary.text_color = 'red'
        screen_manager.current = 'EmployeeAvatar'

    def back_table(self):
        self.ids.salary.text = 'Ausente'
        self.ids.salary.text_color = 'red'
        self.ids.function.text = 'Ausente'
        self.ids.function.text_color = 'red'
        self.ids.name.text = ''
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Table'
