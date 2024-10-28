from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock


class LoginScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.contador_tentativas = 0  # Contador de tentativas

        # Realiza a requisição inicial com retries assíncronos
        Clock.schedule_once(lambda dt: self.warmup_api("https://api-name.onrender.com/ping"))
        Clock.schedule_once(lambda dt: self.warmup_api("https://api-password.onrender.com/ping", headers={'Authorization': 'Bearer spike'}))

    def warmup_api(self, url, headers=None, tentativa=1):
        """
        Função para "acordar" a API e aplicar backoff exponencial em caso de timeout,
        de forma assíncrona para evitar bloqueio da interface.
        """
        if tentativa > 3:  # Limite de tentativas
            return

        # Chama a API com UrlRequest e trata sucessos e falhas
        UrlRequest(
            url,
            timeout=4,
            method='GET',
            req_headers=headers,
            on_success=self.sucesso_chamada_inicial,
            on_error=lambda req, error: self.retry_warmup(url, headers, tentativa)
        )

    def retry_warmup(self, url, headers, tentativa):
        # Calcula o backoff e agenda a próxima tentativa
        backoff = 1 * (2 ** tentativa)
        Clock.schedule_once(lambda dt: self.warmup_api(url, headers, tentativa + 1), backoff)

    def sucesso_chamada_inicial(self, req, result):
        print("API aquecida com sucesso:", result)

    def on_enter(self, *args):
        # Define os ícones de erro e acerto
        self.ids['error'] = MDIconButton(
            icon='alert-circle',
            theme_font_size='Custom',
            font_size='55sp',
            icon_color='red',
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['acerto'] = MDIconButton(
            icon='check',
            theme_font_size='Custom',
            font_size='50sp',
            icon_color='green',
            pos_hint={'center_x': .5, 'center_y': .6}
        )

        # Configura o cartão de carregamento
        self.card = MDCard(
            id='carregando',
            style='elevated',
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            padding="16dp",
            md_bg_color=(1, 1, 1, 1)
        )
        self.ids['card'] = self.card

        # Cria o layout relativo
        relative = MDRelativeLayout()
        self.ids['relative'] = relative

        # Circular progress indicator
        circle = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.ids['progress'] = circle

        # Label de carregamento
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

    def verificar_nome(self):
        nome = self.ids.usuario.text
        url = f"https://api-name.onrender.com/check-name?name={nome}"

        UrlRequest(
            url,
            on_success=self.sucesso_nome,
            on_error=lambda req, error: self.error_request_name(req, error, tentativa=1),
            timeout=4,
            method='GET'
        )

    def error_request_name(self, req, error, tentativa):
        if tentativa <= 3 and str(error) == 'The read operation timed out':
            backoff = 1 * (2 ** tentativa)
            Clock.schedule_once(lambda dt: self.verificar_nome(), backoff)
        else:
            self.exibir_erro_usuario()

    def exibir_erro_usuario(self):
        icon_error = self.ids['error']
        progress = self.ids['progress']
        # Remove o widget de progresso e adiciona o ícone de erro
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_error)
        self.ids.texto_carregando.text = 'Falha ao verificar usuário. Verifique sua internet.'

    def sucesso_nome(self, req, result):
        self.contador_tentativas = 0
        data = result
        if data['exists']:
            self.ids.encontrar.text = ''
            self.ids.usuario.error = False
            self.verificar_senha()
        else:
            self.ids.encontrar.text = 'Usuário não cadastrado'
            self.ids.usuario.error = True

    def verificar_senha(self):
        senha = self.ids.senha.text
        nome = self.ids.usuario.text
        url = f"https://api-password.onrender.com/check-password?name={nome}&password={senha}"
        headers = {
            'Authorization': 'Bearer spike'
        }

        UrlRequest(
            url,
            method='GET',
            on_success=self.sucesso_senha,
            on_error=lambda req, error: self.error_request_senha(req, error, tentativa=1),
            timeout=5,
            req_headers=headers
        )

    def error_request_senha(self, req, error, tentativa):
        if tentativa <= 3 and str(error) == 'The read operation timed out':
            backoff = 1 * (2 ** tentativa)
            Clock.schedule_once(lambda dt: self.verificar_senha(), backoff)
        else:
            self.exibir_erro_senha()

    def exibir_erro_senha(self):
        icon_error = self.ids['error']
        progress = self.ids['progress']
        # Remove o widget de progresso e adiciona o ícone de erro
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_error)
        self.ids.texto_carregando.text = 'Falha ao verificar senha. Verifique sua internet.'

    def sucesso_senha(self, req, result):
        data = result
        if data['exists']:
            self.ids.senha_correta.text = ''
            self.ids.senha.error = False
            acerto = self.ids['acerto']
            progress = self.ids['progress']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(acerto)
            self.ids.texto_carregando.text = 'Login completo'
            print('senha correta')
        else:
            self.ids.senha_correta.text = 'Senha incorreta'
            self.ids.senha.error = True
            self.remove_widget(self.card)
            print('senha incorreta')

    def focus(self):
        textfield_usuario = self.ids.usuario
        textfield_password = self.ids.senha
        text_user = textfield_usuario.text
        text_password = textfield_password.text
        if not textfield_usuario.focus and not textfield_usuario.text:
            textfield_usuario.focus = True
        if text_user:
            textfield_password.focus = True
        if text_user and text_password:
            self.add_widget(self.card)
            self.verificar_nome()

    def chamar_trocar(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "Send"

    def cadastroscreen(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'cadastro'
