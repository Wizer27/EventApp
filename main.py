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

import requests

def find_cafe_with_address(lat, lon, radius=500, amenity='cafe'):
    query = f"""
    [out:json];
    (
      node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    """
    
    try:
        response = requests.post(
            'https://overpass-api.de/api/interpreter',
            data=query,
            timeout=10  # Таймаут на запрос
        )
        response.raise_for_status()  # Проверить HTTP-ошибки
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []
    except ValueError as e:  # Если JSON битый
        print(f"Ошибка парсинга JSON: {e}")
        print(f"Ответ сервера: {response.text[:200]}")  # Логируем начало ответа
        return []
    
    cafes = []
    for element in data.get('elements', []):
        if element['type'] == 'node':
            tags = element.get('tags', {})
            address = {
                'name': tags.get('name', 'Название не указано'),
                'street': tags.get('addr:street'),
                'housenumber': tags.get('addr:housenumber'),
                'city': tags.get('addr:city'),
                'postcode': tags.get('addr:postcode'),
                'lat': element.get('lat'),
                'lon': element.get('lon')
            }
            cafes.append(address)
    
    return cafes
    




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
    

places = find_cafe_with_address(c[0], c[1])  
print("#############")
print("CAFES:")
print("#############")
print(places)
#for place in places['elements']:
    #if place['tags'].get('name') is not None:
        #print(place['tags'].get('name'))    

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

















