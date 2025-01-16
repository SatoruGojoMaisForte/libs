from kivymd.uix.screen import MDScreen
from plyer import call


class ConfirmPermissions(MDScreen):
    def open_permissions(self):
        try:
            call('settings', action='android.intent.action.MAIN')
        except NotImplementedError:
            print("Funcionalidade não suportada neste dispositivo.")
