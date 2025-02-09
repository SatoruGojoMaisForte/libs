from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


KV = '''
MDScreen:
    MDCard:
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        theme_line_color: 'Custom'
        border: [0,]
        line_color: 'grey'
        theme_bg_color: 'Custom'
        md_bg_color: 1, 1, 1, 1
        
        MDRelativeLayout:
            AsyncImage:
                source: 'https://res.cloudinary.com/dsmgwupky/image/upload/v1739053352/image_1_hkgebk.png'
                size_hint: 0.5, 0.5
                pos_hint: {'center_x': 0.5, 'center_y': 0.65}
            
            MDLabel:
                text: 'Tudo certo!!'
                bold: True
                theme_text_color: 'Custom'
                halign: 'center'
                font_style: 'Headline'
                role: 'small'
            
            MDLabel:
                text: 'O funcionario foi adicionado com sucesso verifique na sua tabela'
                font_style: 'Label'
                role: 'large'
                pos_hint: {'center_x': 0.5, 'center_y': 0.43}
                padding: [20, 0, 20, 0]
                halign: 'center'
                theme_text_color: 'Custom'   
                text_color: 'grey'
            
            MDButton:
                theme_width: 'Custom'
                size_hint_x: .3
                theme_bg_color: 'Custom'
                md_bg_color: [0.0, 1.0, 0.0, 1.0]
                pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                
                
                MDButtonText:
                    text: 'Ok'
                    theme_text_color: 'Custom'
                    text_color: 'white'
                    halign: 'center'
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    font_style: 'Title'
                    role: 'medium'
                    bold: True
                    
                
'''


class MyApp(MDApp):
    def build(self):
        Window.size = (350, 800)
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)


MyApp().run()
