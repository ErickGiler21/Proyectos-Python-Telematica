import folium

print("Creador de mapa con ruta simple entre dos puntos")
lat1 = float(input("Latitud punto 1: "))
lon1 = float(input("Longitud punto 1: "))
lat2 = float(input("Latitud punto 2: "))
lon2 = float(input("Longitud punto 2: "))

# Centro del mapa
centro_lat = (lat1 + lat2) / 2
centro_lon = (lon1 + lon2) / 2

mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=13)

# Marcadores
folium.Marker([lat1, lon1], popup="Punto A").add_to(mapa)
folium.Marker([lat2, lon2], popup="Punto B").add_to(mapa)

# Línea recta (simula ruta)
folium.PolyLine([[lat1, lon1], [lat2, lon2]], color="blue", weight=5, opacity=0.8).add_to(mapa)

mapa.save("ruta_fibra.html")
print("Mapa guardado como ruta_fibra.html → ábrelo en tu navegador")