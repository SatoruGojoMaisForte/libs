from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.working_month.working_month import WorkingMonth
from kivy.core.window import Window


class MainApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(WorkingMonth(name='WorkingMonth'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/working_month/working_month.kv')


MainApp().run()
