import requests
from geopy.geocoders import Nominatim


#Берем аддрес исходя из IP через API
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
def find(lat,lon,radius = 1500,amenity = ""):
    query = f"""
    [out:json];
    (
      node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    );
    out body;
    """
    response = requests.post('https://overpass-api.de/api/interpreter', data=query)
    return response.json()

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


    




def find_restaurant(lat, lon, radius=500, amenity='restaurant'):
    query = f"""    
    [out:json];
    (
      node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    );
    out body;
    """
    response = requests.post('https://overpass-api.de/api/interpreter', data=query)
    return response.json()    

def find_events(lat,lon,radius = 10000,amenity = "nightclub"):
    query = f"""
    [out:json];
    (
      node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    );
    out body;
    """
    response = requests.post('https://overpass-api.de/api/interpreter', data=query)
    return response.json()  

#Вывод мест в отсротированом порядке
cords = get_location_by_ip() 
c = cords['coords'].split(',')
    

places = find_cafe(c[0], c[1],1000)  
print("#############")
print("CAFES:")
print("#############")

for place in places:
    print(f"{place['name']} | Координаты: {place['lat']}, {place['lon']}")

places_music = find_restaurant(c[0],c[1])


print("#############")
print("RESTAURANTS:")
print("#############")


for mn in places_music['elements']:
    if mn['tags'].get('name') is not None:
        print(mn['tags'].get('name'))

print("#############")
print("EVENTS/CLUBS:")
print("#############")

parks = find_events(c[0],c[1])
for pr in parks['elements']:
    if pr['tags'].get('name') is not None:
        print(pr['tags'].get('name'))

















