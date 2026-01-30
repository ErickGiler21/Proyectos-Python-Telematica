print("Generador simple de rango de IPs en subred /24")
ip_base = input("Ingresa IP base (ej: 192.168.1.0): ")

partes = ip_base.split('.')
if len(partes) != 4:
    print("IP inválida")
else:
    red = partes[0] + '.' + partes[1] + '.' + partes[2] + '.'
    print(f"Red: {red}0")
    print(f"Primera IP usable: {red}1")
    print(f"Última IP usable: {red}254")
    print(f"Broadcast: {red}255")