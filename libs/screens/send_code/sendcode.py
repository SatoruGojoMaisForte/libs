import re
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen


class SendCode(MDScreen):
    cont_email = 0  # Contador para tentativas de verificação de e-mail
    cont_envio = 0  # Contador para tentativas de envio de código

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
        url = f"https://api-email-5a79.onrender.com/check-email?email={email}"
        UrlRequest(
            url,
            on_success=self.existir,
            on_error=self.error_request_email,
            method='GET'
        )

    def error_request_email(self, req, error):
        self.cont_email += 1  # Incrementa o contador de tentativas
        if self.cont_email <= 3:
            self.email_existir(self.ids.verificar_email.text)  # Tenta novamente
        else:
            icon_error = self.ids['error']
            progress = self.ids['progress']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_error)
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
            self.ids.texto_carregando.text = 'Falha ao verificar o e-mail. Verifique sua internet.'

    def existir(self, req, result):
        data = result
        if data['existir']:
            self.enviar(self.ids.verificar_email.text)
        else:
            self.remove_widget(self.card)
            self.ids.erros.text = 'Email não cadastrado'

    def enviar(self, email):
        url = f"https://api-email-5a79.onrender.com/send_verification_code?email={email}"
        UrlRequest(
            url,
            on_success=self.enviado,
            on_error=self.error_enviar_codigo,
            method='POST'
        )

    def error_enviar_codigo(self, req, error):
        self.cont_envio += 1  # Incrementa o contador de tentativas
        if self.cont_envio <= 3:
            self.enviar(self.ids.verificar_email.text)  # Tenta novamente
        else:
            icon_error = self.ids['error']
            progress = self.ids['progress']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_error)
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
            self.ids.texto_carregando.text = 'Falha ao enviar verificação. Tente novamente mais tarde.'

    def enviado(self, req, result):
        data = result
        if data['enviado']:
            progress = self.ids['progress']
            icon_acerto = self.ids['acerto']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_acerto)
            self.ids.texto_carregando.text = 'Verificação enviada'
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
        else:
            icon_error = self.ids['error']
            progress = self.ids['progress']
            self.ids['relative'].remove_widget(progress)
            self.ids['relative'].add_widget(icon_error)
            self.ids.texto_carregando.pos_hint = {'center_x': .5, 'center_y': .55}
            self.ids.texto_carregando.text = 'Verificação não enviada'

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
