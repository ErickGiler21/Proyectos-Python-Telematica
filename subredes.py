def calcular_subred(ip, mascara):
    # Código simple para split y cálculos básicos
    partes_ip = ip.split('.')
    print(f"Rango aproximado: {partes_ip[0]}.{partes_ip[1]}.{partes_ip[2]}.0 a {partes_ip[0]}.{partes_ip[1]}.{partes_ip[2]}.255 (para máscara /24)")

ip = input("Ingresa una IP (ej: 192.168.1.0): ")
mascara = input("Ingresa la máscara (ej: 24): ")
calcular_subred(ip, mascara)