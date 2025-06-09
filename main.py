import requests



def get_location_by_ip():
    response = requests.get('https://ipinfo.io/json').json()
    return {
        #'city': response.get('city'),
        #'region': response.get('region'),
        #'country': response.get('country'),
        'coords': response.get('loc')  # Широта,долгота (например, "59.93,30.31")
    }



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
    query = f"""
    [out:json];
    (
      node["amenity"="{amenity}"](around:{radius},{lat},{lon});
    );
    out body;
    """
    response = requests.post('https://overpass-api.de/api/interpreter', data=query)
    return response.json()




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


cords = get_location_by_ip()
print(cords['coords'])  
c = cords['coords'].split(',')
    

places = find_cafe(c[0], c[1])  
print("#############")
print("CAFES:")
print("#############")
for place in places['elements']:
    if place['tags'].get('name') is not None:
        print(place['tags'].get('name'))    

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


















