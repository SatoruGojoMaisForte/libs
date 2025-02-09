import re
from time import sleep

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.behaviors import CommonElevationBehavior, CircularRippleBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.pickers import MDModalInputDatePicker, MDModalDatePicker, MDDockedDatePicker
from kivymd.uix.screen import MDScreen
import re


class SignUp(MDScreen):
    avatar = 'https://res.cloudinary.com/dsmgwupky/image/upload/v1732038646/image_5_jewnww.png'

    def text_cpf(self, instance, value):
        # Lógica para lidar com o texto digitado
        for x in value:
            if x in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                self.ids.erro_cpf.text = 'O formato do cpf e invalido'
                self.ids.cpf.error = True
                return
            else:
                self.ids.erro_cpf.text = ''
                self.ids.cpf.error = False
        print(f"Texto digitado: {value}")
        max_length = 11  # O CPF tem 11 dígitos

        # Remove espaços, pontos e traços
        text = str(value).replace(' ', '').replace('.', '').replace('-', '')

        # Limita o número de caracteres a 11
        if len(text) > max_length:
            text = text[:max_length]

        # Formata o texto no padrão de CPF: XXX.XXX.XXX-XX usando regex
        formatted_text = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', text)

        # Atribui o texto formatado ao campo
        self.ids.cpf.text = formatted_text

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

    def on_select_day(self, instance_date_picker, number_day):
        print(number_day)

    def on_select_month(self, instance_date_picker, number_month):
        print(number_month)

    def on_select_year(self, instance_date_picker, number_year):
        print(number_year)

    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()
        print('close')

    def on_ok(self, instance_date_picker):
        print(instance_date_picker.get_date()[0])
        self.ids.date.text = str(instance_date_picker.get_date()[0])
        instance_date_picker.dismiss()

    def show_modal_date_picke(self, *args):
        date_dialog = MDModalDatePicker(min_year=1950)
        date_dialog.bind(on_edit=self.on_edit)
        date_dialog.bind(on_select_day=self.on_select_day)
        date_dialog.bind(on_select_month=self.on_select_month)
        date_dialog.bind(on_select_year=self.on_select_year)
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.open()

    def adicionado(self, req, result):
        print(result)

    def filled(self):
        if self.ids.card.style == 'outlined':
            self.ids.card.style = 'elevated'
            self.ids.card.shadow_color = 'blue'
        else:
            self.ids.card.style = 'outlined'

    def verificar(self):
        if self.ids.nome.text == '':
            self.ids.nome.focus = True
            return
        else:
            self.ids.nome.focus = False

            if self.ids.cpf.text == '':
                self.ids.cpf.focus = True
                return

            else:
                self.ids.cpf.focus = False
                self.manager.transition = SlideTransition(direction='left')
                login = self.manager.get_screen('StepTwo')
                login.nome = self.ids.nome.text
                login.cpf = str(self.ids.cpf.text)
                login.contratante = 'Adrian'
                self.manager.current = 'StepTwo'

    def page_return(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Perfil'

