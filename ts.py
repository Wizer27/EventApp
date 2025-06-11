from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarker 

class MapApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Создаем карту
        mapview = MapView(
            zoom=12,
            lat=55.7522,
            lon=37.6156
        )
        
        # Добавляем маркер
        marker = MapMarker(lat=55.7522, lon=37.6156, source="marker.png")
        mapview.add_marker(marker)
        
        layout.add_widget(mapview)
        return layout

MapApp().run()