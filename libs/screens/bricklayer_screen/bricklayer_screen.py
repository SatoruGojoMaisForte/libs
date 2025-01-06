from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDListItemTrailingCheckbox, MDListItemHeadlineText, MDListItem, MDListItemLeadingIcon
from kivymd.uix.screen import MDScreen


class ListItem(MDListItem):
    text = StringProperty()


class BricklayerScreen(MDScreen):
    nome = 'Custoviano lobo'
    avatar = 'https://res.cloudinary.com/dsmgwupky/image/upload/v1731366361/image_o6cbgf.png'

