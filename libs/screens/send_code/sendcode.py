import json
import os
import re
import threading
from urllib.parse import urlencode
import string
import random
import pandas as pd
import bcrypt
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from flask_mail import Mail, Message
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from dotenv import load_dotenv
from flask import Flask
from time import sleep
load_dotenv()



class SendCode(MDScreen):
    cont_email = 0  # Contador para tentativas de verificação de e-mail
    cont_envio = 0  # Contador para tentativas de envio de código

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.code = None

    def on_enter(self, *args):
        self.code = ''
        # Definindo o ícone de erro para as telas
        icone_erro = MDIconButton(
            icon='alert-circle',
            theme_font_size='Custom',
            font_size='55sp',
            theme_icon_color='Custom',
            pos_hint={'center_x': .5, 'center_y': .6},
            icon_color='red'  # Cor vermelha para representar o erro
        )
        self.ids['error'] = icone_erro

        # Definindo o ícone de acerto para as telas
        icone_acerto = MDIconButton(
            icon='check',
            theme_font_size='Custom',
            font_size='50sp',
            theme_icon_color='Custom',
            pos_hint={'center_x': .5, 'center_y': .6},
            icon_color='green'  # Cor verde para representar o acerto
        )
        self.ids['acerto'] = icone_acerto

        # Definindo o MDCard onde vai ficar todo o corpo do layout
        self.card = MDCard(
            id='carregando',
            style='elevated',
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            md_bg_color=(1, 1, 1, 1),
            theme_bg_color="Custom",
            theme_shadow_offset="Custom",
            shadow_offset=(1, -2),
            theme_shadow_softness="Custom",
            shadow_softness=1,
            theme_elevation_level="Custom",
            elevation_level=2
        )
        self.ids['card'] = self.card

        # Definindo o RelativeLayout onde todo o corpo será posicionado
        relative = MDRelativeLayout()
        self.ids['relative'] = relative

        # Definindo o CircularProgressIndicator onde o usuário vai ter o carregamento visual
        circle = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['progress'] = circle

        # Definindo o Label com texto carregando onde o usuário vai ter o indicador visual
        label = MDLabel(
            text='Carregando...',
            font_style='Title',
            halign='center',
            bold=True,
            text_color='black',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.ids['texto_carregando'] = label
        relative.add_widget(circle)
        relative.add_widget(label)
        self.card.add_widget(relative)

    def set_email(self):
        self.verificar_email = self.ids.verificar_email.text

    def chama_login(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Login'

    def is_email_valid(self, text: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, text) is not None

    def email_existir(self, email):
        if not self.is_email_valid(email):
            self.remove_widget(self.card)
            self.ids.erro_email.text = 'Formato de email inválido'
            self.ids.erro_email.text_color = 'red'
            return

        nome = self.ids.verificar_email.text
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios.json'
        parametros = {
            "rules": {
                "Usuarios": {
                    ".indexOn": ["email"],
                    ".read": "auth != null",
                    ".write": "auth != null"
                }
            }
        }

        # Converte os parâmetros para query string
        query_string = urlencode(parametros)

        # Realiza a requisição GET com UrlRequest
        UrlRequest(
            f'{url}?{query_string}',
            on_success=self.existir,
            method='GET',
        )

    def existir(self, req, result):
        if result:
            for usuario_id, usuario_data in result.items():
                if usuario_data.get('email') == self.ids.verificar_email.text:
                    self.ids.erros.text = ''
                    self.ids.verificar_email.error = False
                    self.patch(result)
                    return

        self.ids.erros.text = 'Email não cadastrado'
        self.ids.erros.text_color = 'red'
        self.ids.verificar_email.error = True
        self.remove_widget(self.card)
        print('email não cadastrado')

    def criar(self):
        # criando um codigo
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choices(caracteres, k=6))

    def patch(self, result):
        import pandas as pd

        print('Adicionando o código criptografado')
        codigo_aleatorio = self.criar()
        self.code = codigo_aleatorio
        usuarios = result
        mail = self.ids.verificar_email.text
        # Converte o dicionário em um DataFrame, onde as chaves do dicionário são o índice
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'

        df = pd.DataFrame.from_dict(usuarios, orient='index')
        indices = df.index[df['email'] == mail].tolist()
        hashed_code = codigo_aleatorio.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_code = bcrypt.hashpw(password=hashed_code, salt=salt).decode(
            'utf-8')
        dados = {'verification_code': hashed_code}

        if indices:
            print('fazendo a requisição')
            self.ids.erros.text = ''
            self.ids.verificar_email.error = False
            UrlRequest(
                url=f'{url}/{indices[0]}.json',
                req_body=json.dumps(dados),
                on_success=self.codigo_alterado,
                req_headers={'Content-Type': 'application/json'},
                method='PATCH'
            )
        else:
            self.remove_widget(self.card)
            self.ids.erros.text = 'Email não cadastrado'
            self.ids.verificar_email.error = True

    def codigo_alterado(self, req, result):
        self.enviar_codigo_verification()

    def enviar_codigo_verification(self):
        app = Flask(__name__)
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD_APP')
        mail = Mail(app)
        print('Enviando codigo')
        html_content = f"""
                <!DOCTYPE html>
                <html lang="pt-br">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Código de Verificação</title>
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
                        body {{
                            margin: 0;
                            padding: 0;
                            background: #fafafa;
                            font-family: 'Montserrat', sans-serif;
                        }}
                        .container {{
                            max-width: 500px;
                            margin: 50px auto;
                            background: #ffffff;
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }}
                        .header {{
                            font-size: 24px;
                            font-weight: 700;
                            margin-bottom: 20px;
                            color: #262626;
                        }}
                        .content {{
                            font-size: 16px;
                            color: #595959;
                            line-height: 1.6;
                        }}
                        .code {{
                            display: inline-block;
                            margin: 20px 0;
                            padding: 10px 20px;
                            background: #f8f9fa;
                            border: 1px solid #e0e0e0;
                            border-radius: 5px;
                            font-weight: 700;
                            font-size: 20px;
                            color: #333;
                        }}
                        .footer {{
                            margin-top: 30px;
                            font-size: 12px;
                            color: #999999;
                        }}
                        .important {{
                            color: #d9534f;
                            font-weight: 700;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">CHATTO</div>
                        <div class="content">
                            <p>Código de verificação:</p>
                            <div class="code">{self.code}</div>
                            <p>Olá, <strong>{self.code} é seu código de verificação</strong>.</p>
                            <p>Insira o código acima na tela de verificação do seu aplicativo para entrar na sua conta. Este código irá expirar em 20 minutos.</p>
                            <p class="important">IMPORTANTE: Não compartilhe seus códigos de segurança com ninguém. <strong>O Chatto</strong> nunca pedirá seus códigos. Isso inclui mensagens de texto, compartilhamento de tela, etc. Ao compartilhar seus códigos de segurança com outra pessoa, você está colocando sua conta e seu conteúdo em risco.</p>
                            <p>Atenciosamente,<br>A equipe do <strong>Chatto</strong></p>
                        </div>
                        <div class="footer">© 2024 Chatto. Todos os direitos reservados.</div>
                    </div>
                </body>
                </html>
                """

        # Criar o contexto da aplicação Flask temporário
        with app.app_context():
            msg = Message(
                "Password Reset Verification Code",
                sender=os.getenv('MAIL_USERNAME'),
                recipients=[self.ids.verificar_email.text]
            )
            msg.html = html_content
            thread = threading.Thread(target=self.enviar_email, args=(mail, msg, app))
            thread.start()
            self.ultima_etapa()

    def enviar_email(self, mail, msg, app):

        with app.app_context():
            mail.send(msg)

    def error(self, req, error):
        print(error)

    def ultima_etapa(self):
        progress = self.ids['progress']
        icon_acerto = self.ids['acerto']
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_acerto)
        self.ids.texto_carregando.text = 'Verificação enviada'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
        sleep(2)
        self.remove_widget(self.card)
        self.chamar_pagina()

    def chamar_pagina(self):
        check = self.manager.get_screen('Check')
        check.email = self.ids.verificar_email.text
        self.manager.current = 'Check'

    def enviar_codigo(self):
        texto = self.ids.verificar_email.text

        if texto:
            if self.is_email_valid(texto):
                self.ids.verificar_email.error = False
                self.ids.erros.text = ''
                self.add_widget(self.card)
                self.cont_email = 0  # Reseta o contador ao iniciar a verificação
                self.email_existir(texto)
            else:
                self.remove_widget(self.card)
                self.ids.erros.text = 'O formato do email é inválido'
                self.ids.verificar_email.error = True
        else:
            self.ids.verificar_email.focus = True
