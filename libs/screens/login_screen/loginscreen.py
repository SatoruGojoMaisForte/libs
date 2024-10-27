from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class LoginScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.contador_tentativas = 0  # Contador de tentativas
        self.chamada_inicial()
        self.chamada_inicial_senha()

    def chamada_inicial_senha(self):
        url = url = f"https://api-name.onrender.com/ping"
        headers = {
            'Authorization': 'Bearer spike'
        }

        UrlRequest(
            url,
            timeout=4,
            method='GET',
            req_headers=headers
        )

    def chamada_inicial(self):
        url = "https://api-name.onrender.com/ping"  # Endpoint de ping
        UrlRequest(
            url,
            on_success=self.sucesso_chamada_inicial,
            timeout=4,
            method='GET'
        )

    def sucesso_chamada_inicial(self, req, result):
        print(result)

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
        # chamei a requisição com timeout de 4 segundos
        nome = self.ids.usuario.text
        url = f"https://api-name.onrender.com/check-name?name={nome}"

        # Faz a requisição com tratamento de exceção
        try:
            UrlRequest(
                url,
                on_success=self.sucesso_nome,
                on_error=self.error_request_name,
                timeout=4,
                method='GET'
            )
        except Exception as e:
            # se a requisição não retorna nada em 4 segundos eu chamo a função de erro
            self.error_request_name(None, e)

    def error_request_name(self, req, error):
        # verificar quantas vezes eu tentei fazer a requisição
        # verificar se o error foi de timeout ou não
        # se for ele vai pedir uma nova requisição

        if self.contador_tentativas <= 3:
            if str(error) == 'The read operation timed out':
                self.contador_tentativas += 1
                self.verificar_nome()
            else:
                pass

        else:
            self.exibir_erro_usuario()

    def exibir_erro_usuario(self):
        icon_error = self.ids['error']
        progress = self.ids['progress']
        # Remove o widget de progresso e adiciona o ícone de erro
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_error)

        # Atualiza a mensagem de carregamento
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
            on_error=self.error_request_senha,
            timeout=5,
            req_headers=headers
        )

    def error_request_senha(self, req, error):
        if self.contador_tentativas <= 3:
            if str(error) == 'The read operation timed out':
                self.contador_tentativas += 1
                self.verificar_senha()
            else:
                pass
        else:
            self.exibir_erro_senha()

    def exibir_erro_senha(self):
        icon_error = self.ids['error']
        progress = self.ids['progress']
        # Remove o widget de progresso e adiciona o ícone de erro
        self.ids['relative'].remove_widget(progress)
        self.ids['relative'].add_widget(icon_error)

        # Atualiza a mensagem de carregamento
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
        # Verificações se os campos estiverem vazios
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
