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

Window.clearcolor = (0.08, 0.08, 0.08, 1)

Builder.load_string('''
<GradientPurpleButton>:
    canvas.before:
        # Тень
        Color:
            rgba: 0.3, 0, 0.5, 0.3
        RoundedRectangle:
            pos: self.x-3, self.y-3
            size: self.width+6, self.height+6
            radius: [self.border_radius]
        
        # Градиент
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.border_radius]
        
        # Блики
        Color:
            rgba: 1, 1, 1, 0.1
        RoundedRectangle:
            pos: self.x, self.y + self.height * 0.7
            size: self.width, self.height * 0.3
            radius: [self.border_radius]
''')

class GradientPurpleButton(Button):
    bg_color = ListProperty([0.45, 0.1, 0.9, 1])
    border_radius = NumericProperty(dp(12))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0, 0, 0, 0]
        self.color = [1, 1, 1, 1]
        self.font_size = dp(16)
        self.bold = True
        self.size_hint = (None, None)
        self.size = (dp(220), dp(55))
        self.pos_hint = {'center_x': 0.5}
        self.always_release = True
        
        self.bind(
            on_enter=self.on_hover,
            on_leave=self.on_hover_leave
        )
    
    def on_hover(self, *args):
        Animation(bg_color=[0.55, 0.2, 1.0, 1], d=0.15).start(self)
    
    def on_hover_leave(self, *args):
        Animation(bg_color=[0.45, 0.1, 0.9, 1], d=0.3).start(self)
    
    def on_press(self):
        # Анимация изменения цвета и размера вместо scale
        Animation(bg_color=[0.35, 0.05, 0.8, 1], d=0.1).start(self)
        Animation(width=self.width*0.98, height=self.height*0.98, d=0.1).start(self)
    
    def on_release(self):
        Animation(bg_color=[0.55, 0.2, 1.0, 1], d=0.3).start(self)
        Animation(width=self.size[0], height=self.size[1], d=0.3).start(self)
        if hasattr(self, 'on_release_action'):
            self.on_release_action()

class DarkLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0.9, 0.9, 0.9, 1)
        self.font_size = dp(18)
        self.halign = 'center'
        self.valign = 'middle'
        self.size_hint_y = None
        self.height = dp(100)
class ScreenMain(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title = "EventsNearby"
        
        layout = BoxLayout(
            orientation='vertical', 
            padding=dp(40), 
            spacing=dp(30)
        )
        
        self.label = DarkLabel(text="Нажмите на кнопку")
        
        self.button = GradientPurpleButton(text="НАЖМИ МЕНЯ")
        self.button.on_release_action = self.show_text
        
        layout.add_widget(self.label)
        layout.add_widget(self.button)
        self.add_widget(layout)
    
    
    def show_text(self):
        print("Button is working OK")
        self.manager.transition.direction = 'left'
        self.manager.current = "lenpasword"
        self.label.text = "Кнопка сработала успешно!"
        Animation(
            color=[0.3, 0.9, 0.6, 1],
            d=0.5,
            t='out_elastic'
        ).start(self.label)
class Second(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        boxlayout = BoxLayout(orientation="vertical", spacing=5, padding=[10])

        button_new_pasword = Button(
            text="Return",
            background_color=[2, 1.5, 3, 1],
            size_hint=[1, 0.1],
            on_press=self._on_press_button_new_pasword,
        )

        boxlayout.add_widget(button_new_pasword)
        self.add_widget(boxlayout)

    def _on_press_button_new_pasword(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_screen'
   
class Main(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ScreenMain(name='main_screen'))
        sm.add_widget(Second(name='lenpasword'))

        return sm
if __name__ == "__main__":
    Main().run()