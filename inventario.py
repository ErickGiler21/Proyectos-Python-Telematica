inventario = {}  # Ej: {'router': 5, 'cable': 10}

def agregar(item, cantidad):
    if item in inventario:
        inventario[item] += cantidad
    else:
        inventario[item] = cantidad

# Menú simple
while True:
    opcion = input("1: Agregar, 2: Listar, 3: Salir: ")
    if opcion == '1':
        item = input("Item: ")
        cant = int(input("Cantidad: "))
        agregar(item, cant)
    elif opcion == '2':
        print(inventario)
    elif opcion == '3':
        break