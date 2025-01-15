from kivymd.uix.screen import MDScreen
from jnius import autoclass


class ConfirmPermissions(MDScreen):
    def open_permissions(self, *args):
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
            intent.setData('package:' + PythonActivity.mActivity.getPackageName())
            PythonActivity.mActivity.startActivity(intent)
        except Exception as e:
            print(f"Erro ao abrir configurações: {e}")
