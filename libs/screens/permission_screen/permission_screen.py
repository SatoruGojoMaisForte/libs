from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from android.permissions import request_permissions, check_permission, Permission

class PermissionScreen(MDScreen):

    def on_enter(self):
        """
        Quando a tela é carregada, verifica as permissões.
        """
        self.check_and_request_permissions()

    def check_and_request_permissions(self):
        """
        Verifica e solicita permissões, se necessário.
        """
        permissions_to_request = []
        required_permissions = [
            Permission.CAMERA,
            Permission.RECORD_AUDIO,
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.INTERNET
        ]

        for permission in required_permissions:
            if not check_permission(permission):
                permissions_to_request.append(permission)

        if permissions_to_request:
            print("Solicitando permissões...")
            request_permissions(permissions_to_request, self.permission_callback)
        else:
            print("Todas as permissões já foram concedidas.")
            self.on_permissions_granted()

    def permission_callback(self, permissions, results):
        """
        Callback chamado após o usuário permitir ou negar permissões.
        """
        if all(results):
            self.on_permissions_granted()
        else:
            self.on_permissions_denied()

    def on_permissions_granted(self):
        """
        Ações a serem executadas se as permissões forem concedidas.
        """
        print("Permissões concedidas.")
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'EditProfile'

    def on_permissions_denied(self):
        """
        Ações a serem executadas se as permissões forem negadas.
        """
        print("Permissões negadas.")
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Denied'
