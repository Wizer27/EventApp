from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_garden.mapview import MapView, MapMarkerPopup

class MapApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        mapview = MapView(
            zoom=15,
            lat=55.7522,
            lon=37.6156,
        )
        
        # Маркер 1 с подписью
        marker1 = MapMarkerPopup(lat=55.7522, lon=37.6156, source="Images/mr2.png")
        label1 = Label(text="Красная площадь", size_hint=(None, None), size=(150, 40))
        marker1.add_widget(label1)
        
        # Маркер 2 с подписью
        marker2 = MapMarkerPopup(lat=55.7523, lon=37.616, source="Images/mr2.png")
        label2 = Label(text="Другое место", size_hint=(None, None), size=(150, 40))
        marker2.add_widget(label2)
        
        mapview.add_marker(marker1)
        mapview.add_marker(marker2)
        layout.add_widget(mapview)
        
        return layout

MapApp().run()