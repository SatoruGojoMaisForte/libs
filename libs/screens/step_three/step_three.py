import json

from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class StepThree(MDScreen):
    contratante = 'Barba voss'
    nome = 'wELBER'
    cpf = '09713890124'
    pix = 'welber@gmail.com'
    contratado = '25/11/2024'
    idade = '26'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.funcionario = None

    def ajustar(self, instance, text):
        if self.ids.habilidades.error:
            self.ids.habilidades.text = self.ids.habilidades.text[0: 150]

    def etapa1(self):
        if self.ids.habilidades.text == '':
            self.ids.habilidades.focus = True
        else:
            self.ids.habilidades.focus = False
            if self.ids.cargo.text == '':
                self.ids.cargo.focus = True
            else:
                self.avançar()
    def page_return(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'StepTwo'

    def avançar(self):
        self.manager.transition = SlideTransition(direction='left')
        step = self.manager.get_screen('StepFour')
        step.contratante = self.contratante
        step.nome = self.nome
        step.cpf = self.cpf
        step.pix = self.pix
        step.contratado = self.contratado
        step.idade = self.idade
        step.competencias = self.ids.habilidades.text
        step.cargo = self.ids.cargo.text
        self.manager.current = 'StepFour'
