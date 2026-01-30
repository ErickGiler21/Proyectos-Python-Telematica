import pandas as pd

def validar_lat_lon(valor):
    try:
        val = float(valor)
        return -90 <= val <= 90 if 'lat' in str(valor) else -180 <= val <= 180
    except ValueError:
        return False

def validar_datos(df):
    errores = []
    # Validar duplicados
    duplicados = df[df.duplicated(subset=['nombre'], keep=False)]
    if not duplicados.empty:
        errores.append(f"Duplicados encontrados: {duplicados['nombre'].tolist()}")

    # Validar lat/lon
    invalidos = df[~df.apply(lambda row: validar_lat_lon(row['lat']) and validar_lat_lon(row['lon']), axis=1)]
    if not invalidos.empty:
        errores.append(f"Coordenadas inválidas en: {invalidos['nombre'].tolist()}")

    return errores

archivo_entrada = "nodos_gis.csv"
archivo_salida = "nodos_limpios.csv"

try:
    df = pd.read_csv(archivo_entrada)
    errores = validar_datos(df)

    if errores:
        print("Errores encontrados:")
        for err in errores:
            print(err)
        # Corrección simple: eliminar duplicados
        df = df.drop_duplicates(subset=['nombre'])
        print("Duplicados eliminados automáticamente.")
    else:
        print("Datos válidos.")

    df.to_csv(archivo_salida, index=False)
    print(f"Datos validados y guardados en {archivo_salida}")
except FileNotFoundError:
    print(f"Error: {archivo_entrada} no encontrado. Crea un CSV con columnas: nombre, lat, lon.")
except Exception as e:
    print(f"Error: {e}")