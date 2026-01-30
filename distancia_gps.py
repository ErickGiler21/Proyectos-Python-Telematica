from math import radians, sin, cos, sqrt, atan2

def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distancia = R * c
    return distancia

print("Calculadora de distancia entre dos puntos GPS")
lat1 = float(input("Latitud punto 1 (ej -2.189): "))
lon1 = float(input("Longitud punto 1 (ej -79.889): "))
lat2 = float(input("Latitud punto 2: "))
lon2 = float(input("Longitud punto 2: "))

dist = distancia_km(lat1, lon1, lat2, lon2)
print(f"Distancia aproximada: {dist:.2f} km")