# RedesBasicasTools.py - Herramientas básicas de redes para telemática
# Autor: Erick Giler Veintimilla - Proyecto personal 2026

import ipaddress
import subprocess
import time
import sys
from typing import List

# ────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ────────────────────────────────────────────────

def ejecutar_ping(host: str) -> str:
    """Realiza ping a un host y devuelve resultado simple"""
    try:
        # Windows usa -n, Linux/Mac usa -c
        param = '-n' if sys.platform.lower().startswith('win') else '-c'
        output = subprocess.check_output(
            ["ping", param, "3", host],
            stderr=subprocess.STDOUT,
            timeout=10
        ).decode('utf-8', errors='ignore')
        
        if "TTL=" in output or "tiempo=" in output or "time=" in output:
            return "OK"
        return "FALLÓ"
    except Exception:
        return "FALLÓ"

def guardar_resultados(nombre_archivo: str, contenido: str):
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"\nResultados guardados en: {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar: {e}")

# ────────────────────────────────────────────────
# 1. CALCULADORA DE SUBREDES IPv4
# ────────────────────────────────────────────────

def calculadora_subredes():
    print("\n=== Calculadora de Subredes IPv4 ===")
    try:
        red = input("Ingresa red en CIDR (ej: 192.168.1.0/24): ").strip()
        network = ipaddress.ip_network(red, strict=False)
        
        print(f"\nRed: {network.network_address}")
        print(f"Máscara: {network.netmask}  /{network.prefixlen}")
        print(f"Primera IP usable: {network.network_address + 1}")
        print(f"Última IP usable: {network.broadcast_address - 1}")
        print(f"Broadcast: {network.broadcast_address}")
        print(f"Número de hosts: {network.num_addresses - 2}")
        print(f"Tipo: {'Privada' if network.is_private else 'Pública'}")
        
        # Preguntar si guardar
        if input("\n¿Guardar resultado en txt? (s/n): ").lower().startswith('s'):
            guardar_resultados("subred.txt", f"Red: {network}\n{str(network).center(40, '=')}\n" + 
                              f"Primera usable: {network.network_address + 1}\n" +
                              f"Última usable: {network.broadcast_address - 1}\n" +
                              f"Broadcast: {network.broadcast_address}\n" +
                              f"Hosts: {network.num_addresses - 2}\n")
            
    except ValueError as e:
        print(f"Error: Formato inválido - {e}")

# ────────────────────────────────────────────────
# 2. PING MASIVO A LISTA DE HOSTS
# ────────────────────────────────────────────────

def ping_masivo():
    print("\n=== Ping Masivo ===")
    print("Ingresa hosts/IPs (uno por línea, vacío para terminar)")
    hosts: List[str] = []
    
    while True:
        host = input("Host/IP: ").strip()
        if not host:
            break
        hosts.append(host)
    
    if not hosts:
        print("No ingresaste ningún host.")
        return
    
    print("\nResultados:")
    print("-"*50)
    print(f"{'Host':<20} {'Estado':<10} {'Hora':<20}")
    print("-"*50)
    
    resultados = []
    for host in hosts:
        estado = ejecutar_ping(host)
        hora = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{host:<20} {estado:<10} {hora}")
        resultados.append(f"{hora} | {host} | {estado}")
    
    if input("\n¿Guardar resultados? (s/n): ").lower().startswith('s'):
        guardar_resultados("ping_masivo.txt", "\n".join(resultados))

# ────────────────────────────────────────────────
# 3. GENERADOR DE RANGOS PRIVADOS / PÚBLICOS
# ────────────────────────────────────────────────

def generador_ips():
    print("\n=== Generador de Rangos IP ===")
    print("1. Rangos privados comunes")
    print("2. Generar IPs privadas aleatorias (ej: 192.168.x.x)")
    print("3. Volver")
    
    opcion = input("\nElige (1-3): ").strip()
    
    if opcion == '1':
        print("\nRangos privados IPv4 (RFC 1918):")
        print("10.0.0.0      - 10.255.255.255     (16,777,216 hosts)")
        print("172.16.0.0    - 172.31.255.255     (1,048,576 hosts)")
        print("192.168.0.0   - 192.168.255.255    (65,536 hosts)")
        print("127.0.0.0     - 127.255.255.255    (loopback)")
    
    elif opcion == '2':
        try:
            cantidad = int(input("¿Cuántas IPs generar? (máx 20): "))
            cantidad = min(max(cantidad, 1), 20)
            segmento = input("Segmento base (ej: 192.168.10): ").strip()
            
            print("\nIPs generadas:")
            for i in range(1, cantidad + 1):
                ip = f"{segmento}.{i}"
                print(ip)
        except ValueError:
            print("Cantidad inválida. Usando 5 por defecto.")
            for i in range(1, 6):
                print(f"192.168.10.{i}")

# ────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ────────────────────────────────────────────────

def menu():
    while True:
        print("\n" + "═"*50)
        print("      REDES BASICAS TOOLS - Erick Giler 2026")
        print("═"*50)
        print("1. Calculadora de subredes IPv4")
        print("2. Ping masivo a lista de hosts")
        print("3. Generador de rangos IP")
        print("4. Salir")
        print("─"*50)

        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == '1':
            calculadora_subredes()
        elif opcion == '2':
            ping_masivo()
        elif opcion == '3':
            generador_ips()
        elif opcion == '4':
            print("\n¡Gracias por usar RedesBasicasTools!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()