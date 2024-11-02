import json
import queue
import threading
from time import sleep

import bcrypt
import pandas as pd
import requests
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from dotenv import load_dotenv
import os

class TrocarSenha(MDScreen):
    email = StringProperty()

    def on_enter(self, *args):
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
        icone_acerto = AsyncImage(
            source='https://res.cloudinary.com/dsmgwupky/image/upload/v1730504140/image_yvn8lp.png',
            size_hint=(None, None),
            size=("80dp", "150dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            allow_stretch=True
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
        from kivymd.uix.label import MDLabel
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
        self.nome()

    def nome(self):
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'
        UrlRequest(
            f'{url}.json',
            method='GET',
            on_success=self.etapa1
        )

    def etapa1(self, req, result):
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'
        usuarios = result

        # criando um dataframe com os usuarios
        df = pd.DataFrame.from_dict(usuarios, orient='index')

        # pegando codigo com index
        indices = df.index[df['email'] == self.email].tolist()

        #
        UrlRequest(
            url=f'{url}/{indices[0]}.json',
            method='GET',
            on_success=self.etapa2
        )

    def etapa2(self, req, result):
        usuario = result
        self.ids.usuario.text = f'{usuario['name']} - Chatto'

    def modificar(self, campo):
        if campo == 'confirmar':
            text = self.ids.confirmar.text
            text = str(text).replace(' ', '')
            text = str(text).replace(':', '')
            text = str(text).replace(';', '')
            self.ids.confirmar.text =  text

        else:
            text = self.ids.senha.text
            text = str(text).replace(' ', '')
            text = str(text).replace(':', '')
            text = str(text).replace(';', '')
            self.ids.senha.text = text


    def visibilizar_senha1(self):
        visivel = self.ids.senha.password
        if visivel:
            self.ids.senha.password = False
            self.ids.confirmar.password = False
        else:
            self.ids.senha.password = True
            self.ids.confirmar.password = True


    def alterar_senha(self):
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'
        UrlRequest(
            f'{url}.json',
            method='GET',
            on_success=self.senha_etapa1
        )

    def senha_etapa1(self, req, result):
        usuarios = result
        url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios'

        df = pd.DataFrame.from_dict(usuarios, orient='index')
        indices = df.index[df['email'] == self.email].tolist()

        hashed_code = self.ids.confirmar.text.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_code = bcrypt.hashpw(password=hashed_code, salt=salt).decode('utf-8')

        dados = {'password': hashed_code}
        if indices:
            UrlRequest(
                url=f'{url}/{indices[0]}.json',
                req_body=json.dumps(dados),
                on_success=self.senha_alterada,
                req_headers={'Content-Type': 'application/json'},
                method='PATCH'
            )

    def senha_alterada(self, req, result):
        progress = self.ids['progress']
        icon_acerto = self.ids['acerto']
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_acerto)
        self.ids.texto_carregando.text = 'Senha alterada'
        self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
        self.login()

    def login(self):
        self.manager.current = 'Login'

    def requisitos(self):
        texto_confirmar = self.ids.confirmar.text
        texto_senha = self.ids.senha.text
        if texto_senha == '':
            self.ids.senha.focus = True
            return
        elif texto_confirmar == '':
            self.ids.confirmar.focus = True
            return
        if texto_senha == texto_confirmar:
            if len(texto_senha) >= 6:
                self.add_widget(self.card)
                self.alterar_senha()
                self.ids.hint.text = 'Confirmar nova palavra-passe'
                return
            else:
                self.ids.erro.text = 'Minimo de 6 caracteres'
        else:
            self.ids.erro.text = 'As senhas devem ser iguais'
            return

