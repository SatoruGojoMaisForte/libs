from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screenmanager import MDScreenManager
from libs.screens.working_days.working_days import WorkingDays
from kivy.core.window import Window


class MainApp(MDApp):

    def build(self):
        self.load_all_kv_files()
        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(WorkingDays(name='WorkingDays'))
        return self.screenmanager

    def load_all_kv_files(self):
        Builder.load_file('libs/screens/working_days/working_days.kv')


MainApp().run()
