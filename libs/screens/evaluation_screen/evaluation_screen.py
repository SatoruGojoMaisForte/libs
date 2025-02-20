from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen


class EvaluationScreen(MDScreen):
    employee_name = 'Welber'
    employee_function = 'Pedreiro'
    avatar = 'https://res.cloudinary.com/dsmgwupky/image/upload/v1738458050/KingHades.jpg'
    contractor = 'Solitude'
    method_salary = StringProperty()
    salary = StringProperty()
    assess = '8.4'
    coexistence = '1'
    punctuality = '1'
    efficiency = '5'
    scale = StringProperty()
    days_work = 6

    def on_enter(self, *args):
        self.ids.perfil.source = self.avatar
        self.ids.name.text = self.employee_name
        self.ids.function.text = self.employee_function
        if self.method_salary in 'Diaria':
            self.calculate_day()
            return

        if self.method_salary in 'Semanal':
            self.calculate_week()
            return

        if self.method_salary in 'Quinzenal':
            self.calculate_biweekly()
            return

        if self.method_salary in 'Mensal':
            self.calculate_month()
            return

        if self.method_salary in 'Empreita':
            self.calculate_undertakes()
            return
        self.components()

    def calculate_day(self):
        if self.scale in '6x1':
            percentage = (self.days_work / 6) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            salary = int(self.salary) * self.days_work
            print(salary)
            self.ids.value_salary.text = 'R${:,}'.format(salary)

        elif self.scale in '5x2':
            percentage = (self.days_work / 5) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            salary = int(self.salary) * self.days_work
            print(salary)
            self.ids.value_salary.text = 'R${:,}'.format(salary)

        elif self.scale in '4x3':
            percentage = (self.days_work / 4) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            salary = int(self.salary) * self.days_work
            print(salary)
            self.ids.value_salary.text = 'R${:,}'.format(salary)

    def calculate_week(self):
        if self.scale in '6x1':
            percentage = (self.days_work / 6) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 6

            self.ids.value_salary.text = 'R${:,}'.format(day * self.days_work)

        if self.scale in '5x2':
            percentage = (self.days_work / 5) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 5

            self.ids.value_salary.text = 'R${:,}'.format(day * self.days_work)

        if self.scale in '4x3':
            percentage = (self.days_work / 4) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 4
            self.ids.value_salary.text = 'R${:,}'.format(day * self.days_work)

    def calculate_biweekly(self):
        if self.scale in '6x1':
            percentage = (self.days_work / 12) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 13
            self.ids.value_salary.text = 'R${:,.2f}'.format(day * self.days_work)

        if self.scale in '5x2':
            percentage = (self.days_work / 10) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 13
            self.ids.value_salary.text = 'R${:,.2f}'.format(day * self.days_work)

        if self.scale in '4x3':
            percentage = (self.days_work / 8) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 8
            self.ids.value_salary.text = 'R${:,.2f}'.format(day * self.days_work)

    def calculate_month(self):
        if self.scale in '6x1':
            percentage = (self.days_work / 26) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 26
            self.ids.value_salary.text = 'R${:,.2f}'.format(day * self.days_work)

        if self.scale in '5x2':
            percentage = (self.days_work / 22) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 22
            self.ids.value_salary.text = 'R${:,.2f}'.format(day * self.days_work)

        if self.scale in '4x3':
            percentage = (self.days_work / 17) * 100
            self.ids.percentage.text = '{:.2f}%'.format(percentage)
            day = int(self.salary) / 17
            self.ids.value_salary.text = 'R${:,.2f}'.format(day * self.days_work)

    def calculate_undertakes(self):
        self.ids.frequency.text = 'Prazo'
        self.ids.percentage.text = f'{self.days_work}'

    def components(self):
        # Convivencia ----------------------------------------------
        if not self.coexistence:
            self.ids.coexistence.text_color = 'red'
            self.ids.text_coexistence.text = 'Não definido'
        else:
            numb = int(self.coexistence)

            if numb == 1:
                self.ids.text_coexistence.text_color = get_color_from_hex('#FF0000')
                self.ids.text_coexistence.text = f'Conflituoso(a)'

            elif numb == 2:
                self.ids.text_coexistence.text_color = get_color_from_hex('#E06666')
                self.ids.text_coexistence.text = f' Tolerável(a)'

            elif numb == 3:
                self.ids.text_coexistence.text_color = get_color_from_hex("#808080")
                self.ids.text_coexistence.text = 'Neutro(a)'

            elif numb == 4:
                self.ids.text_coexistence.text_color = get_color_from_hex("#008000")
                self.ids.text_coexistence.text = 'Colaborativa (a)'

            elif numb == 5:
                self.ids.text_coexistence.text_color = get_color_from_hex("#0044CC")
                self.ids.text_coexistence.text = 'Excelente(a)'

        # Eficiencia

        if not self.efficiency:
            self.ids.efficiency.text_color = 'red'
            self.ids.text_efficiency.text = 'Não definido'

        else:
            numb = int(self.efficiency)

            if numb == 1:
                self.ids.text_efficiency.text_color = get_color_from_hex('#FF0000')
                self.ids.text_efficiency.text = f'Ineficiente(a)'

            elif numb == 2:
                self.ids.text_efficiency.text_color = get_color_from_hex('#E06666')
                self.ids.text_efficiency.text = f'Baixa Eficiência(a)'

            elif numb == 3:
                self.ids.text_efficiency.text_color = get_color_from_hex("#808080")
                self.ids.text_efficiency.text = 'Razoável(a)'

            elif numb == 4:
                self.ids.text_efficiency.text_color = get_color_from_hex("#008000")
                self.ids.text_efficiency.text = 'Eficiente(a)'

            elif numb == 5:
                self.ids.text_efficiency.text_color = get_color_from_hex("#0044CC")
                self.ids.text_efficiency.text = 'Altamente Eficiente(a)'

        # salario ---------------------------------------------------------------
        if not self.salary:
            self.ids.salary.text_color = 'red'
            self.ids.text_salary.text = 'Não definido'

        else:
            #self.ids.salary.text_color = 'green'
            self.ids.text_salary.text = '{}: R$ {:,}'.format(self.method_salary, int(self.salary))

        # Pontualidade ------------------------------------------------------------
        if not self.punctuality:
            self.ids.punctuality.text_color = 'red'
            self.ids.text_punctuality.text = 'Não definido'

        else:
            numb = int(self.punctuality)

            if numb == 1:
                self.ids.text_punctuality.text_color = get_color_from_hex('#FF0000')
                self.ids.text_punctuality.text = f'Muito Atrasado(a)'

            elif numb == 2:
                self.ids.text_punctuality.text_color = get_color_from_hex('#E06666')
                self.ids.text_punctuality.text = f'Frequentemente Atrasado(a)'

            elif numb == 3:
                self.ids.text_punctuality.text_color = get_color_from_hex("#808080")
                self.ids.text_punctuality.text = 'Pontualidade Regular(a)'

            elif numb == 4:
                self.ids.text_punctuality.text_color = get_color_from_hex("#008000")
                self.ids.text_punctuality.text = 'Pontual(a)'

            elif numb == 5:
                self.ids.text_punctuality.text_color = get_color_from_hex("#0044CC")
                self.ids.text_punctuality.text = 'Sempre Pontual/Adiantado(a)'

    def back_table(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Table'
