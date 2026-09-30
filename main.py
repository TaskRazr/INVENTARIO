"""
main.py
Interfaz de consola (CLI) para el sistema de gestión de inventario del
laboratorio de electrónica. Punto de entrada de la aplicación en modo texto.

Ejecutar con:
    python main.py
"""

from inventario import Inventario
from modelos import ComponenteElectronico, Herramienta, InstrumentoMedicion


def menu():
    print("\n" + "=" * 55)
    print(" INVENTARIO - LABORATORIO DE ELECTRONICA")
    print("=" * 55)
    print("1. Registrar componente electrónico")
    print("2. Registrar herramienta")
    print("3. Registrar instrumento de medición")
    print("4. Listar todos los elementos")
    print("5. Buscar por ID")
    print("6. Buscar por categoría")
    print("7. Buscar por nombre")
    print("8. Actualizar cantidad")
    print("9. Eliminar elemento")
    print("10. Reporte de bajo stock")
    print("0. Salir")
    print("=" * 55)


def pedir(texto, default=None):
    valor = input(f"{texto}{' [' + str(default) + ']' if default is not None else ''}: ").strip()
    return valor if valor else default


def registrar_electronico(inv):
    print("\n--- Nuevo componente electrónico ---")
    id_c = pedir("ID")
    nombre = pedir("Nombre")
    categoria = pedir("Categoría (ej: Resistencias, Capacitores, ICs)")
    cantidad = int(pedir("Cantidad", 0))
    ubicacion = pedir("Ubicación (ej: Gaveta A3)")
    descripcion = pedir("Descripción", "")
    tipo_e = pedir("Tipo (ej: Resistencia, Capacitor, IC)", "N/A")
    voltaje = float(pedir("Voltaje de operación", 0.0))

    comp = ComponenteElectronico(id_c, nombre, categoria, cantidad, ubicacion,
                                  descripcion, tipo_e, voltaje)
    if inv.agregar_componente(comp):
        print("✔ Componente registrado y guardado en inventario.txt")
    else:
        print("✘ Ya existe un elemento con ese ID.")


def registrar_herramienta(inv):
    print("\n--- Nueva herramienta ---")
    id_c = pedir("ID")
    nombre = pedir("Nombre")
    categoria = pedir("Categoría (ej: Manual, Eléctrica)")
    cantidad = int(pedir("Cantidad", 0))
    ubicacion = pedir("Ubicación")
    descripcion = pedir("Descripción", "")
    estado = pedir("Estado (Bueno/Regular/Malo)", "Bueno")

    comp = Herramienta(id_c, nombre, categoria, cantidad, ubicacion,
                        descripcion, estado)
    if inv.agregar_componente(comp):
        print("✔ Herramienta registrada y guardada en inventario.txt")
    else:
        print("✘ Ya existe un elemento con ese ID.")


def registrar_instrumento(inv):
    print("\n--- Nuevo instrumento de medición ---")
    id_c = pedir("ID")
    nombre = pedir("Nombre")
    categoria = pedir("Categoría (ej: Medición, Generación)")
    cantidad = int(pedir("Cantidad", 0))
    ubicacion = pedir("Ubicación")
    descripcion = pedir("Descripción", "")
    calibrado = pedir("¿Calibrado? (si/no)", "si").lower() in ("si", "sí", "s")
    fecha_cal = pedir("Fecha de última calibración (YYYY-MM-DD)", "N/A")

    comp = InstrumentoMedicion(id_c, nombre, categoria, cantidad, ubicacion,
                                descripcion, calibrado, fecha_cal)
    if inv.agregar_componente(comp):
        print("✔ Instrumento registrado y guardado en inventario.txt")
    else:
        print("✘ Ya existe un elemento con ese ID.")


def mostrar_lista(lista):
    if not lista:
        print("(sin resultados)")
        return
    for c in lista:
        print(" -", c)


def main():
    inv = Inventario("inventario.txt")

    while True:
        menu()
        opcion = pedir("Elige una opción")

        if opcion == "1":
            registrar_electronico(inv)
        elif opcion == "2":
            registrar_herramienta(inv)
        elif opcion == "3":
            registrar_instrumento(inv)
        elif opcion == "4":
            print("\n--- Inventario completo ---")
            mostrar_lista(inv.listar_todos())
        elif opcion == "5":
            id_c = pedir("ID a buscar")
            comp = inv.buscar_por_id(id_c)
            print(comp if comp else "No encontrado.")
        elif opcion == "6":
            cat = pedir("Categoría")
            mostrar_lista(inv.buscar_por_categoria(cat))
        elif opcion == "7":
            texto = pedir("Texto a buscar en el nombre")
            mostrar_lista(inv.buscar_por_nombre(texto))
        elif opcion == "8":
            id_c = pedir("ID del elemento")
            cantidad = int(pedir("Nueva cantidad", 0))
            print("✔ Actualizado." if inv.actualizar_cantidad(id_c, cantidad)
                  else "✘ No encontrado.")
        elif opcion == "9":
            id_c = pedir("ID del elemento a eliminar")
            print("✔ Eliminado." if inv.eliminar_componente(id_c)
                  else "✘ No encontrado.")
        elif opcion == "10":
            umbral = int(pedir("Umbral de bajo stock", 5))
            print(f"\n--- Elementos con cantidad <= {umbral} ---")
            mostrar_lista(inv.reporte_bajo_stock(umbral))
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
