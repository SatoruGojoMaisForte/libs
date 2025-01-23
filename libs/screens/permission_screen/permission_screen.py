from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from android.permissions import request_permissions, check_permission, Permission


class PermissionScreen(MDScreen):

    def request_permission(self):
        """
        Verifica e solicita permissões, se necessário.
        """
        if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
            request_permissions(
                permissions=[
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE
                ],
                callback=self.permission_callback
            )
            print("Solicitando permissões...")
        else:
            print("Permissões já concedidas.")
            self.on_permissions_granted()

    def permission_callback(self, permissions, results):
        """
        Callback chamado após o pedido de permissões.
        """
        if all(results):
            print("Todas as permissões foram concedidas.")
            self.on_permissions_granted()
        else:
            print("Algumas permissões foram negadas.")
            self.on_permissions_denied()

    def on_permissions_granted(self):
        """
        Ações a serem executadas se as permissões forem concedidas.
        """
        print("Permissões concedidas, execute a funcionalidade necessária.")
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'EditProfile'

    def on_permissions_denied(self):
        """
        Ações a serem executadas se as permissões forem negadas.
        """
        print("Permissões negadas, mostre uma mensagem ou desative a funcionalidade.")
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'Denied'
