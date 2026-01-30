from ping3 import ping
import json
import time
from statistics import mean

def medir_ping(host='8.8.8.8'):
    try:
        delay = ping(host, unit='ms', timeout=4)
        if delay is not None:
            return delay
        else:
            print(f"Ping a {host} falló (timeout o no responde)")
            return float('inf')
    except Exception as e:
        print(f"Error en ping: {e}")
        return float('inf')

def cargar_historial(archivo):
    try:
        with open(archivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_historial(archivo, historial, nuevo_ping, host):
    historial.append({'tiempo': time.strftime('%Y-%m-%d %H:%M:%S'), 'ping_ms': nuevo_ping, 'host': host})
    with open(archivo, 'w') as f:
        json.dump(historial, f, indent=2)

archivo_json = "historial_ping.json"
historial = cargar_historial(archivo_json)

print("Monitor de latencia de red (ping3) - Ctrl+C para salir")

while True:
    try:
        opcion = input("\n1: Medir ping   2: Ver histórico   3: Salir\n→ ").strip()
        if opcion == '1':
            host = '8.8.8.8'
            print(f"Midiendo ping a {host}...")
            ping_val = medir_ping(host)
            if ping_val != float('inf'):
                print(f"✓ Latencia: {ping_val:.2f} ms")
            else:
                print("✗ Falló. Probando 1.1.1.1...")
                ping_val = medir_ping('1.1.1.1')
                if ping_val != float('inf'):
                    print(f"✓ Latencia alternativa: {ping_val:.2f} ms")
                else:
                    print("✗ Ambos fallaron. Revisa conexión.")
            guardar_historial(archivo_json, historial, ping_val, host)
        
        elif opcion == '2':
            if historial:
                print("\nHistórico reciente:")
                for entry in historial[-10:]:
                    ms = entry['ping_ms']
                    host = entry.get('host', 'desconocido')
                    status = f"{ms:.2f} ms" if ms != float('inf') else "inf (falló)"
                    print(f"  {entry['tiempo']} | {status} | {host}")
                
                validos = [h['ping_ms'] for h in historial if h['ping_ms'] != float('inf')]
                if validos:
                    print(f"\nPromedio de mediciones válidas: {mean(validos):.2f} ms")
                else:
                    print("No hay mediciones válidas aún.")
            else:
                print("Aún no hay registros.")
        
        elif opcion == '3':
            print("¡Hasta la próxima!")
            break
        
        else:
            print("Opción inválida.")
    
    except KeyboardInterrupt:
        print("\nSaliendo...")
        break