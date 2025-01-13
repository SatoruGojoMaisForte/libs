from kivymd.uix.screen import MDScreen
from android.permissions import request_permissions, Permission, check_permission


class PermissionScreen(MDScreen):

    def request_permission(self):
        """
        Verifica e solicita permissões, se necessário.
        """
        if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            print("Solicitando permissões...")
        else:
            print("Permissões já concedidas.")
