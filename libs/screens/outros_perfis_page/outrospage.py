import os
import queue
import threading
import requests
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from libs.components_perfil.seguidores import Seguidores
import dotenv
dotenv.load_dotenv()


class OutrosPage(MDScreen):
    avatar = StringProperty()
    username = StringProperty()

    def on_enter(self, *args):
        self.carregar_all()
        self.verificar()
        Clock.schedule_interval(self.verificar_resultado_seguidor, 0.1)

    def verificar(self):
        self.result_queue = queue.Queue()
        thread = threading.Thread(target=self.verificar_seguidor, args=(self.result_queue,))
        thread.start()
        Clock.schedule_interval(self.verificar_resultado_seguidor, 0.1)

    def verificar_resultado_seguidor(self, dt):
        try:
            seguir = self.result_queue.get_nowait()
        except queue.Empty:
            return

        if not seguir:
            self.ids.bot_seguir.text = 'Seguir o usuario'
            self.ids.bot.md_bg_color = [0, 149 / 255, 246 / 255, 1]
            self.ids.bot_seguir.text_color = 'white'
        else:
            self.ids.bot_seguir.text = 'Seguindo o usuario'
            self.ids.bot.md_bg_color = [1, 1, 1, 0.8]
            self.ids.bot_seguir.text_color = 'black'

        Clock.schedule_once(self.verificar_resultado_seguidor, 0.1)

    # verificando se ele seguir ----------------------------------------------------------------------------------------
    def verificar_seguidor(self, result_queue):
        id_user = os.getenv('ID')
        url = f'https://api-home-p4dl.onrender.com/verificar-seguidor?seguidor={id_user}&seguido={self.id_bio()['id_seguido']}'
        response = requests.get(url)
        try:
            data = response.json()
            result_queue.put(data['seguir'])
        except:
            result_queue.put(False)

    def seguidor(self):
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.verificar_seguidor, args=(result_queue,))
        thread.start()
        return result_queue.get()

    def alterar(self):
        # verificar se ele seguir a pessoa ou não
        seguir = self.seguidor()
        if self.ids.bot_seguir.text == 'Seguir o usuario':
            self.ids.bot_seguir.text = 'Seguindo o usuario'
            self.ids.bot.md_bg_color = [1, 1, 1, 0.8]
            self.ids.bot_seguir.text_color = 'black'
            self.following()
            return
        if self.ids.bot_seguir.text == 'Seguindo o usuario':
            self.ids.bot_seguir.text = 'Seguir o usuario'
            self.ids.bot.md_bg_color = [0, 149 / 255, 246 / 255, 1]
            self.ids.bot_seguir.text_color = 'white'
            self.remover_seguidores()
            return

    def text_id(self, result_queue):
        url = f'https://api-imagem.onrender.com/get-id?nome={self.username}'
        response = requests.get(url)

        try:
            data = response.json()
            result_queue.put(data)
        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put('0')

    def id_bio(self):
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.text_id, args=(result_queue,))
        thread.start()
        data = result_queue.get()
        Clock.unschedule(lambda dt: self.id_bio(), 0.1)
        return {'id_seguido': data.get('id_seguido'), 'seguindo': data.get('seguindo')}

    # modificando seguidores -------------------------------------------------------------------------------------------

    def followers(self):
        id_user = os.getenv('ID')
        url = f'https://api-home-p4dl.onrender.com/follower?seguidor={id_user}&seguido={self.id_bio()['id_seguido']}'

        try:
            # Faz a requisição HTTP dentro da thread para não travar a interface
            response = requests.post(url)
            data = response.json()

            # Atualiza o resultado na thread principal da interface
            if data['adicionado']:
                print('adicionado')

        except Exception as e:
            print(f"Erro ao adicionar seguidor: {e}")

    def following(self):
        # Inicia a função `followers` em uma thread separada
        threading.Thread(target=self.followers).start()

    def thread_remover_seguidores(self, result_queue):
        id_user = os.getenv('ID')
        url = f'https://api-home-p4dl.onrender.com/remover-seguidor?name={self.username}&seguidor={id_user}&seguido={self.id_bio()['id_seguido']}'
        response = requests.post(url)
        try:
            data = response.json()
            result_queue.put(str(data['message']))
        except:
            result_queue.put('0')

    def remover_seguidores(self):
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.thread_remover_seguidores, args=(result_queue,))
        thread.start()

        seguidores = self.ids.seguir
        seguidores.atualizar_seguidores(result_queue.get())

    # carregando perfil ------------------------------------------------------------------------------------------------
    def all_perfil(self, result_queue):
        url = f'https://api-imagem.onrender.com/all-perfil?id={self.id_bio()['id_seguido']}'
        response = requests.get(url)

        try:
            data = response.json()
            print(data)
            result_queue.put(data)

        except Exception as e:
            print(f"Erro: {e}")
            result_queue.put('Não tem bio')

    def carregar_all(self):
        """Carrega os elementos do perfil através de um thread"""
        result_queue = queue.Queue()
        thread = threading.Thread(target=self.all_perfil, args=(result_queue,))
        thread.start()

        """Carregando a bio na interface principal atraves da api"""
        data = result_queue.get()
        bio = data.get('bio', 'Usuario do chatto')
        bio_widget = self.ids.bio
        bio_widget.atualizar_bio(bio)
        Clock.unschedule(lambda dt: self.carregar_all(), 0.1)

        """Carregando os seguidos na interface principal atraves da api"""
        seguidos = data.get('seguidos', '0')
        seguidos_widget = self.ids.seguido
        seguidos_widget.atualizar_seguindo(seguidos)
        Clock.unschedule(lambda dt: self.carregar_all(), 0.1)

        """Carregando os seguidores na interface principal atraves da api"""
        seguidores = data.get('seguidores', '0')
        seguidores_widget = self.ids.seguir
        seguidores_widget.atualizar_seguidores(seguidores)
        Clock.unschedule(lambda dt: self.carregar_all(), 0.1)

    # carregando imagem do meu perfil ----------------------------------------------------------------------------------
    def caminho_imagem(self, result_queue):
        id = os.getenv('ID')
        url = f'https://api-imagem.onrender.com/get-imagem?name={id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result_queue.put(data['message'])
        else:
            result_queue.put('https://res.cloudinary.com/dsmgwupky/image/upload/v1726685784/a8da222be70a71e7858bf752065d5cc3-fotor-20240918154039_dokawo.png')

    def my_avatar(self):
        result_queue = queue.Queue()

        # Inicia a thread para realizar a requisição de imagem
        threading.Thread(target=self.caminho_imagem, args=(result_queue,)).start()

        # Retorna o resultado da fila após a conclusão da thread
        return result_queue.get()
