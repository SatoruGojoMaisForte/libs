import json
import re
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen


class EditProfile(MDScreen):
    telefone = '62993683473'
    email = 'viitiinmec@gmail.com'
    company = 'rjporcelanatoliquido'
    name_user = 'Welber'

    def on_enter(self, *args):
        self.ids.name_user.text = self.name_user
        self.ids.telefone.text = self.telefone
        self.ids.email.text = self.email
        self.ids.company.text = self.company

    def is_email_valid(self, text: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, text) is not None

    def on_text(self, instance, text):
        email_valid = self.is_email_valid(text)
        if email_valid:
            self.ids.erro2.text = ''
            self.ids.correct2.icon_color = 'green'
            self.ids.correct2.icon = 'check'

        else:
            self.ids.erro2.text = 'Formato invalido!!'
            self.ids.correct2.icon_color = 'red'
            self.ids.correct2.icon = 'alert'

    def on_text_two(self, instance, numero):
        # Remove tudo que não for número
        numero = re.sub(r'\D', '', numero)

        if len(numero) == 11:  # Número com código do país
            self.ids.telefone.text = f"({numero[0:2]}) {numero[2:7]}-{numero[7:]}"
            self.ids.erro1.text = ""
            self.ids.erro1.text = ""
            self.ids.correct1.icon_color = 'green'
            self.ids.correct1.icon = 'check'
        else:
            self.ids.erro1.text = "Número inválido"
            self.ids.correct1.icon_color = 'red'
            self.ids.correct1.icon = 'alert'

    def on_text_three(self, instance, company):
        if company != '':
            self.ids.correct3.icon_color = 'green'
            self.ids.correct3.icon = 'check'

    def on_text_four(self, instance, name):
        if name != '':
            self.ids.erro4.text = ''
            self.ids.correct4.icon_color = 'green'
            self.ids.correct4.icon = 'check'
        else:
            self.ids.erro4.text = 'Campo obrigatorio'
            self.ids.correct4.icon_color = 'red'
            self.ids.correct4.icon = 'alert'

    def step_one(self):
        """Verificar se algum dos campos não estão corretos"""
        print('test')
        if self.ids.telefone.text in '':
            self.ids.telefone.focus = True
            return

        if self.ids.email.text in '':
            self.ids.email.focus = True
            return

        if self.ids.name_user.text in '':
            self.ids.name_user.focus = True
            return

        if self.ids.erro1.text != '':
            self.ids.telefone.focus = True
            return

        if self.ids.erro2.text != '':
            self.ids.email.focus = True
            return

        if self.ids.erro4.text != '':
            self.ids.name_user.focus = True
            return

        self.update_database()

    def update_database(self):
        ''' Agora vamos puxar os dados do firebase'''

        url = 'https://obra-7ebd9-default-rtdb.firebaseio.com/Users'
        UrlRequest(
            url=f'{url}/.json',
            on_success=self.update_database_2,

        )

    def update_database_2(self, req, users):
        for key, value in users.items():

            if value['name'] == self.name_user:
                self.update_database_3(key)

    def update_database_3(self, key):
        url = f'https://obra-7ebd9-default-rtdb.firebaseio.com/Users/{key}'
        data = {'name': self.ids.name_user.text,
                'telefone': self.ids.telefone.text,
                'email': self.ids.email.text,
                'company': self.ids.company.text
                }

        UrlRequest(
            f'{url}/.json',
            method='PATCH',
            req_body=json.dumps(data),
            on_success=self.database_sucess
        )

    def database_sucess(self, req, result):
        print(result)

    def login(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Perfil'
