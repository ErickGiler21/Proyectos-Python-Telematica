import os

def ping(ip):
    response = os.system(f"ping -c 1 {ip} > /dev/null")  # Para Linux/Mac; usa -n 1 para Windows
    if response == 0:
        print(f"{ip} está activo!")
    else:
        print(f"{ip} no responde.")

ip = input("Ingresa IP o sitio (ej: google.com): ")
ping(ip)