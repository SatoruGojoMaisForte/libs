import re
import requests
import threading
import queue
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from dotenv import set_key


class SendCode(MDScreen):

    def save_email_to_env(self, email):
        env_file = ".env"
        set_key(env_file, "EMAIL_USER", email)

    def set_email(self):
        self.verificar_email = self.ids.verificar_email.text

    def chama_login(self):
        self.manager.current = 'Login'

    def is_email_valid(self, text: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, text) is not None

    def email_existir(self, email, result_queue):
        # Check if the email exists in the database
        response = requests.get(f"https://api-email-evhk.onrender.com/check-email?email={email}")
        data = response.json()

        if data['existir']:
            result_queue.put(True)
        else:
            result_queue.put(False)

    def send_verification_email(self, email, result_queue):
        response = requests.post(f"https://api-email-evhk.onrender.com/send_verification_code?email={email}")
        try:
            data = response.json()

            if data['enviado']:
                result_queue.put(True)

        except:
            result_queue.put(False)

    def email_existir_in_thread(self, email):
        result_queue = queue.Queue()

        # Inicia a thread para verificar se o email existe
        thread = threading.Thread(target=self.email_existir, args=(email, result_queue))
        thread.start()
        thread.join()  # Aguarda a conclusão da thread

        # Retorna o resultado da fila
        return result_queue.get()

    def send_verification_email_in_thread(self, email):
        result_queue = queue.Queue()

        # Inicia a thread para enviar o código de verificação
        thread = threading.Thread(target=self.send_verification_email, args=(email, result_queue))
        thread.start()
        thread.join()  # Aguarda a conclusão da thread

        # Retorna o resultado da fila
        return result_queue.get()

    def enviar_codigo(self):
        # verificar se o campo está vazio
        texto = self.ids.verificar_email.text

        if texto:
            # verificar se o texto está no formato de um email
            if self.is_email_valid(texto):
                self.ids.erros.text = ''
                email_existi = self.email_existir_in_thread(texto)

                if email_existi:
                    # enviar um código de verificação no email da pessoa
                    enviar = self.send_verification_email_in_thread(texto)
                    if enviar:
                        self.manager.current = "Check"
                        self.save_email_to_env(email=texto)
                    else:
                        print('Falha ao enviar')
                else:
                    self.ids.erros.text = 'Email não encontrado'
            else:
                self.ids.verificar_email.error = True
                self.ids.erros.text = 'O email está em um formato inválido'
        else:
            self.ids.verificar_email.error = True
            self.ids.erros.text = 'Preencha o campo com o email'
