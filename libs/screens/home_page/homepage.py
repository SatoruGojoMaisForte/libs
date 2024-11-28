import threading
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from KivyMD.kivymd.app import MDApp
from libs.components.circle_perfis import CirclePerfis
from libs.components.post_cards import PostCards
from kivy.network.urlrequest import UrlRequest


class HomePage(MDScreen):
    email = 'sukunamec@gmail.com'
    perfis_loaded = False
    posts_loaded = False

    def on_enter(self):

        self.avatar()
        if not self.perfis_loaded:
            url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios.json'
            UrlRequest(
                url=url,
                on_success=self.usuarios
            )
            self.perfis_loaded = True

        if not self.posts_loaded:
            threading.Thread(target=self.list_posts).start()
            self.posts_loaded = True

    def usuarios(self, req, result):
        nome='Carol'
        contador = 0
        for user_id, user_data in result.items():
            contador += 1
            name = user_data.get('name')
            perfil = user_data.get('perfil')
            if nome != name:
                self.ids.stories.add_widget(CirclePerfis(
                    avatar=perfil,
                    name=name,

                ))
            if contador >= 10:
                break

    def update_perfis(self, data):
        # Atualiza perfis com nome de usuários
        nome = self.nome()
        for item in data:
            if item['nome'] != nome:
                self.ids.stories.add_widget(CirclePerfis(
                    avatar=item['perfil'],
                    name=item['nome'],

                ))

    # carregando o navigation é story creator --------------------------------------------------------------------------
    def avatar(self):
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

        # pegando codigo com index
        indice_usuario = next((k for k, v in usuarios.items() if v.get('email') == self.email), None)
        #
        perfil = usuarios[indice_usuario]['perfil']
        self.ids.story.avatar = perfil
        self.ids.navigation.avatar = perfil

    # carregando os posts ----------------------------------------------------------------------------------------------
    def list_posts(self):
        # Simula a carga de postagens
        Clock.schedule_once(lambda dt: self.update_posts())

    def update_posts(self):
        # Atualiza as postagens na interface
        self.ids.timeline.add_widget(PostCards(
            username='@Memes',
            avatar='https://res.cloudinary.com/dsmgwupky/image/upload/v1728587443/4.png',
            post='https://res.cloudinary.com/dsmgwupky/image/upload/v1728672252/meme_got8sw.jpg',
            likes='1.200',
            caption='memes.com.br.pt.lula.faz o L'
        ))

