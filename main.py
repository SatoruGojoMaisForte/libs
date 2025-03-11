from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.edit_profile.edit_profile import EditProfile
from libs.screens.edit_profile_employee.edit_profile_employee import EditProfileEmployee
from libs.screens.edit_profile_two.edit_profile_two import EditProfileTwo
from libs.screens.fourth_week.fourth_week import FourthWeek
from libs.screens.principal_screen.principal_screen import PerfilScreen
from libs.screens.table_screen.table_screen import TableScreen
from libs.screens.add_employee.add_employee import AddEmployee
from libs.screens.add_employee_avatar.add_employee_avatar import EmployeeAvatar
from libs.screens.function_screen.function_screen import FunctionScreen
from libs.screens.functions_screen.functions_screen import FunctionsScreen
from libs.screens.evaluation_screen.evaluation_screen import EvaluationScreen
from libs.screens.asses_punctuality.asses_punctuality import AssesPunctuality
from libs.screens.asses_effiency.asses_effiency import AssesEffiency
from libs.screens.asses_coexistence.asses_coexistence import AssesCoexistence
from libs.screens.third_week.third_week import ThirdWeek
from libs.screens.working_days.working_days import WorkingDays
from libs.screens.working_month.working_month import WorkingMonth
from libs.screens.first_week.first_week import FirstWeek
from libs.screens.second_week.second_week import SecondWeek
from kivy.core.window import Window


class MainApp(MDApp):

    def build(self):
        Window.size = (350, 700)
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(PerfilScreen(name='Perfil'))
        self.screenmanager.add_widget(WorkingDays(name='WorkingDays'))
        self.screenmanager.add_widget(EditProfileEmployee(name='EditProfileEmployee'))
        self.screenmanager.add_widget(EvaluationScreen(name='Evaluation'))
        self.screenmanager.add_widget(AssesEffiency(name='AssesEfficiency'))
        self.screenmanager.add_widget(FourthWeek(name='FourthWeek'))
        self.screenmanager.add_widget(ThirdWeek(name='ThirdWeek'))
        self.screenmanager.add_widget(SecondWeek(name='SecondWeek'))
        self.screenmanager.add_widget(FirstWeek(name='FirstWeek'))
        self.screenmanager.add_widget(WorkingMonth(name='WorkingMonth'))
        self.screenmanager.add_widget(AssesCoexistence(name='AssesCoexistence'))
        self.screenmanager.add_widget(AssesPunctuality(name='AssesPunctuality'))
        self.screenmanager.add_widget(AddEmployee(name='Add'))
        self.screenmanager.add_widget(EmployeeAvatar(name='EmployeeAvatar'))
        self.screenmanager.add_widget(EditProfileTwo(name='EditProfileTwo'))
        self.screenmanager.add_widget(FunctionsScreen(name='Functions'))
        self.screenmanager.add_widget(FunctionScreen(name='Function'))
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
        Builder.load_file('libs/screens/function_screen/function_screen.kv')
        Builder.load_file('libs/screens/functions_screen/functions_screen.kv')
        Builder.load_file('libs/screens/evaluation_screen/evaluation_screen.kv')
        Builder.load_file('libs/screens/asses_punctuality/asses_punctuality.kv')
        Builder.load_file('libs/screens/asses_effiency/asses_effiency.kv')
        Builder.load_file('libs/screens/asses_coexistence/asses_coexistence.kv')
        Builder.load_file('libs/screens/working_days/working_days.kv')
        Builder.load_file('libs/screens/working_month/working_month.kv')
        Builder.load_file('libs/screens/first_week/first_week.kv')
        Builder.load_file('libs/screens/second_week/second_week.kv')
        Builder.load_file('libs/screens/third_week/third_week.kv')
        Builder.load_file('libs/screens/fourth_week/fourth_week.kv')
        Builder.load_file('libs/screens/edit_profile_employee/edit_profile_employee.kv')

MainApp().run()
