from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarker 

class MapApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Создаем карту
        mapview = MapView(
            zoom=15,
            lat=55.7522,
            lon=37.6156,
            size = (1,1)
            
        )
        
        # Добавляем маркер
        marker = MapMarker(lat=55.7522, lon=37.6156, source="Images/mr2.png")
        marker2 = MapMarker(lat = 55.7523,lon = 37.616,source = "Images/mr2.png")
        mapview.add_marker(marker)
        mapview.add_marker(marker2)
        layout.add_widget(mapview)
        return layout

MapApp().run()