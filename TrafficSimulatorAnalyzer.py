# TrafficSimulatorAnalyzer.py - Simulador y Analizador de Tráfico en Redes de Fibra
# Autor: Erick Giler Veintimilla - Proyecto personal 2026

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración global
NUM_NODOS = 6
CAPACIDAD_LINK_KBPS = 10000
TIEMPO_SIMULACION_S = 300
TASA_LLEGADA_PAQ_SEG = 800
TAMANO_PAQ_BYTES = 1500
NUM_SIMULACIONES = 5

ARCHIVO_RESULTADOS = "resultados_trafico.csv"
REPORTE_TXT = "reporte_trafico.txt"

# ────────────────────────────────────────────────
# SIMULACIÓN PRINCIPAL
# ────────────────────────────────────────────────
def simular_red():
    print(f"\nIniciando simulación ({NUM_SIMULACIONES} corridas de {TIEMPO_SIMULACION_S} s)...")
    
    resultados = []
    historial_latencia = []
    historial_congestion = []

    for corrida in range(1, NUM_SIMULACIONES + 1):
        print(f"  Corrida {corrida}/{NUM_SIMULACIONES}... ", end="")

        paquetes_en_cola = 0
        paquetes_perdidos = 0
        latencias = []
        congestiones = []

        capacidad_seg = (CAPACIDAD_LINK_KBPS * 1000 / 8) / TAMANO_PAQ_BYTES

        for t in range(TIEMPO_SIMULACION_S):
            llegadas = np.random.poisson(TASA_LLEGADA_PAQ_SEG)
            procesados = min(paquetes_en_cola + llegadas, int(capacidad_seg + 0.999))

            paquetes_en_cola = paquetes_en_cola + llegadas - procesados

            buffer_max = int(capacidad_seg * 10)
            if paquetes_en_cola > buffer_max:
                paquetes_perdidos += paquetes_en_cola - buffer_max
                paquetes_en_cola = buffer_max

            latencia_ms = (paquetes_en_cola / capacidad_seg * 1000) + \
                          (TAMANO_PAQ_BYTES * 8 / (CAPACIDAD_LINK_KBPS * 1000)) * 1000 \
                          if capacidad_seg > 0 else 0
            latencias.append(latencia_ms)

            utilizacion = ((llegadas + paquetes_en_cola) / capacidad_seg * 100) if capacidad_seg > 0 else 0
            congestiones.append(min(utilizacion, 100))

        latencia_prom = np.mean(latencias) if latencias else 0
        utilizacion_prom = np.mean(congestiones) if congestiones else 0
        paquetes_totales = TASA_LLEGADA_PAQ_SEG * TIEMPO_SIMULACION_S
        throughput = (TASA_LLEGADA_PAQ_SEG * TAMANO_PAQ_BYTES * 8 / 1000) * \
                     (1 - (paquetes_perdidos / paquetes_totales if paquetes_totales > 0 else 0))

        resultados.append({
            'corrida': corrida,
            'latencia_prom_ms': round(latencia_prom, 2),
            'utilizacion_prom_%': round(utilizacion_prom, 2),
            'paquetes_perdidos': paquetes_perdidos,
            'throughput_kbps': round(throughput, 2)
        })

        historial_latencia.append(latencias)
        historial_congestion.append(congestiones)

        print(f"Latencia avg: {latencia_prom:.1f} ms | Utilización: {utilizacion_prom:.1f}%")

    df_resultados = pd.DataFrame(resultados)
    return df_resultados, historial_latencia, historial_congestion

# ────────────────────────────────────────────────
# VISUALIZACIÓN
# ────────────────────────────────────────────────
def graficar_resultados(historial_latencia, historial_congestion):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    for i, lat in enumerate(historial_latencia):
        plt.plot(lat, alpha=0.6, label=f'Corrida {i+1}')
    plt.title("Evolución de Latencia por Corrida")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Latencia (ms)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.subplot(1, 2, 2)
    for i, cong in enumerate(historial_congestion):
        plt.plot(cong, alpha=0.6, label=f'Corrida {i+1}')
    plt.title("Evolución de Utilización")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Utilización (%)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig("grafico_trafico.png")
    plt.close()
    print("  Gráfico generado: 'grafico_trafico.png'")

# ────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ────────────────────────────────────────────────
def menu():
    global NUM_NODOS, CAPACIDAD_LINK_KBPS, TASA_LLEGADA_PAQ_SEG, TAMANO_PAQ_BYTES, TIEMPO_SIMULACION_S, NUM_SIMULACIONES
    # ↑↑↑ Esta línea SOLO aquí, al inicio de la función, permite leer las variables globales en todo el menú

    print("\nBienvenido a TrafficSimulatorAnalyzer - Erick Giler 2026")
    print("Simulador de tráfico en redes de fibra óptica\n")

    while True:
        print("\n" + "═"*50)
        print("1. Ejecutar simulación completa")
        print("2. Ver configuración actual")
        print("3. Cambiar parámetros")
        print("4. Salir")
        print("─"*50)

        opcion = input("Elige (1-4): ").strip()

        if opcion == '1':
            df_res, hist_lat, hist_cong = simular_red()
            print("\nResumen:")
            print(df_res.to_string(index=False))

            df_res.to_csv(ARCHIVO_RESULTADOS, index=False)
            print(f"  Guardado: {ARCHIVO_RESULTADOS}")

            graficar_resultados(hist_lat, hist_cong)

            with open(REPORTE_TXT, 'w', encoding='utf-8') as f:
                f.write(f"Reporte - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write(df_res.to_string(index=False))
                f.write("\nConfiguración:\n")
                f.write(f"- Nodos: {NUM_NODOS}\n")
                f.write(f"- Capacidad: {CAPACIDAD_LINK_KBPS} kbps\n")
                f.write(f"- Tasa llegada: {TASA_LLEGADA_PAQ_SEG} paq/s\n")
                f.write(f"- Duración: {TIEMPO_SIMULACION_S} s\n")
                f.write(f"- Corridas: {NUM_SIMULACIONES}\n")

            print(f"  Reporte: {REPORTE_TXT}")

        elif opcion == '2':
            print("\nConfiguración:")
            print(f"  Nodos: {NUM_NODOS}")
            print(f"  Capacidad: {CAPACIDAD_LINK_KBPS} kbps")
            print(f"  Tasa llegada: {TASA_LLEGADA_PAQ_SEG} paq/s")
            print(f"  Tamaño paquete: {TAMANO_PAQ_BYTES} bytes")
            print(f"  Duración: {TIEMPO_SIMULACION_S} s")
            print(f"  Corridas: {NUM_SIMULACIONES}")

        elif opcion == '3':
            print("\nCambiar parámetros (Enter = mantener):")

            n = input(f"  Nodos ({NUM_NODOS}): ").strip()
            if n:
                try: NUM_NODOS = int(n)
                except: print("  Valor inválido")

            cap = input(f"  Capacidad kbps ({CAPACIDAD_LINK_KBPS}): ").strip()
            if cap:
                try: CAPACIDAD_LINK_KBPS = int(cap)
                except: print("  Valor inválido")

            tasa = input(f"  Tasa paq/s ({TASA_LLEGADA_PAQ_SEG}): ").strip()
            if tasa:
                try: TASA_LLEGADA_PAQ_SEG = int(tasa)
                except: print("  Valor inválido")

            tam = input(f"  Tamaño paquete bytes ({TAMANO_PAQ_BYTES}): ").strip()
            if tam:
                try: TAMANO_PAQ_BYTES = int(tam)
                except: print("  Valor inválido")

            dur = input(f"  Duración s ({TIEMPO_SIMULACION_S}): ").strip()
            if dur:
                try: TIEMPO_SIMULACION_S = int(dur)
                except: print("  Valor inválido")

            corr = input(f"  Corridas ({NUM_SIMULACIONES}): ").strip()
            if corr:
                try: NUM_SIMULACIONES = int(corr)
                except: print("  Valor inválido")

            print("  Parámetros actualizados.")

        elif opcion == '4':
            print("\n¡Gracias! 🚀")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()