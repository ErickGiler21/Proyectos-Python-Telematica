# TelematicaTools.py - Herramienta integrada para telemática/GIS/redes
# Autor: Erick Giler Veintimilla - Proyecto personal 2026

import json
import time
import os
import pandas as pd
from ping3 import ping
from geopy.distance import geodesic
from itertools import permutations
from statistics import mean

# ────────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL
# ────────────────────────────────────────────────
HISTORIAL_PING = "historial_ping.json"
NODOS_FIBRA_CSV = "nodos_fibra.csv"

# ────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ────────────────────────────────────────────────

def cargar_json(archivo):
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_json(archivo, data):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ────────────────────────────────────────────────
# 1. MONITOREO DE LATENCIA (PING)
# ────────────────────────────────────────────────

def medir_latencia(host='8.8.8.8'):
    try:
        delay = ping(host, unit='ms', timeout=5)
        return delay if delay is not None else float('inf')
    except Exception as e:
        print(f"  Error en ping a {host}: {e}")
        return float('inf')

def monitoreo_latencia():
    historial = cargar_json(HISTORIAL_PING)
    hosts = ['8.8.8.8', '1.1.1.1', '208.67.222.222']  # Google, Cloudflare, OpenDNS

    print("\n" + "="*50)
    print("         MONITOREO DE LATENCIA DE RED")
    print("="*50)
    print("Midiendo a múltiples servidores DNS...\n")

    resultados = {}
    for host in hosts:
        print(f"  → {host.ljust(15)} ... ", end="")
        latencia = medir_latencia(host)
        if latencia != float('inf'):
            print(f"{latencia:>6.2f} ms")
            resultados[host] = latencia
        else:
            print("falló")

    # Guardar en histórico
    registro = {
        'tiempo': time.strftime('%Y-%m-%d %H:%M:%S'),
        'resultados': {h: float(v) if v != float('inf') else None for h, v in resultados.items()}
    }
    historial.append(registro)
    guardar_json(HISTORIAL_PING, historial)

    # Promedio actual
    latencias_validas = [v for v in resultados.values() if v != float('inf')]
    if latencias_validas:
        print(f"\nPromedio actual: {mean(latencias_validas):.2f} ms")
    else:
        print("\nTodas las mediciones fallaron este turno.")

    # Histórico breve (tolerante a formatos antiguos)
    if len(historial) > 1:
        print("\nÚltimas mediciones válidas:")
        for reg in historial[-3:]:
            tiempo = reg.get('tiempo', 'sin fecha')
            if 'resultados' in reg:
                vals = [v for v in reg['resultados'].values() if v is not None]
            elif 'ping_ms' in reg:
                vals = [reg['ping_ms']] if reg.get('ping_ms') != float('inf') else []
            else:
                vals = []

            if vals:
                print(f"  {tiempo} → {mean(vals):.2f} ms")
            else:
                print(f"  {tiempo} → sin datos válidos")

# ────────────────────────────────────────────────
# 2. OPTIMIZADOR DE RUTAS FIBRA + MAPA
# ────────────────────────────────────────────────

def crear_nodos_ficticios():
    data = pd.DataFrame({
        'nombre': ['NodoA', 'NodoB', 'NodoC', 'NodoD'],
        'lat': [-2.1894, -2.2038, -2.2200, -2.1800],
        'lon': [-79.8892, -79.8975, -79.9000, -79.8800]
    })
    data.to_csv(NODOS_FIBRA_CSV, index=False)
    print(f"Archivo de nodos de ejemplo creado: {NODOS_FIBRA_CSV}")
    print("Puedes editarlo manualmente para agregar tus nodos reales.")

def optimizar_rutas():
    if not os.path.exists(NODOS_FIBRA_CSV):
        crear_nodos_ficticios()

    try:
        df = pd.read_csv(NODOS_FIBRA_CSV)
        df.set_index('nombre', inplace=True)
        puntos = list(df.index)

        if len(puntos) < 2:
            print("Necesitas al menos 2 nodos para calcular rutas.")
            return

        print(f"\nNodos cargados ({len(puntos)}): {', '.join(puntos)}")

        mejor_ruta = None
        min_dist = float('inf')

        max_puntos = min(7, len(puntos))  # 7! = 5040 permutaciones → razonable
        if len(puntos) > max_puntos:
            print(f"Demasiados nodos ({len(puntos)}), limitando a {max_puntos} para rapidez.")
            puntos = puntos[:max_puntos]

        for perm in permutations(range(len(puntos))):
            ruta_idx = list(perm)
            total = 0
            for i in range(len(ruta_idx)-1):
                p1 = (df.iloc[ruta_idx[i]]['lat'], df.iloc[ruta_idx[i]]['lon'])
                p2 = (df.iloc[ruta_idx[i+1]]['lat'], df.iloc[ruta_idx[i+1]]['lon'])
                total += geodesic(p1, p2).km

            if total < min_dist:
                min_dist = total
                mejor_ruta = [puntos[i] for i in ruta_idx]

        print(f"\nMejor ruta encontrada: {' → '.join(mejor_ruta)}")
        print(f"Distancia total aproximada: {min_dist:.2f} km")

        # ── Generar mapa interactivo ──
        try:
            import folium

            centro_lat = df['lat'].mean()
            centro_lon = df['lon'].mean()
            mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=14)

            # Marcadores
            for idx, row in df.iterrows():
                folium.Marker(
                    [row['lat'], row['lon']],
                    popup=idx,
                    tooltip=idx
                ).add_to(mapa)

            # Línea de la ruta óptima
            coords_ruta = [(df.loc[nodo, 'lat'], df.loc[nodo, 'lon']) for nodo in mejor_ruta]
            folium.PolyLine(
                coords_ruta,
                color="blue",
                weight=6,
                opacity=0.9
            ).add_to(mapa)

            mapa.save("ruta_optima_fibra.html")
            print("\n→ Mapa interactivo generado: abre 'ruta_optima_fibra.html' en tu navegador")
            print("   (muestra marcadores y la línea azul de la ruta más corta)")

        except ImportError:
            print("\nfolium no está instalado. Para ver el mapa instala:")
            print("   pip install folium")
        except Exception as e:
            print(f"Error al generar mapa: {e}")

    except Exception as e:
        print(f"Error al procesar nodos: {e}")
        print("Verifica que el CSV tenga columnas: nombre, lat, lon (sin comas en nombres)")

# ────────────────────────────────────────────────
# 3. VALIDADOR DE DATOS GIS
# ────────────────────────────────────────────────

def validar_gis():
    archivo = "nodos_gis.csv"
    if not os.path.exists(archivo):
        print(f"No se encontró {archivo}.")
        print("Crea uno con columnas: nombre,lat,lon")
        print("Ejemplo:")
        print("nombre,lat,lon")
        print("NodoCentral,-2.1894,-79.8892")
        return

    try:
        df = pd.read_csv(archivo)
        print(f"\nValidando {len(df)} registros en {archivo}...")

        df['lat_ok'] = df['lat'].apply(lambda x: isinstance(x, (int, float)) and -90 <= x <= 90)
        df['lon_ok'] = df['lon'].apply(lambda x: isinstance(x, (int, float)) and -180 <= x <= 180)
        df['duplicado'] = df.duplicated(subset=['nombre'], keep=False)

        invalidos = df[~(df['lat_ok'] & df['lon_ok'])]
        duplicados = df[df['duplicado']]

        if invalidos.empty and duplicados.empty:
            print("✓ Todos los datos son válidos.")
        else:
            if not invalidos.empty:
                print(f"✗ Coordenadas inválidas ({len(invalidos)}):")
                print(invalidos[['nombre','lat','lon']].to_string(index=False))
            if not duplicados.empty:
                print(f"⚠ Duplicados encontrados ({len(duplicados)//2} pares):")
                print(duplicados[['nombre']].to_string(index=False))

        # Guardar limpia
        limpia = df[df['lat_ok'] & df['lon_ok']].drop(columns=['lat_ok','lon_ok','duplicado'])
        limpia.to_csv("nodos_gis_limpio.csv", index=False)
        print("→ Versión limpia guardada: nodos_gis_limpio.csv")

    except Exception as e:
        print(f"Error al validar: {e}")

# ────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ────────────────────────────────────────────────

def menu():
    while True:
        print("\n" + "═"*50)
        print("          TELEMATICA TOOLS - Erick Giler 2026")
        print("═"*50)
        print("1. Monitorear latencia de red (ping múltiple)")
        print("2. Optimizar rutas de fibra óptica + mapa")
        print("3. Validar y limpiar datos GIS (CSV)")
        print("4. Salir")
        print("─"*50)

        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == '1':
            monitoreo_latencia()
        elif opcion == '2':
            optimizar_rutas()
        elif opcion == '3':
            validar_gis()
        elif opcion == '4':
            print("\n¡Gracias por usar TelematicaTools! 🚀")
            print("Sube este proyecto a GitHub para tu portafolio.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()