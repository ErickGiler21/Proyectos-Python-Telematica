import pandas as pd
from geopy.distance import geodesic
from itertools import permutations
import os

def crear_csv_ficticio_si_no_existe(archivo):
    data = pd.DataFrame({
        'nombre': ['NodoA', 'NodoB', 'NodoC', 'NodoD'],  # Agregué uno más para probar permutaciones
        'lat': [-2.1894, -2.2038, -2.2200, -2.1800],
        'lon': [-79.8892, -79.8975, -79.9000, -79.8800]
    })
    data.to_csv(archivo, index=False)
    print(f"CSV ficticio creado/actualizado: {archivo}")

def calcular_distancia_total(ruta, df):
    total = 0
    for i in range(len(ruta) - 1):
        punto1 = (df.loc[ruta[i], 'lat'], df.loc[ruta[i], 'lon'])
        punto2 = (df.loc[ruta[i+1], 'lat'], df.loc[ruta[i+1], 'lon'])
        total += geodesic(punto1, punto2).km
    return total

archivo_csv = "nodos_fibra.csv"

# Verificación confiable
if not os.path.exists(archivo_csv):
    crear_csv_ficticio_si_no_existe(archivo_csv)
else:
    print(f"Usando CSV existente: {archivo_csv}")

try:
    df = pd.read_csv(archivo_csv)
    print("\nDatos cargados:")
    print(df)
    
    df.set_index('nombre', inplace=True)
    puntos = list(df.index)
    
    if len(puntos) < 2:
        print("Error: Necesitas al menos 2 nodos para calcular rutas.")
    else:
        if len(puntos) > 5:  # Limita para no tardar eternamente (5! = 120 permutaciones)
            print("Demasiados puntos; limitando a 5 para rapidez.")
            puntos = puntos[:5]

        mejor_ruta = None
        min_dist = float('inf')
        for perm in permutations(range(len(puntos))):
            ruta_idx = list(perm)
            dist = calcular_distancia_total(ruta_idx, df)
            if dist < min_dist:
                min_dist = dist
                mejor_ruta = [puntos[i] for i in ruta_idx]

        print(f"\nMejor ruta encontrada: {' -> '.join(mejor_ruta)}")
        print(f"Distancia total aproximada: {min_dist:.2f} km")
except Exception as e:
    print(f"Error al procesar: {e}")
    print("Sugerencia: Verifica que el CSV tenga columnas 'nombre', 'lat', 'lon' sin errores.")