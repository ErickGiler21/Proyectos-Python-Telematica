inventario = {}

print("Contador de equipos de telecomunicaciones")
print("Escribe 'salir' para terminar")

while True:
    equipo = input("\nEquipo a agregar (ej: router, switch, cable): ").lower()
    if equipo == 'salir':
        break
    if equipo in inventario:
        inventario[equipo] += 1
    else:
        inventario[equipo] = 1
    print(f"Agregado 1 {equipo}. Total ahora: {inventario.get(equipo, 0)}")

print("\nInventario final:")
for eq, cant in inventario.items():
    print(f"{eq.capitalize()}: {cant}")