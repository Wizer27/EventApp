import plotly.express as px

# Данные: города с координатами
data = {
    "city": ["Москва", "Санкт-Петербург", "Казань"],
    "lat": [55.7522, 59.9343, 55.7961],
    "lon": [37.6156, 30.3351, 49.1064]
}

fig = px.scatter_geo(data, lat="lat", lon="lon", text="city")
fig.update_geos(center=dict(lat=55, lon=45), scope="world")
fig.show()