from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.choice_account.choice_account import ChoiceAccount
from libs.screens.init_screen.init_screen import InitScreen
from libs.screens.register_funcionario.register_funcionario import RegisterFuncionario
from libs.screens.register_contractor.register_contractor import RegisterContractor



class MainApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(InitScreen(name='Init'))
        self.screenmanager.add_widget(ChoiceAccount(name='ChoiceAccount'))
        self.screenmanager.add_widget(RegisterContractor(name='RegisterContractor'))
        self.screenmanager.add_widget(RegisterFuncionario(name='RegisterFuncionario'))


        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/init_screen/init_screen.kv')
        Builder.load_file('libs/screens/choice_account/choice_account.kv')
        Builder.load_file('libs/screens/register_funcionario/register_funcionario.kv')
        Builder.load_file('libs/screens/register_contractor/register_contractor.kv')


MainApp().run()
