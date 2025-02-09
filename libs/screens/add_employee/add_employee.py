from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen


class AddEmployee(MDScreen):
    def on_enter(self):
        self.load_salary()
        self.load_function()

    def load_salary(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['Salario minimo', 'entre 1.518 e 2000', 'entre 2000 é 3000', 'entre 3000 e 4000', 'entre 5000 e 6000']

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
            max_height='400dp'
        )

    def load_function(self):
        # Abrir um popup de menu para a pessoa escolher o seu estado
        states = ['Servente', 'Pedreiro', 'Engenheiro', 'Advogado', 'Professor']

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
            width_mult=5,
            max_height='400dp'
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

        if self.ids.name.text == '':
            self.ids.name.focus = True
            return

        self.avatar_employee()

    def avatar_employee(self):
        self.manager.transition = SlideTransition(direction='left')
        app = MDApp.get_running_app()
        screen_manager = app.root
        employee_avatar = screen_manager.get_screen('EmployeeAvatar')
        employee_avatar.name_employee = self.ids.name.text
        employee_avatar.function = self.ids.function.text
        employee_avatar.salary = self.ids.salary.text
        screen_manager.current = 'EmployeeAvatar'

    def back_table(self):
        self.ids.salary.text = 'Ausente'
        self.ids.salary.text_color = 'red'
        self.ids.function.text = 'Ausente'
        self.ids.function.text_color = 'red'
        self.ids.name.text = ''
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Table'
