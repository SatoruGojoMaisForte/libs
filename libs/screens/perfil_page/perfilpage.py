import os
import threading

import requests
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
import queue
import dotenv
dotenv.load_dotenv()

class PerfilPage(MDScreen):
    avatar = StringProperty()

    def on_enter(self, *args):
        self.carregar_all()
        self.carregar_nome()

    # carregando bios --------------------------------------------------------------------------------------------------
    def all_perfil(self, result_queue):
        id = os.getenv('ID')
        url = f'https://api-imagem.onrender.com/all-perfil?id={id}'
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

    # carregando o nome ------------------------------------------------------------------------------------------------
    def caminho_name(self, result_queue):
        id = os.getenv('ID')
        url = f'https://api-perfil.onrender.com/get-name?id={id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result_queue.put(data['informações'])
        else:
            result_queue.put('nome não encontrado')

    def carregar_nome(self):
        result_queue = queue.Queue()
        # Inicia a thread para realizar a requisição de nome
        threading.Thread(target=self.caminho_name, args=(result_queue,)).start()

        # Retorna o resultado da fila após a conclusão da thread
        seguidores = result_queue.get()
        seguidores_widget = self.ids.name
        seguidores_widget.atualizar_name(seguidores)


