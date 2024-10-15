import os
import requests
from kivymd.uix.screen import MDScreen
from dotenv import load_dotenv
from time import sleep

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

cont = 0


class WriteCode(MDScreen):

    def check_code(self):
        code = self.ids.codigo.text
        email = os.getenv('EMAIL_USER')
        print(f'{email}')

        # Faz a requisição para verificar o código
        response = requests.post(
            f"https://api-email-evhk.onrender.com/verify_code?email={email}&code={code}"
        )
        data = response.json()

        # Verifica a resposta da API
        if data['message'] == 'O codigo digitado está correto':
            return True
        elif data['message'] == 'O codigo digitado está expirado':
            return False

    def check_text_length(self):
        # Verifica se o campo de código está vazio
        if self.ids.codigo.text == '':
            self.ids.codigo.focus = True
        else:
            text_field = self.ids.codigo
            max_length = 6

            # Remove espaços e limita o comprimento ao valor máximo
            text = text_field.text.replace(' ', '')
            if len(text) > max_length:
                text = text[:max_length]

            # Formata o texto em grupos de 3 caracteres
            formatted_text = ''.join(
                ''.join(text[i:i + 3]) for i in range(0, len(text), 3)
            )

            # Ajusta o campo de texto
            text_field.text = formatted_text
            text_field.halign = 'center'
            text_field.font_size = 40

    def voltar(self):
        self.manager.current = 'Check'

    def check(self):
        # Chama a função de verificação do código
        check = self.check_code()

        # Verifica se o código está correto
        if check:
            print(f'Código verificado com sucesso: {check}')
            self.ids.erros.text = ''
            self.manager.current = 'Login'
        else:
            self.ids.erros.text = 'O código inserido está incorreto'
