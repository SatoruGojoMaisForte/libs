from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDockedDatePicker, MDModalDatePicker, MDModalInputDatePicker
from kivymd.uix.screen import MDScreen


class StepTwo(MDScreen):
    contratante = StringProperty()
    nome = StringProperty()
    cpf = StringProperty()

    def on_enter(self, *args):
        print(self.nome, self.cpf)

    def open_menu(self, item):
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in range(15, 82)
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def menu_callback(self, text_item):
        self.ids.drop_text.text = text_item
        print(text_item)

    def show_modal_input_date_picker(self, *args):
        def on_edit(*args):
            date_dialog.dismiss()
            Clock.schedule_once(self.show_modal_date_picker, 0.2)

        date_dialog = MDModalInputDatePicker()
        date_dialog.bind(on_edit=on_edit)
        date_dialog.open()

    def on_edit(self, instance_date_picker):
        instance_date_picker.dismiss()
        Clock.schedule_once(self.show_modal_input_date_picker, 0.2)

    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()

    def on_select_day(self, instance_date_picker, number_day):
        self.ids.contratar.text = str(instance_date_picker.get_date()[0])

    def on_select_month(self, instance_date_picker, number_month):
        self.ids.contratar.text = str(instance_date_picker.get_date()[0])

    def on_select_year(self, instance_date_picker, number_year):
        self.ids.contratar.text = str(instance_date_picker.get_date()[0])

    def on_ok(self, instance_date_picker):
        print(instance_date_picker.get_date()[0])
        instance_date_picker.dismiss()
        self.date = instance_date_picker

    def show_modal_date_picker(self, *args):
        date_dialog = MDDockedDatePicker()
        date_dialog.bind(on_edit=self.on_edit)
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.bind(on_select_day=self.on_select_day)
        date_dialog.bind(on_select_month=self.on_select_month)
        date_dialog.bind(on_select_year=self.on_select_year)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.open()

    def page_return(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'SignUp'

    def verificar(self):
        if self.ids.pix.text == '':
            self.ids.pix.focus = True
        else:
            self.ids.pix.focus = False
            if self.ids.contratar.text != 'Selecionar':
                print(self.ids.drop_text.text)
                self.ids.drop_text.text_color = 'black'

                if self.ids.drop_text.text != 'Idade' and self.ids.drop_text != 'Obrigatoria':
                    self.ids.drop_text.text_color = 'black'
                    self.avançar()

                else:
                    self.ids.drop_text.text = 'Obrigatoria'
                    self.ids.drop_text.text_color = 'red'

            else:
                self.ids.contratar.text = 'Data obrigatoria'
                self.ids.contratar.text_color = 'red'

    def avançar(self):
        self.manager.transition = SlideTransition(direction='left')
        step = self.manager.get_screen('StepThree')
        step.contratante = self.contratante
        step.nome = self.nome
        step.cpf = self.cpf
        step.pix = self.ids.pix.text
        step.contratado = self.ids.contratar.text
        step.idade = self.ids.drop_text.text
        self.manager.current = 'StepThree'
