import queue
import os
import requests
import threading
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen

from KivyMD.kivymd.app import MDApp
from libs.components.circle_perfis import CirclePerfis
from libs.components.post_cards import PostCards
from dotenv import load_dotenv
load_dotenv()


class HomePage(MDScreen):
    perfis_loaded = False  # Variável de controle para perfis
    posts_loaded = False  # Variável de controle para postagens

    def on_enter(self):
        # Carrega os perfis e postagens apenas na primeira vez
        if not self.perfis_loaded:
            threading.Thread(target=self.list_perfis).start()  # Inicia thread para carregar perfis
            self.perfis_loaded = True  # Marca que os perfis foram carregados

        if not self.posts_loaded:
            threading.Thread(target=self.list_posts).start()  # Inicia thread para carregar postagens
            self.posts_loaded = True  # Marca que as postagens foram carregadas

    def list_perfis(self):
        url = 'https://api-home-p4dl.onrender.com/nomes?page=1'
        try:
            response = requests.get(url)
            data = response.json()

            # Atualiza a interface do usuário no thread principal
            Clock.schedule_once(lambda dt: self.update_perfis(data))

        except Exception as e:
            print(f"Erro ao carregar perfis: {e}")

    def caminho_name(self, result_queue):
        id = os.getenv('ID')
        url = f'https://api-perfil.onrender.com/get-name?id={id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result_queue.put(data['informações'])
        else:
            result_queue.put('nome não encontrado')

    def nome(self):
        result_queue = queue.Queue()
        # Inicia a thread para realizar a requisição de nome
        threading.Thread(target=self.caminho_name, args=(result_queue,)).start()

        # Retorna o resultado da fila após a conclusão da thread
        return result_queue.get()

    def update_perfis(self, data):
        # Atualiza perfis com nome de usuários
        nome = self.nome()
        for item in data:
            if item['nome'] != nome:
                self.ids.stories.add_widget(CirclePerfis(
                    avatar=item['perfil'],
                    name=item['nome'],

                ))

    def caminho_imagem(self, result_queue):
        id = os.getenv('ID')
        url = f'https://api-imagem.onrender.com/get-imagem?name={id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result_queue.put(data['message'])
        else:
            result_queue.put('https://res.cloudinary.com/dsmgwupky/image/upload/v1726685784/a8da222be70a71e7858bf752065d5cc3-fotor-20240918154039_dokawo.png')

    def avatar(self):
        result_queue = queue.Queue()

        # Inicia a thread para realizar a requisição de imagem
        threading.Thread(target=self.caminho_imagem, args=(result_queue,)).start()

        # Retorna o resultado da fila após a conclusão da thread
        return result_queue.get()

    def list_posts(self):
        # Simula a carga de postagens
        Clock.schedule_once(lambda dt: self.update_posts())

    def update_posts(self):
        # Atualiza as postagens na interface
        self.ids.timeline.add_widget(PostCards(
            username='Miranha',
            avatar='https://res.cloudinary.com/dsmgwupky/image/upload/v1728587443/4.png',
            post='https://res.cloudinary.com/dsmgwupky/image/upload/v1728672252/meme_got8sw.jpg',
            likes='234',
            caption='memes.com'
        ))

