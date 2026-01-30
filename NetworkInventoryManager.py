# NetworkInventoryManager.py - Gestor de Inventario de Equipos de Red
# Autor: Erick Giler Veintimilla - Proyecto personal 2026
# Ideal para gestión de inventarios en telecomunicaciones (routers, switches, fibra, etc.)

import json
import os
from datetime import datetime

# Archivo donde se guarda el inventario
INVENTARIO_JSON = "inventario_red.json"

# ────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ────────────────────────────────────────────────

def cargar_inventario():
    if os.path.exists(INVENTARIO_JSON):
        try:
            with open(INVENTARIO_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_inventario(inventario):
    with open(INVENTARIO_JSON, 'w', encoding='utf-8') as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)
    print(f"  Inventario guardado en {INVENTARIO_JSON}")

# ────────────────────────────────────────────────
# FUNCIONES PRINCIPALES
# ────────────────────────────────────────────────

def agregar_equipo(inventario):
    print("\nAgregar nuevo equipo:")
    nombre = input("  Nombre del equipo (ej: Router Cisco 2911): ").strip().title()
    if not nombre:
        print("  Nombre requerido.")
        return

    # Verificar si ya existe
    if nombre in inventario:
        print(f"  El equipo '{nombre}' ya existe. ¿Editar cantidad? (s/n)")
        if input("  → ").lower() != 's':
            return
        cantidad = int(input(f"  Nueva cantidad para '{nombre}': "))
    else:
        cantidad = int(input("  Cantidad: "))
        if cantidad < 1:
            print("  Cantidad debe ser positiva.")
            return

    tipo = input("  Tipo (ej: Router, Switch, Cable Fibra, Nodo): ").strip().title()
    ubicacion = input("  Ubicación (ej: Bodega Durán, Sitio Guayaquil): ").strip()

    inventario[nombre] = {
        'cantidad': cantidad,
        'tipo': tipo,
        'ubicacion': ubicacion,
        'fecha_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    print(f"  '{nombre}' agregado/actualizado con {cantidad} unidades.")

def listar_inventario(inventario):
    if not inventario:
        print("\n  No hay equipos en el inventario.")
        return

    print("\n" + "="*60)
    print("          INVENTARIO DE EQUIPOS DE RED")
    print("="*60)
    print(f"{'Equipo':<35} {'Cant.':<6} {'Tipo':<15} {'Ubicación':<20} {'Últ. Act.':<16}")
    print("-"*60)

    total_equipos = 0
    for nombre, datos in inventario.items():
        print(f"{nombre:<35} {datos['cantidad']:<6} {datos['tipo']:<15} {datos['ubicacion']:<20} {datos['fecha_actualizacion']:<16}")
        total_equipos += datos['cantidad']

    print("-"*60)
    print(f"Total de equipos: {total_equipos}")
    print(f"Total de tipos únicos: {len(inventario)}")

def buscar_equipo(inventario):
    busqueda = input("\nBuscar equipo (nombre o parte del nombre): ").strip().lower()
    encontrados = {k: v for k, v in inventario.items() if busqueda in k.lower()}

    if not encontrados:
        print("  No se encontraron coincidencias.")
        return

    print("\nResultados de búsqueda:")
    for nombre, datos in encontrados.items():
        print(f"  {nombre}: {datos['cantidad']} unidades | Tipo: {datos['tipo']} | Ubicación: {datos['ubicacion']}")

def editar_equipo(inventario):
    nombre = input("\nNombre del equipo a editar: ").strip().title()
    if nombre not in inventario:
        print("  Equipo no encontrado.")
        return

    print(f"  Equipo actual: {nombre}")
    print(f"    Cantidad: {inventario[nombre]['cantidad']}")
    print(f"    Tipo: {inventario[nombre]['tipo']}")
    print(f"    Ubicación: {inventario[nombre]['ubicacion']}")

    nuevo_cant = input("  Nueva cantidad (Enter para mantener): ")
    if nuevo_cant:
        try:
            inventario[nombre]['cantidad'] = int(nuevo_cant)
        except:
            print("  Cantidad inválida, se mantiene la anterior.")

    nuevo_tipo = input("  Nuevo tipo (Enter para mantener): ").strip().title()
    if nuevo_tipo:
        inventario[nombre]['tipo'] = nuevo_tipo

    nuevo_ub = input("  Nueva ubicación (Enter para mantener): ").strip()
    if nuevo_ub:
        inventario[nombre]['ubicacion'] = nuevo_ub

    inventario[nombre]['fecha_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("  Equipo actualizado.")

def eliminar_equipo(inventario):
    nombre = input("\nNombre del equipo a eliminar: ").strip().title()
    if nombre in inventario:
        confirm = input(f"  ¿Eliminar '{nombre}'? (s/n): ").lower()
        if confirm == 's':
            del inventario[nombre]
            print("  Equipo eliminado.")
    else:
        print("  Equipo no encontrado.")

# ────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ────────────────────────────────────────────────

def menu():
    inventario = cargar_inventario()
    print("\nBienvenido a NetworkInventoryManager - Erick Giler 2026")

    while True:
        print("\n" + "═"*50)
        print("          GESTOR DE INVENTARIO DE RED")
        print("═"*50)
        print("1. Agregar / Actualizar equipo")
        print("2. Listar todo el inventario")
        print("3. Buscar equipo")
        print("4. Editar equipo")
        print("5. Eliminar equipo")
        print("6. Salir")
        print("─"*50)

        opcion = input("Elige una opción (1-6): ").strip()

        if opcion == '1':
            agregar_equipo(inventario)
        elif opcion == '2':
            listar_inventario(inventario)
        elif opcion == '3':
            buscar_equipo(inventario)
        elif opcion == '4':
            editar_equipo(inventario)
        elif opcion == '5':
            eliminar_equipo(inventario)
        elif opcion == '6':
            guardar_inventario(inventario)
            print("\n¡Gracias por usar NetworkInventoryManager! 🚀")
            print("Guarda este proyecto en tu GitHub para tu CV.")
            break
        else:
            print("Opción no válida.")

        # Guardar automáticamente después de cada acción (excepto salir)
        if opcion != '6':
            guardar_inventario(inventario)

if __name__ == "__main__":
    menu()