import folium  # Instala si no lo tienes
import pandas as pd

# Crea un CSV simple manualmente o usa datos ficticios
data = pd.DataFrame({
    'lat': [-2.189, -2.200],  # Ej: coordenadas de Guayaquil
    'lon': [-79.889, -79.900],
    'nombre': ['Nodo1', 'Nodo2']
})

mapa = folium.Map(location=[-2.189, -79.889], zoom_start=13)
for idx, row in data.iterrows():
    folium.Marker([row['lat'], row['lon']], popup=row['nombre']).add_to(mapa)
mapa.save('mapa_red.html')  # Abre en navegador