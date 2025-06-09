import plotly
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import webbrowser
class Button_Map(Button):
    def __init__(self,link):
        self.link = link
    def op_press(self):
        webbrowser.open(self.link)
            