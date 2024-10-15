import queue
import threading
from kivymd.uix.screen import MDScreen
import requests

click_button_user = 0
click_button_password = 0


class LoginScreen(MDScreen):

    def check_name(self, result_queue):
        name = self.ids.usuario.text

        # Check if the name exists in the database
        response = requests.get(f"https://api-name.onrender.com/check-name?name={name}")
        try:
            data = response.json()

            if data['exists']:
                result_queue.put(True)
            else:
                result_queue.put(False)
        except:
            result_queue.put(False)

    def check_password(self, name, password, result_queue):
        url = f"https://api-password.onrender.com/check-password?name={name}&password={password}"
        headers = {
            'Authorization': 'Bearer spike'
        }
        response = requests.get(url, headers=headers)
        try:
            data = response.json()

            if not data['exists']:
                result_queue.put(False)
            else:
                result_queue.put(True)
        except:
            result_queue.put(False)

    def check_name_in_thread(self):
        result_queue = queue.Queue()

        # Inicia a thread para verificar o nome
        thread = threading.Thread(target=self.check_name, args=(result_queue,))
        thread.start()
        thread.join()  # Aguarda a conclusão da thread

        # Retorna o resultado da fila
        return result_queue.get()

    def check_password_in_thread(self, name, password):
        result_queue = queue.Queue()

        # Inicia a thread para verificar a senha
        thread = threading.Thread(target=self.check_password, args=(name, password, result_queue))
        thread.start()
        thread.join()  # Aguarda a conclusão da thread

        # Retorna o resultado da fila
        return result_queue.get()

    def focus(self):
        global click_button_user, click_button_password
        textfield_usuario = self.ids.usuario
        textfield_password = self.ids.senha
        text_user = self.ids.usuario.text
        text_password = textfield_password.text

        # verificações se os campos estiverem vazios
        if not textfield_usuario.focus and not textfield_usuario.text:
            textfield_usuario.focus = True
            click_button_user += 1

        if text_user:
            textfield_password.focus = True

        if text_user and text_password:
            user_existir = self.check_name_in_thread()

            if not user_existir:
                self.ids.encontrar.text = 'Usuario não cadastrado'
                self.ids.usuario.error = True

            else:
                self.ids.encontrar.text = ''
                senha = self.check_password_in_thread(self.ids.usuario.text, self.ids.senha.text)

                if senha:
                    self.ids.senha_correta.text = ''
                    self.manager.current = 'principal'
                else:
                    self.ids.senha_correta.text = 'A senha está incorreta'
                    self.ids.senha.error = True

    def chamar_trocar(self, *args):
        self.manager.current = "Send"
