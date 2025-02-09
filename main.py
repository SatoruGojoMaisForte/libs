from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.edit_profile.edit_profile import EditProfile
from libs.screens.edit_profile_two.edit_profile_two import EditProfileTwo
from libs.screens.principal_screen.principal_screen import PerfilScreen
from libs.screens.table_screen.table_screen import TableScreen
from libs.screens.add_employee.add_employee import AddEmployee
from libs.screens.add_employee_avatar.add_employee_avatar import EmployeeAvatar
from kivy.core.window import Window


class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(PerfilScreen(name='Perfil'))
        self.screenmanager.add_widget(EmployeeAvatar(name='EmployeeAvatar'))
        self.screenmanager.add_widget(AddEmployee(name='Add'))
        self.screenmanager.add_widget(EditProfileTwo(name='EditProfileTwo'))
        self.screenmanager.add_widget(TableScreen(name='Table'))
        self.screenmanager.add_widget(EditProfile(name='EditProfile'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/edit_profile/edit_profile.kv')
        Builder.load_file('libs/screens/principal_screen/principal_screen.kv')
        Builder.load_file('libs/screens/edit_profile_two/edit_profile_two.kv')
        Builder.load_file('libs/components/navigations_buttons.kv')
        Builder.load_file('libs/screens/table_screen/table_screen.kv')
        Builder.load_file('libs/screens/add_employee/add_employee.kv')
        Builder.load_file('libs/screens/add_employee_avatar/add_employee_avatar.kv')


MainApp().run()
