from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.list import MDListItemLeadingAvatar

class PostCards(MDCard):
    profile_pic = StringProperty()
    username = StringProperty()
    avatar = StringProperty()
    post = StringProperty()
    caption = StringProperty()
    likes = StringProperty()
    posted_ago = StringProperty()
    comments = StringProperty()
