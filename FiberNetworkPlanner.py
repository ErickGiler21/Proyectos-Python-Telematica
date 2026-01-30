# TrafficSimulatorAnalyzer.py - Simulador y Analizador de Tráfico en Redes de Fibra
# Autor: Erick Giler Veintimilla - Proyecto personal 2026
# Simula tráfico de paquetes, congestión y latencia en una red de nodos

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configuración global (ajusta estos valores según necesites)
NUM_NODOS = 6                      # Número de nodos en la red (anillo o línea)
CAPACIDAD_LINK_KBPS = 10000        # Capacidad por enlace (10 Mbps)
TIEMPO_SIMULACION_S = 300          # Duración de cada simulación (segundos)
TASA_LLEGADA_PAQ_SEG = 800         # Paquetes por segundo promedio (Poisson)
TAMANO_PAQ_BYTES = 1500            # Tamaño promedio de paquete
NUM_SIMULACIONES = 5               # Corridas Monte Carlo

ARCHIVO_RESULTADOS = "resultados_trafico.csv"
REPORTE_TXT = "reporte_trafico.txt"

# ────────────────────────────────────────────────
# SIMULACIÓN PRINCIPAL
# ────────────────────────────────────────────────
def simular_red():
    print(f"\nIniciando simulación ({NUM_SIMULACIONES} corridas de {TIEMPO_SIMULACION_S} segundos)...")
    
    resultados = []
    historial_latencia = []
    historial_congestion = []

    for corrida in range(1, NUM_SIMULACIONES + 1):
        print(f"  Corrida {corrida}/{NUM_SIMULACIONES}... ", end="")

        # Variables de estado
        paquetes_en_cola = 0
        paquetes_perdidos = 0
        latencias = []
        congestiones = []

        # Capacidad en paquetes por segundo
        capacidad_seg = (CAPACIDAD_LINK_KBPS * 1000 / 8) / TAMANO_PAQ_BYTES

        # Simulación por segundo
        for t in range(TIEMPO_SIMULACION_S):
            # Llegada de paquetes (Poisson)
            llegadas = np.random.poisson(TASA_LLEGADA_PAQ_SEG)

            # Procesamiento
            procesados = min(paquetes_en_cola + llegadas, int(capacidad_seg + 0.999))  # redondeo hacia arriba

            # Actualizar cola
            paquetes_en_cola = paquetes_en_cola + llegadas - procesados

            # Pérdidas si excede buffer (simplificado)
            buffer_max = int(capacidad_seg * 10)  # Umbral de congestión
            if paquetes_en_cola > buffer_max:
                paquetes_perdidos += paquetes_en_cola - buffer_max
                paquetes_en_cola = buffer_max

            # Latencia aproximada (cola + transmisión)
            if capacidad_seg > 0:
                latencia_ms = (paquetes_en_cola / capacidad_seg) * 1000 + \
                              (TAMANO_PAQ_BYTES * 8 / (CAPACIDAD_LINK_KBPS * 1000)) * 1000
            else:
                latencia_ms = 0

            latencias.append(latencia_ms)

            # Congestión (% utilización)
            utilizacion = ((llegadas + paquetes_en_cola) / capacidad_seg * 100) if capacidad_seg > 0 else 0
            congestiones.append(min(utilizacion, 100))

        # Resultados de la corrida
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
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Latencia (ms)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.subplot(1, 2, 2)
    for i, cong in enumerate(historial_congestion):
        plt.plot(cong, alpha=0.6, label=f'Corrida {i+1}')
    plt.title("Evolución de Utilización / Congestión")
    plt.xlabel("Tiempo (segundos)")
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
    print("\nBienvenido a TrafficSimulatorAnalyzer - Erick Giler 2026\n")
    print("Simulador de tráfico en redes de fibra óptica\n")

    while True:
        print("\n" + "═"*60)
        print("          SIMULADOR DE TRÁFICO DE RED")
        print("═"*60)
        print("1. Ejecutar simulación completa")
        print("2. Ver configuración actual")
        print("3. Cambiar parámetros (avanzado)")
        print("4. Salir")
        print("─"*60)

        opcion = input("Elige (1-4): ").strip()

        if opcion == '1':
            df_res, hist_lat, hist_cong = simular_red()
            print("\nResumen de simulaciones:")
            print(df_res.to_string(index=False))

            # Guardar CSV
            df_res.to_csv(ARCHIVO_RESULTADOS, index=False)
            print(f"  Resultados guardados en {ARCHIVO_RESULTADOS}")

            # Gráfico
            graficar_resultados(hist_lat, hist_cong)

            # Reporte TXT
            with open(REPORTE_TXT, 'w', encoding='utf-8') as f:
                f.write(f"Reporte de Simulación de Tráfico - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write(df_res.to_string(index=False))
                f.write(f"\n\nConfiguración utilizada:\n")
                f.write(f"- Nodos: {NUM_NODOS}\n")
                f.write(f"- Capacidad por enlace: {CAPACIDAD_LINK_KBPS} kbps\n")
                f.write(f"- Tasa llegada: {TASA_LLEGADA_PAQ_SEG} paq/s\n")
                f.write(f"- Duración: {TIEMPO_SIMULACION_S} s\n")
                f.write(f"- Corridas: {NUM_SIMULACIONES}\n")

            print(f"  Reporte TXT generado: {REPORTE_TXT}")

        elif opcion == '2':
            print("\nConfiguración actual:")
            print(f"  Nodos en red: {NUM_NODOS}")
            print(f"  Capacidad por enlace: {CAPACIDAD_LINK_KBPS} kbps")
            print(f"  Tasa llegada paquetes: {TASA_LLEGADA_PAQ_SEG} paq/s")
            print(f"  Tamaño paquete: {TAMANO_PAQ_BYTES} bytes")
            print(f"  Duración simulación: {TIEMPO_SIMULACION_S} s")
            print(f"  Corridas Monte Carlo: {NUM_SIMULACIONES}")

        elif opcion == '3':
            print("\nCambiar parámetros (presiona Enter para mantener):")

            n = input(f"  Nodos ({NUM_NODOS}): ").strip()
            if n: 
                try:
                    NUM_NODOS = int(n)
                except:
                    print("  Valor inválido, se mantiene el anterior.")

            cap = input(f"  Capacidad kbps ({CAPACIDAD_LINK_KBPS}): ").strip()
            if cap: 
                try:
                    CAPACIDAD_LINK_KBPS = int(cap)
                except:
                    print("  Valor inválido, se mantiene el anterior.")

            tasa = input(f"  Tasa llegada paq/s ({TASA_LLEGADA_PAQ_SEG}): ").strip()
            if tasa: 
                try:
                    TASA_LLEGADA_PAQ_SEG = int(tasa)
                except:
                    print("  Valor inválido, se mantiene el anterior.")

            tam = input(f"  Tamaño paquete bytes ({TAMANO_PAQ_BYTES}): ").strip()
            if tam: 
                try:
                    TAMANO_PAQ_BYTES = int(tam)
                except:
                    print("  Valor inválido, se mantiene el anterior.")

            dur = input(f"  Duración s ({TIEMPO_SIMULACION_S}): ").strip()
            if dur: 
                try:
                    TIEMPO_SIMULACION_S = int(dur)
                except:
                    print("  Valor inválido, se mantiene el anterior.")

            corr = input(f"  Corridas ({NUM_SIMULACIONES}): ").strip()
            if corr: 
                try:
                    NUM_SIMULACIONES = int(corr)
                except:
                    print("  Valor inválido, se mantiene el anterior.")

            print("  Parámetros actualizados.")

        elif opcion == '4':
            print("\n¡Gracias por usar TrafficSimulatorAnalyzer! 🚀")
            print("Sube este script a GitHub para mostrar tus habilidades en simulación de redes.")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()