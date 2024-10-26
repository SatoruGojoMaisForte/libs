import queue

import requests
from PIL.ImageDraw import ImageDraw
from kivy.properties import StringProperty, NumericProperty, Clock, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
import os
import json
from kivymd.uix.button import MDButtonText
import sys
from kivy.metrics import dp
import socketio
import threading
from kivymd.uix.card import MDCard
from plyer import filechooser
from PIL import Image
from KivyMD.kivymd.uix.boxlayout import MDBoxLayout
from KivyMD.kivymd.uix.label import MDLabel
from kivy.graphics import RoundedRectangle, Color
from kivymd.uix.textfield import MDTextFieldHintText

from KivyMD.kivymd.uix.relativelayout import MDRelativeLayout
from KivyMD.kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText, MDSnackbarCloseButton, \
    MDSnackbarButtonContainer
from KivyMD.kivymd.uix.textfield import MDTextField
from dotenv import load_dotenv
load_dotenv()

# Classes para o navigation app bar ------------------------------------------------------------------------------------
class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen(MDScreen):
    pass


id = os.getenv('ID')
# Classes para mensagens -----------------------------------------------------------------------------------------------
class Eu(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 17
    image_source = StringProperty()
    def color_eu(self):
        return get_color_from_hex("#82f2fa")


class Ele(MDBoxLayout):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 17
    image_source = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.ajustar_padding)

    def ajustar_padding(self, *args):
        # Acessa o MDLabel para calcular a altura
        label = self.ids.label
        altura_texto = label.texture_size[1]
        # Ajusta o padding com base na altura do texto
        if altura_texto <= dp(40):  # Aproximadamente 1 ou 2 linhas
            novo_padding = [12, 8]
        else:
            novo_padding = [12, 18]

        print(f"Ajustando padding: {novo_padding}")
        self.padding = novo_padding
        self.ids.box.canvas.ask_update()
        self.canvas.ask_update()


# Classe para realizar as mensagens entre as seções --------------------------------------------------------------------
class WebSocketClient:
    def __init__(self, app, name):
        self.web = socketio.Client()
        sio_thread = threading.Thread(target=self.conect)
        sio_thread.start()
        self.kivyapp = app
        self.textfield = ''
        self.name = name
        self.id = 4
        self.web.on('message', self.receber_mensagem)

    def conect(self):
        self.web.connect('http://localhost:5000')
        print("Conectado ao servidor")
        self.web.wait()

    def enviar_mensagem(self, message):
        data = {
            'message': message,
            'username': str(self.id)
        }
        self.web.emit('message', data)

    def image(self, nome):
        url = f'https://api-imagem.onrender.com/get-imagem?name={nome}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['message']

    def carregar_mensagens(self):
        carregar = threading.Thread(target=self.carregar_mensagen)
        carregar.start()

    def carregar_mensagen(self):
        response = requests.get('http://localhost:5000/carregar-mensagens')
        if response.status_code == 200:
            messages = response.json()

            for msg in messages:
                self.receber_mensagem(msg)

    def receber_mensagem(self, data):
        def atualizar_chat(*args):
            size = 0
            halign = ''
            username = data.get('username')
            message_text = data.get('message')
            print(username, message_text)
            if username == str(self.id):
                caracteres = len(message_text)
                if caracteres < 3:
                    size = .15
                    halign = 'center'
                elif caracteres < 6:
                    size = .18
                    halign = 'center'
                    print('stop 2')
                elif caracteres < 9:
                    size = .24
                    halign = 'center'
                    print('stop 3')
                elif caracteres < 12:
                    size = .28
                    halign = 'center'
                    print('stop 4')
                elif caracteres < 15:
                    size = .33
                    halign = 'center'
                elif caracteres < 18:
                    size = .38
                    halign = 'center'
                elif caracteres < 21:
                    size = .44
                    halign = 'center'
                elif caracteres < 24:
                    size = .49
                    halign = 'center'
                elif caracteres < 27:
                    size = .55
                    halign = 'center'
                elif caracteres < 30:
                    size = .60
                    halign = 'center'
                elif caracteres < 33:
                    size = .60
                    halign = 'center'
                elif caracteres < 36:
                    size = .65
                    halign = 'center'
                elif caracteres < 39:
                    size = .70
                    halign = 'left'
                elif caracteres < 42:
                    size = .75
                    halign = 'left'
                elif caracteres < 45:
                    size = .80
                    halign = 'left'
                elif caracteres < 48:
                    size = .85
                    halign = 'left'
                else:
                    size = .90
                    halign = 'left'
                self.kivyapp.ids.chat_list.add_widget(Eu(text=f'{message_text}', size_hint_x=size, halign=halign))
            else:
                caracteres = len(message_text)
                ele = Ele()
                print(ele.ids.box.padding)
                if caracteres < 3:
                    size = .35
                    halign = 'center'

                    print(ele.ids.box.padding)
                elif caracteres < 6:
                    size = .40
                    halign = 'center'
                    print('stop 2')

                    print(ele.ids.box.padding)
                elif caracteres < 9:
                    size = .45
                    halign = 'center'
                    print('stop 3')

                    print(ele.ids.box.padding)
                elif caracteres < 12:
                    size = .50
                    halign = 'center'

                    print('stop 4')
                elif caracteres < 15:
                    size = .56
                    halign = 'center'

                elif caracteres < 18:
                    size = .65
                    halign = 'center'

                elif caracteres < 21:
                    size = .69
                    halign = 'center'

                elif caracteres < 24:
                    size = .74
                    halign = 'center'

                elif caracteres < 27:
                    size = .79
                    halign = 'center'

                elif caracteres < 30:
                    size = .84
                    halign = 'center'

                elif caracteres < 33:
                    size = .89
                    halign = 'center'

                elif caracteres < 36:
                    size = .94
                    halign = 'center'
                else:
                    size = .95
                    halign = 'left'
                self.kivyapp.ids.chat_list.add_widget(
                    Ele(text=f'{message_text}', image_source=f'{self.image(username)}', size_hint_x=size, halign=halign)
                )

        Clock.schedule_once(atualizar_chat)

        self.kivyapp.ids.message_scroll.scroll_y = 0



# Classe onde vai fica toda a logica da interface ----------------------------------------------------------------------
class PrincipalScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.cont = 0
        # Configurações do textfield de trocar nome --------------------------------------------------------------------
        self.textfield_nome = MDTextField(
            id="textfield_nome",
            pos_hint={'center_x': 0.39, 'center_y': 0.9},
            size_hint=(0.65, None),
            text=self.nome(),
            font_style='Headline',
            role='medium',
            theme_text_color='Custom',
            md_bg_color=(0, 0, 0, 1),
            theme_line_color='Custom',
            line_color_normal=(1, 1, 1, 1),
            line_color_focus=(1, 1, 1, 1),
            font_size='18sp',
            padding=[15, 15, 15, 15],
            mode="outlined",  # Alternativa para "outlined
        )
        self.textfield_nome.bind(text=self.limitar_nome)
        # Configurações do textfield de trocar a bio -------------------------------------------------------------------
        self.textfield = MDTextField(
            id='bio',
            mode="outlined",
            text=self.text_bio(),
            multiline=True,
            max_height= "120dp",
            size_hint_x=0.8,
            size_hint_y=0.8,
        )
        self.textfield.bind(text=self.reajuste)
        self.card3 = MDCard(
            style='elevated',
            size_hint=(None, None),
            size=("80dp", "45dp"),
            pos_hint={'top': 0.93, 'right': 0.92},
            padding="16dp",
            theme_shadow_color="Custom",
            shadow_color="black",
            theme_bg_color='Custom',
            md_bg_color=(0, 1, 0, 1),
            radius=[15],
            shadow_offset=(1, -2),
            shadow_softness=1,
            elevation_level=2,
        )
        box3 = BoxLayout(size_hint=(1, 1), orientation='horizontal', padding=0, spacing=0)
        label3 = MDLabel(
            text="Entrar",
            theme_text_color="Custom",
            text_color="white",
            halign='center',
            font_style="Title",
            role='medium',
            bold=True
        )
        box3.add_widget(label3)
        self.card3.add_widget(box3)
        self.card3.bind(on_release=self.novo_nome)
        # configurações dos botões de ações do textfield ---------------------------------------------------------------
        self.boxlayout = BoxLayout(spacing=20)
        card1 = MDCard(
            style='elevated',
            size_hint=(None, None),
            size=("100dp", "45dp"),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            theme_shadow_color="Custom",
            shadow_color="black",
            theme_bg_color='Custom',
            md_bg_color=(1, 0, 0, 1),
            radius=[15],
            shadow_offset=(1, -2),
            shadow_softness=2,
            elevation_level=2,
        )
        box1 = BoxLayout(size_hint=(1, 1), orientation='horizontal', padding=0, spacing=0)
        label1 = MDLabel(
            text="Cancelar",
            theme_text_color="Custom",
            text_color="white",
            halign='center',
            font_style="Title",
            role='medium',
            bold=True
        )
        box1.add_widget(label1)
        card1.add_widget(box1)
        card1.bind(on_release=self.cancelar)
        card2 = MDCard(
            style='elevated',
            size_hint=(None, None),
            size=("80dp", "45dp"),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            theme_shadow_color="Custom",
            shadow_color="black",
            theme_bg_color='Custom',
            md_bg_color=(0, 1, 0, 1),
            radius=[15],
            shadow_offset=(1, -2),
            shadow_softness=1,
            elevation_level=2,
        )
        box2 = BoxLayout(size_hint=(1, 1), orientation='horizontal', padding=0, spacing=0)
        label2 = MDLabel(
            text="Entrar",
            theme_text_color="Custom",
            text_color="white",
            halign='center',
            font_style="Title",
            role='medium',
            bold=True
        )
        box2.add_widget(label2)
        card2.add_widget(box2)
        card2.bind(on_release=self.alterar_bio)
        self.boxlayout.add_widget(card1)
        self.boxlayout.add_widget(card2)

        # Inicializando a conexão como chat ----------------------------------------------------------------------------
        self.websocket_client = WebSocketClient(self, f'{self.nome()}')
        self.max_lines = 6
        self.existir = False
        self.ids.screen_manager.current = 'Perfil'

    def limitar_nome(self, instance, value):
        if len(value) >= 15:
            self.textfield_nome.text = value[:15]

    def color_ele(self):
        return get_color_from_hex("#68dbe3")

    # Definindo a logica da trocar de telas entra navigations ----------------------------------------------------------

    def on_switch_tabs(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        # Mudança de abas no MDScreenManager
        self.ids.screen_manager.current = item_text
        if self.ids.screen_manager.current == 'Chat':
            self.cont += 1
            if self.cont <= 1:
                self.websocket_client.carregar_mensagens()
                self.ids.centro.remove_widget(self.ids.navigation)
            else:
                self.ids.centro.remove_widget(self.navigation_bar)
        elif self.ids.screen_manager.current == 'Home':
            self.ids.perfis.clear_widgets()
            self.adicionando_perfis()

    def sair_do_chat(self):
        self.ids.screen_manager.current = 'Home'
        self.navigation_bar = MDNavigationBar(
            id='navigation',
            on_switch_tabs=self.on_switch_tabs
        )

        self.navigation_bar.add_widget(BaseMDNavigationItem(icon="home", text="Home"))
        self.navigation_bar.add_widget(BaseMDNavigationItem(icon="chat", text="Chat"))
        self.navigation_bar.add_widget(BaseMDNavigationItem(icon="account-circle", text="Perfil"))

        self.ids.centro.add_widget(self.navigation_bar)

    # Configurações do chat --------------------------------------------------------------------------------------------
    def limitar(self):
        texto = self.ids.message.text
        print(len(texto))
        if len(texto) >= 50:
            self.ids.message.text = texto[:100]

    def receber(self, data):
        self.websocket_client.receber_mensagem(data)

    def send(self):
        if self.ids.message.text != '':
            mensagem = self.ids.message.text
            self.websocket_client.enviar_mensagem(mensagem)
            self.ids.message.text = ''

    # Configurações do perfil ------------------------------------------------------------------------------------------

    def image(self):
        return 'https://res.cloudinary.com/dsmgwupky/image/upload/v1726094211/image_stqmqg.png'

    def caminho_imagem(self, result_queue):
        url = f'https://api-imagem.onrender.com/get-imagem?name=4'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result_queue.put(data['message'])
        else:
            result_queue.put(None)

    def caminho_imagem_thread(self):
        result_queue = queue.Queue()

        # Inicia a thread para realizar a requisição de imagem
        thread = threading.Thread(target=self.caminho_imagem, args=(result_queue,))
        thread.start()
        thread.join()  # Aguarda a conclusão da thread

        # Retorna o resultado da fila (pode ser a URL da imagem ou None)
        return result_queue.get()

    def abrir_galeria(self):
        filechooser.open_file(on_selection=self.selecionar)

    def selecionar(self, selection):
        if selection:
            print(f"Arquivo selecionado: {selection[0]}")
            self.recortar_imagem(selection[0], f'{self.user()}.png')
        else:
            print("Nenhum arquivo foi selecionado.")

    def recortar_imagem(self, caminho, salvar, size=(110, 110)):
        # Abrir a imagem
        img = Image.open(caminho).convert('RGBA')

        # Criar uma máscara circular
        mask = Image.new("L", (size[0], size[1]), 0)  # Máscara do tamanho do perfil
        draw = ImageDraw(mask)

        # Calcular o raio e o centro
        radius = min(size) // 2
        center = (size[0] // 2, size[1] // 2)

        # Desenhar um círculo na máscara
        draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill=255)

        # Redimensionar a imagem original
        img = img.resize((size[0], size[1]))

        # Criar a imagem recortada
        img_cropped = Image.new("RGBA", (size[0], size[1]))
        img_cropped.paste(img, (0, 0), mask=mask)

        # Salvar a imagem recortada
        img_cropped.save(salvar)
        self.salvar = salvar
        server = threading.Thread(target=self.salvar_imagem)
        server.start()

    def nome_existir(self):
        server = threading.Thread(target=self.check)
        server.start()
        print(server)

    def check(self):
        url = f'https://api-name.onrender.com/check-name?name={self.textfield_nome.text}'
        response = requests.get(url)
        try:
            data = response.json()
            if data['exists']:
                return True
            else:
                return False
        except:
            print('chupa')

    def salvar_imagem_in_thread(self, image_path, result_queue):
        url = f'https://api-imagem.onrender.com/upload-image?name={self.user()}&id=4'

        try:
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                response = requests.post(url, files=files)

            if response.status_code == 200:
                result = response.json()
                result_queue.put(result['secure_url'])  # Coloca a URL segura na fila
            else:
                result_queue.put(None)  # Se o status não for 200, retorna None
        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put(None)

    def salvar_imagem(self):
        result_queue = queue.Queue()
        image_path = self.salvar

        # Inicia a thread para salvar a imagem
        thread = threading.Thread(target=self.salvar_imagem_in_thread, args=(image_path, result_queue))
        thread.start()
        thread.join()  # Aguarda a conclusão da thread

        # Obtém o resultado da fila
        secure_url = result_queue.get()

        if secure_url:
            self.ids.img_perfil.source = secure_url
        else:
            print("Erro ao enviar a imagem.")

    def seguidores_in_thread(self, result_queue):
        url = 'https://api-perfil.onrender.com/get-seguidores?id=4'

        try:
            response = requests.get(url)
            data = response.json()
            print(data)
            result_queue.put(data['informações'])  # Coloca as informações na fila
        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put('0')  # Retorna '0' em caso de erro

    def seguidores(self):
        result_queue = queue.Queue()

        # Inicia a thread para obter seguidores.kv
        thread = threading.Thread(target=self.seguidores_in_thread, args=(result_queue,))
        thread.start()
        thread.join()  # Aguarda a conclusão da thread

        # Obtém o resultado da fila
        seguidores_info = result_queue.get()

        if seguidores_info != '0':
            return seguidores_info
        else:
            return '0'

    def seguindo_in_thread(self, result_queue):
        url = 'https://api-perfil.onrender.com/get-seguindo?id=4'

        try:
            response = requests.get(url)
            data = response.json()
            print(data)
            result_queue.put(data['informações'])
        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put('0')

    def seguindo(self):
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.seguindo_in_thread, args=(result_queue,))
        thread.start()
        thread.join()

        seguindo_info = result_queue.get()

        if seguindo_info != '0':
            return seguindo_info
        else:
            return '0'

    def nome_in_thread(self, result_queue):
        url = 'https://api-perfil.onrender.com/get-name?id=4'
        response = requests.get(url)

        try:
            data = response.json()
            print(data)
            result_queue.put(f'{str(data["informações"])[:15]}..')  # Corrigido para usar aspas duplas

        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put('User')  # Retorna 'User' em caso de erro

    def user_in_thread(self, result_queue):
        url = 'https://api-perfil.onrender.com/get-name?id=4'
        response = requests.get(url)

        try:
            data = response.json()
            print(data)
            result_queue.put(data['informações'])

        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put('User')  # Retorna 'User' em caso de erro

    def text_bio_in_thread(self, result_queue):
        url = 'https://api-perfil.onrender.com/get-bio?id=4'
        response = requests.get(url)

        try:
            data = response.json()
            print(data)
            self.ajustar_bio(data['informações'])
            result_queue.put(str(data['informações']).replace('/n', '\n'))  # Corrigido para formatar a bio

        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put('Não tem bio')  # Retorna 'Não tem bio' em caso de erro

    def nome(self):
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.nome_in_thread, args=(result_queue,))
        thread.start()
        thread.join()
        return result_queue.get()

    def user(self):
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.user_in_thread, args=(result_queue,))
        thread.start()
        thread.join()
        return result_queue.get()

    def text_bio(self):
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.text_bio_in_thread, args=(result_queue,))
        thread.start()
        thread.join()

        return result_queue.get()

    def ajustar_bio(self, texto):

        if len(texto) <= 200 and len(texto) > 146:
            self.ids.layout.pos_hint = {'center_x': 0.56, 'center_y': 1.0}
            print('2')

        elif len(texto) <= 146 and len(texto) > 115:
            self.ids.layout.pos_hint = {'center_x': 0.56, 'center_y': 1.2}
            print('1')


        if len(texto) <= 70:
            self.ids.layout.pos_hint = {'center_x': 0.56, 'center_y': 1.08}
            print('3')

    def reajuste(self, instance, value):
        textfield = self.textfield.text
        print(len(value))
        self.textfield.text = value[:190]

        if len(value) <= 200 and len(value) > 146:
            self.textfield.pos_hint = {'center_y': 0.6, 'center_x': 0.5}
            self.boxlayout.pos_hint = {'center_y': 0.46, 'center_x': 0.89}
            print('reajustado1 ')

        elif len(value) <= 146 and len(value) > 115:
            self.textfield.pos_hint = {'center_y': 0.62, 'center_x': 0.5}
            self.boxlayout.pos_hint = {'center_y': 0.47, 'center_x': 0.89}
            print('reajustado2')

        if len(value) <= 115 and len(value) > 70:
            self.textfield.pos_hint = {'center_y': 0.62, 'center_x': 0.5}
            self.boxlayout.pos_hint = {'center_y': 0.5, 'center_x': 0.89}
            print('reajustado3')

        if len(value) <= 70:
            self.textfield.pos_hint = {'center_y': 0.63, 'center_x': 0.5}
            self.boxlayout.pos_hint = {'center_y': 0.52, 'center_x': 0.89}
            print('reajustado4 ')

    def ajustar(self):
        textfield = self.text_bio()
        print(len(textfield))

        if len(textfield) <= 200:
            print('reajustado1 ')
            return {'center_y': 0.6, 'center_x': 0.5}

        elif len(textfield) <= 146:
            print('reajustado2')
            return {'center_y': 0.62, 'center_x': 0.5}

        if len(textfield) <= 115:
            print('reajustado3')
            return {'center_y': 0.53, 'center_x': 0.5}

        if len(textfield) <= 50:
            print('reajustado4 ')
            return {'center_y': 0.54, 'center_x': 0.5}

    def ajustar_botoes(self):
        textfield = self.text_bio()
        print(len(textfield))

        if len(textfield) <= 200 and len(textfield) > 146:
            print('seleto1 ')
            return {'center_y': 0.44, 'center_x': 0.89}

        elif len(textfield) <= 146 and len(textfield) > 115:
            print('seleto2')
            return {'center_y': 0.47, 'center_x': 0.89}

        if len(textfield) <= 115 and len(textfield) > 70:
            print('reajustado3')
            return {'center_y': 0.48, 'center_x': 0.89}

        if len(textfield) <= 70:
            print('reajustado4 ')
            return {'center_y': 0.5, 'center_x': 0.89}

    def adicionar_bio(self):
        self.ids.bio.text = ''
        self.ids.layout.pos_hint={'center_y': 0.1}
        self.textfield.pos_hint = self.ajustar()
        self.boxlayout.pos_hint = self.ajustar_botoes()
        self.ids.centro2.add_widget(self.textfield)
        self.ids.centro2.add_widget(self.boxlayout)

    def cancelar(self, instance):
        self.ids.bio.text = self.text_bio()

        self.ids.centro2.remove_widget(self.textfield)
        self.ids.centro2.remove_widget(self.boxlayout)

    def alterar_bio(self, instance):
        server = threading.Thread(target=self.url_bio_thread)
        server.start()
        self.ids.bio.text = self.textfield.text
        self.ajustar_bio(self.textfield.text)
        self.ids.centro2.remove_widget(self.boxlayout)
        self.ids.centro2.remove_widget(self.textfield)

    def url_bio_thread(self):
        url = f'https://api-bio.onrender.com/alterar-bio?nome={self.nome()}&bio={self.textfield.text}'
        response = requests.post(url)
        data = response.json()

    def adicionar_textfield_nome(self):
        self.ids.itadori.text = ''
        self.ids.edit.pos_hint = {'top': 0.93, 'right': 1.1}
        self.textfield_nome.focus = True
        self.ids.centro2.add_widget(self.card3)
        self.ids.centro2.add_widget(self.textfield_nome)

    def snack(self):
        MDSnackbar(
            MDSnackbarSupportingText(
                text="Usuario ja cadastrado",
            ),
            MDSnackbarButtonContainer(
                MDSnackbarCloseButton(
                    icon="close",
                ),
                pos_hint={"center_y": 0.5}
            ),
            y=dp(24),
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()

    def adicionando_perfis(self):
        # Cria uma fila para receber os dados da thread
        self.result_queue = queue.Queue()

        # Inicia uma thread para buscar os perfis
        thread = threading.Thread(target=self.fetch_perfis)
        thread.start()

    def fetch_perfis(self):
        url = 'https://api-home-p4dl.onrender.com/nomes?page=1'
        response = requests.get(url)
        data = response.json()

        # Adiciona seu próprio perfil se existir na lista
        for item in data:
            if item['nome'] == self.user():  # Verifica se o nome é o seu
                self.result_queue.put((item, True))  # Adiciona seu perfil na fila
                break  # Sai do loop depois de adicionar seu perfil

        # Adiciona os outros perfis que não são o seu
        for item in data:
            if item['nome'] != self.user():
                self.result_queue.put((item, False))  # Adiciona os outros perfis na fila

        # Chama a atualização da UI na thread principal
        Clock.schedule_once(self.update_perfis, 0)

    def update_perfis(self, dt):
        while not self.result_queue.empty():
            item, is_user_profile = self.result_queue.get()

            # Cria o card para o perfil
            card = MDCard(
                MDRelativeLayout(
                    AsyncImage(
                        source=item['perfil'],
                        allow_stretch=True,
                        size_hint=(None, None),
                        size=(dp(80), dp(80)),
                        pos_hint={'center_x': 0.5, 'center_y': 0.6},
                        keep_ratio=True
                    ),
                    MDLabel(
                        text=item['nome'],
                        adaptive_size=True,
                        color="grey",
                        pos_hint={'center_y': 0.2, 'center_x': 0.5},
                        halign='center',
                        bold=True
                    ),
                ),
                style="elevated",
                pos_hint={"center_x": .5, "center_y": .5},
                padding="4dp",
                size_hint=(None, None),
                size=("100dp", "150dp"),
                theme_shadow_color="Custom",
                shadow_color="white",
                theme_bg_color="Custom",
                md_bg_color="white",
                md_bg_color_disabled="grey",
                theme_shadow_offset="Custom",
                shadow_offset=(1, -2),
                theme_shadow_softness="Custom",
                shadow_softness=1,
                theme_elevation_level="Custom",
                elevation_level=2
            )

            # Adiciona o card no topo se for o perfil do usuário
            if is_user_profile:
                self.ids.perfis.add_widget(card, index=0)  # Adiciona o card no topo
            else:
                self.ids.perfis.add_widget(card)  # Adiciona os outros perfis

    def adicionar_scroll(self):
        # Move o scroll para a direita (incrementa 20% da largura total)
        target_x = min(self.ids.scroll.scroll_x + 0.5, 1)
        Clock.schedule_once(lambda dt: setattr(self.ids.scroll, 'scroll_x', target_x), 0.1)

    def remove_scroll(self):
        # Move o scroll para a esquerda (reduz 20% da largura total)
        target_x = max(self.ids.scroll.scroll_x - 0.5, 0)
        Clock.schedule_once(lambda dt: setattr(self.ids.scroll, 'scroll_x', target_x), 0.1)

    def novo_nome(self, instance):
        existir = self.check()
        if not existir:
            server = threading.Thread(target=self.requests)
            server.start()
            self.ids.itadori.text = self.textfield_nome.text
            self.ids.edit.pos_hint = {'top': 0.93, 'right': 0.92}
            self.ids.centro2.remove_widget(self.card3)
            self.ids.centro2.remove_widget(self.textfield_nome)
        else:
            self.snack()

    def requests(self):
        url = f'https://api-name.onrender.com/alterar-nome?nome={self.user()}&novo={self.textfield_nome.text}'
        response = requests.post(url)


