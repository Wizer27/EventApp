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
import requests
from geopy.geocoders import Nominatim
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
Window.clearcolor = (0.08, 0.08, 0.08, 1)



##########################
#Локальные функции
##########################
def get_location_by_ip():
    response = requests.get('https://ipinfo.io/json').json()
    return {
        #'city': response.get('city'),
        #'region': response.get('region'),
        #'country': response.get('country'),
        'coords': response.get('loc')  # Широта,долгота (например, "59.93,30.31")
    }

#Функция для преобразования координат в полный адресс
def reveal_adress(cd1:float,cd2:float):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.reverse(f"{str(cd1)},{str(cd2)}")
    return location.address
c = reveal_adress(55.751244,37.618423)
print("Testing Addreses")
print(c)


# Функции для нахождения различных мест по ключевым словам






def find_cafe(lat, lon, radius=500, amenity='cafe'):
    """
    Ищет места по типу (кафе, бар и т.д.) в радиусе от заданных координат.
    Возвращает список словарей с названиями и координатами.
    Формат вывода: [{'name': '...', 'lat': ..., 'lon': ...}, ...]
    """
    query = f"""
    [out:json];
    node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    out body;
    """
    
    try:
        response = requests.post(
            'https://overpass-api.de/api/interpreter',
            data={'data': query},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Тело ответа сервера: {e.response.text[:200]}")  # Логируем начало ошибки
        return []

    places = []
    for element in data.get('elements', []):
        if element['type'] == 'node':
            name = element.get('tags', {}).get('name', 'Без названия')
            places.append({
                'name': name,
                'lat': element.get('lat'),
                'lon': element.get('lon')
            })
    
    return places


    



  

def find_restaurant(lat, lon, radius=1000, amenity='restaurant'):
    """
    Ищет места по типу (кафе, бар и т.д.) в радиусе от заданных координат.
    Возвращает список словарей с названиями и координатами.
    Формат вывода: [{'name': '...', 'lat': ..., 'lon': ...}, ...]
    """
    query = f"""
    [out:json];
    node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    out body;
    """
    
    try:
        response = requests.post(
            'https://overpass-api.de/api/interpreter',
            data={'data': query},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Тело ответа сервера: {e.response.text[:200]}")  # Логируем начало ошибки
        return []

    places = []
    for element in data.get('elements', []):
        if element['type'] == 'node':
            name = element.get('tags', {}).get('name', 'Без названия')
            places.append({
                'name': name,
                'lat': element.get('lat'),
                'lon': element.get('lon')
            })
    
    return places


def find_events(lat, lon, radius=1000, amenity='nightclub'):
    """
    Ищет места по типу (кафе, бар и т.д.) в радиусе от заданных координат.
    Возвращает список словарей с названиями и координатами.
    Формат вывода: [{'name': '...', 'lat': ..., 'lon': ...}, ...]
    """
    query = f"""
    [out:json];
    node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    out body;
    """
    
    try:
        response = requests.post(
            'https://overpass-api.de/api/interpreter',
            data={'data': query},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Тело ответа сервера: {e.response.text[:200]}")  # Логируем начало ошибки
        return []

    places = []
    for element in data.get('elements', []):
        if element['type'] == 'node':
            name = element.get('tags', {}).get('name', 'Без названия')
            places.append({
                'name': name,
                'lat': element.get('lat'),
                'lon': element.get('lon')
            })
    
    return places





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
        
        # Создаем ScrollView с Label внутри
        scroll = ScrollView(size_hint=(1, 1))
        self.scroll_label = DarkLabel(
            text="Нажмите на кнопку", 
            size_hint_y=None,
            halign='left',  # Выравнивание по левому краю
            valign='top',   # Выравнивание по верху
            text_size=(Window.width - dp(80), None)  # Ширина текста с учетом padding
        )
        spinner = Spinner(
            text='Выберите пункт',
            values=('Пункт 1', 'Пункт 2', 'Пункт 3'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        spinner.bind(text=self.on_spinner_select)
        self.scroll_label.bind(
            texture_size=self.scroll_label.setter('size')  # Автоподстройка высоты
        )
        scroll.add_widget(self.scroll_label)
        
        self.button = GradientPurpleButton(text="НАЖМИ МЕНЯ")
        self.button.on_release_action = self.show_text
        layout.add_widget(spinner)
        layout.add_widget(scroll)
        layout.add_widget(self.button)
        self.add_widget(layout)
    def on_spinner_select(self, spinner, text):
            print(f"Выбран: {text}")
    def show_text(self):
        print("Button is working OK")
        cords = get_location_by_ip()
        c = cords['coords'].split(',')
        places = find_cafe(c[0], c[1], 1000)  
        text = ""
        text += "CAFES:" + '\n'
        for place in places:
            text += f"{place['name']} | Координаты: {place['lat']}, {place['lon']}" + '\n'
        places_music = find_restaurant(c[0],c[1])
        text += "RESTAURANTS:" + '\n'
        for place in places_music:
            text += f"{place['name']} | Координаты: {place['lat']}, {place['lon']}"    
        self.scroll_label.text = text
        
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