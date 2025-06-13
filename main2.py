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
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.textinput import TextInput 
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
class LogIn(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Вход в аккаунт"
        
        # Основной контейнер с затемнением
        main_box = BoxLayout(
            orientation='vertical',
            padding=dp(40),
            spacing=dp(25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.8)
        )
        # Заголовок
        title = Label(
            text="Создать аккаунт",
            font_size=dp(24),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint=(1, None),
            height=dp(40))
        
        # Контейнер для полей ввода
        input_box = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(220))
        
        # Стилизованные поля ввода
        self.username = TextInput(
            hint_text="Имя пользователя",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_active='',
            foreground_color=[0.9, 0.9, 0.9, 1],
            background_color=[0.12, 0.12, 0.12, 1],
            padding=dp(15),
            hint_text_color=[0.6, 0.6, 0.6, 1],
            cursor_color=[0.9, 0.9, 0.9, 1],
            cursor_width=dp(2))
        
        self.password = TextInput(
            hint_text="Пароль",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_active='',
            foreground_color=[0.9, 0.9, 0.9, 1],
            background_color=[0.12, 0.12, 0.12, 1],
            padding=dp(15),
            hint_text_color=[0.6, 0.6, 0.6, 1],
            cursor_color=[0.9, 0.9, 0.9, 1],
            cursor_width=dp(2))
        
        # Добавляем границы с закругленными углами
        for field in [self.username, self.password]:
            with field.canvas.before:
                Color(0.45, 0.1, 0.9, 0.7)  # Фиолетовый цвет границы
                field.rect = RoundedRectangle(
                    size=(field.width, field.height),
                    pos=field.pos,
                    radius=[dp(10)])
            field.bind(pos=self.update_field_rect, size=self.update_field_rect)
        
        # Кнопка подтверждения
        self.conf = GradientPurpleButton(text="Подтвердить")
        self.conf.on_release_action = self.print_logs
        
        # Ссылка на вход
        login_link = Label(
            text="Нет аккаунта? Создать.",
            font_size=dp(14),
            color=[0.6, 0.6, 0.6, 1],
            size_hint=(1, None),
            height=dp(30))
        login_link.bind(on_touch_down=self.switch_to_login)
        
        # Сборка интерфейса
        input_box.add_widget(self.username)
        input_box.add_widget(self.password)
        
        main_box.add_widget(title)
        main_box.add_widget(input_box)
        main_box.add_widget(self.conf)
        main_box.add_widget(login_link)
        
        self.add_widget(main_box)
    
    def update_field_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def print_logs(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_screen'
        print(f"Username: {self.username.text}")
        print(f"Password: {self.password.text}")
    
    def switch_to_login(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print("Переход к форме входа")
            # Здесь можно добавить переход к экрану входа
            # self.manager.current = 'login'
            self.manager.transition.direction = 'left'
            self.manager.current = 'register' 
class Register(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title = "Регистрация"
        main_box = BoxLayout(
            orientation='vertical',
            padding=dp(40),
            spacing=dp(25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.8)
        )
        # Заголовок
        title = Label(
            text="Создать аккаунт",
            font_size=dp(24),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint=(1, None),
            height=dp(40))
        
        # Контейнер для полей ввода
        input_box = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(220))
        
        # Стилизованные поля ввода
        self.username = TextInput(
            hint_text="Имя пользователя",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_active='',
            foreground_color=[0.9, 0.9, 0.9, 1],
            background_color=[0.12, 0.12, 0.12, 1],
            padding=dp(15),
            hint_text_color=[0.6, 0.6, 0.6, 1],
            cursor_color=[0.9, 0.9, 0.9, 1],
            cursor_width=dp(2))
        
        self.password = TextInput(
            hint_text="Пароль",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_active='',
            foreground_color=[0.9, 0.9, 0.9, 1],
            background_color=[0.12, 0.12, 0.12, 1],
            padding=dp(15),
            hint_text_color=[0.6, 0.6, 0.6, 1],
            cursor_color=[0.9, 0.9, 0.9, 1],
            cursor_width=dp(2))
        for field in [self.username, self.password]:
            with field.canvas.before:
                Color(0.45, 0.1, 0.9, 0.7)  # Фиолетовый цвет границы
                field.rect = RoundedRectangle(
                    size=(field.width, field.height),
                    pos=field.pos,
                    radius=[dp(10)])
            field.bind(pos=self.update_field_rect, size=self.update_field_rect)
        input_box.add_widget(self.username)
        input_box.add_widget(self.password)
        
        main_box.add_widget(title)
        main_box.add_widget(input_box)
        self.add_widget(main_box)
    def update_field_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
        
            
               
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
        self.spinner = Spinner(
            text='Выберите пункт',
            values=('Рестораны', 'Клубы/Развлечения', 'Кафе/Перекусы'),
            size_hint=(None, None),
            size=(300, 200),
            pos_hint={'center_x': 0.5}
        )
        self.spinner.bind(text=self.on_spinner_select)
        self.scroll_label.bind(
            texture_size=self.scroll_label.setter('size')  # Автоподстройка высоты
        )
        scroll.add_widget(self.scroll_label)
        
        self.button = GradientPurpleButton(text="НАЙТИ")
        self.button2 = GradientPurpleButton(text = "Посмотреть на карте")
        self.button2.on_release_action = self.show_on_map
        self.button.on_release_action = self.show_text
        layout.add_widget(self.spinner)
        layout.add_widget(scroll)
        layout.add_widget(self.button)
        layout.add_widget(self.button2)
        self.add_widget(layout)
    def on_spinner_select(self, spinner, text) -> str:
        print(text)
        return text
            
    def show_text(self):
        print("Button is working OK")
        cords = get_location_by_ip()
        c = cords['coords'].split(',')
        places = find_cafe(c[0], c[1], 1000)  
        text = ""
        if self.spinner.text == "Кафе/Перекусы":
            print("CAFE is working")
            text += "CAFES:" + '\n'
            for place in places:
                text += f"{place['name']} | Координаты: {place['lat']}, {place['lon']}" + '\n'
        if self.spinner.text == "Рестораны":     
            places_music = find_restaurant(c[0],c[1])
            text += "RESTAURANTS:" + '\n'
            for place in places_music:
                text += f"{place['name']} | Координаты: {place['lat']}, {place['lon']}" + '\n' 
        if self.spinner.text == "Клубы/Развлечения":
            parks = find_events(c[0],c[1],2000)
            text += "CLUBS/EVENTS:" + '\n'
            for place in parks:
                text += f"{place['name']} | Координаты: {place['lat']}, {place['lon']}" + '\n'
        self.scroll_label.text = text
        return text
    def show_on_map(self):
        print("Showing on map") 
        self.manager.transition.direction = 'left'
        self.manager.current = 'lenpasword' 
            
class Second(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        boxlayout = BoxLayout(orientation="horizontal", spacing=5, padding=[10])

        button_new_pasword = Button(
            text="<- Вернуться назад ",
            background_color=[2, 1.5, 3, 1],
            size_hint=[1, 0.1],
            on_press=self._on_press_button_new_pasword,
        )
        mapview = MapView(
            zoom=15,
            lat=55.7522,
            lon=37.6156,
            size = (1,1)
            
        )
        
        # Добавляем маркер
        boxlayout.add_widget(button_new_pasword)
        marker = MapMarker(lat=55.7522, lon=37.6156, source="Images/mr2.png")
        marker2 = MapMarker(lat = 55.7523,lon = 37.616,source = "Images/mr2.png")
        mapview.add_marker(marker)
        mapview.add_marker(marker2)
        boxlayout.add_widget(mapview)

        self.add_widget(boxlayout)

    def _on_press_button_new_pasword(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_screen'
class Main(App):
    def build(self):
        sm = ScreenManager()
        self.states = {}
        sm.add_widget(LogIn(name = "login"))
        sm.add_widget(Register(name = "register"))
        sm.add_widget(ScreenMain(name='main_screen'))
        sm.add_widget(Second(name='lenpasword'))

        return sm    
if __name__ == "__main__":
    Main().run()