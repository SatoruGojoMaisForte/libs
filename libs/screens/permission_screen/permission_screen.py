from kivymd.uix.screen import MDScreen
from plyer import call


class PermissionScreen(MDScreen):

    def request_permission(self):
       try:
            call('settings', action='android.intent.action.MAIN')

        except NotImplementedError:
            print("Funcionalidade não suportada neste dispositivo.")

    
