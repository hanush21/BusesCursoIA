from services.persistence import (
    cargar_buses,
    cargar_clientes,
    cargar_billetes,
    guardar_buses,
    guardar_clientes,
    guardar_billetes
)
from services.billetes_service import venda, devolucio, estat, crear_billete, cancelar_billete
from services.bus import create_bus, update_bus, delete_bus, find_by_id as find_bus
from services.cliente import create_cliente, update_cliente, delete_cliente, find_by_id as find_cliente
from models.bus import Bus
from models.cliente import Cliente

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Introduce un número válido.")

def pausar():
    input("\nPulsa ENTER para continuar...")

def menu_principal():
    print("\n=== Sistema de Buses ===")
    print("1) Gestión de buses")
    print("2) Gestión de clientes")
    print("3) Venta de billetes")
    print("4) Devolución/cancelación de billetes")
    print("5) Estado de asientos")
    print("6) Listar billetes por bus")
    print("0) Salir")
    return input("Selecciona una opción: ").strip()

def menu_buses(buses):
    while True:
        print("\n-- Gestión de buses --")
        print("1) Listar buses")
        print("2) Crear bus")
        print("3) Actualizar bus")
        print("4) Eliminar bus")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1":
            if not buses:
                print("No hay buses.")
            else:
                for b in buses:
                    print(b, "- libres:", len(b.asientos_disponibles()))
            pausar()
        elif op == "2":
            placa = input("Placa: ").strip()
            capacidad = input_int("Capacidad: ")
            bus = create_bus(buses, placa, capacidad)
            guardar_buses(buses)
            print("Creado:", bus)
            pausar()
        elif op == "3":
            bid = input_int("ID del bus a actualizar: ")
            bus = find_bus(buses, bid)
            if not bus:
                print("No existe ese bus.")
                pausar(); continue
            nueva_placa = input(f"Placa nueva (enter para mantener {bus.placa}): ").strip() or None
            cap_in = input("Nueva capacidad (enter para mantener): ").strip()
            nueva_cap = int(cap_in) if cap_in else None
            try:
                update_bus(buses, bid, nueva_placa, nueva_cap)
                guardar_buses(buses)
                print("Actualizado:", bus)
            except Exception as e:
                print("Error:", e)
            pausar()
        elif op == "4":
            bid = input_int("ID del bus a eliminar: ")
            try:
                ok = delete_bus(buses, bid)
                if ok:
                    guardar_buses(buses)
                    print("Bus eliminado.")
                else:
                    print("Bus no encontrado.")
            except Exception as e:
                print("Error:", e)
            pausar()
        elif op == "0":
            return
        else:
            print("Opción no válida.")

def menu_clientes(clientes, billetes):
    while True:
        print("\n-- Gestión de clientes --")
        print("1) Listar clientes")
        print("2) Crear cliente")
        print("3) Actualizar cliente")
        print("4) Eliminar cliente")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1":
            if not clientes:
                print("No hay clientes.")
            else:
                for c in clientes:
                    print(c)
            pausar()
        elif op == "2":
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido (opcional): ").strip() or None
            c = create_cliente(clientes, nombre, apellido)
            guardar_clientes(clientes)
            print("Creado:", c)
            pausar()
        elif op == "3":
            cid = input_int("ID del cliente a actualizar: ")
            c = find_cliente(clientes, cid)
            if not c:
                print("No existe ese cliente.")
                pausar(); continue
            nombre = input(f"Nombre nuevo (enter para mantener {c.nombre}): ").strip() or None
            apellido = input(f"Apellido nuevo (enter para mantener {c.apellido or ''}): ").strip() or None
            update_cliente(clientes, cid, nombre, apellido)
            guardar_clientes(clientes)
            print("Actualizado:", c)
            pausar()
        elif op == "4":
            cid = input_int("ID del cliente a eliminar: ")
            try:
                ok = delete_cliente(clientes, cid, billetes)
                if ok:
                    guardar_clientes(clientes)
                    print("Cliente eliminado.")
                else:
                    print("Cliente no encontrado.")
            except Exception as e:
                print("Error:", e)
            pausar()
        elif op == "0":
            return
        else:
            print("Opción no válida.")

def menu_billetes(buses, clientes, billetes):
    print("\n-- Venta de billetes --")
    if not buses:
        print("Primero crea un bus.")
        pausar(); return
    # elegir bus
    for b in buses:
        print(b, "- asientos libres:", b.asientos_disponibles())
    bid = input_int("ID del bus: ")
    bus = find_bus(buses, bid)
    if not bus:
        print("Bus no encontrado."); pausar(); return
    # elegir cliente o crear
    if clientes:
        for c in clientes:
            print(c)
    else:
        print("No hay clientes, crea uno nuevo.")
    elec = input("ID de cliente existente o 'N' para crear: ").strip()
    if elec.upper() == 'N':
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido (opcional): ").strip() or None
        cliente = create_cliente(clientes, nombre, apellido)
        guardar_clientes(clientes)
    else:
        cliente = find_cliente(clientes, int(elec))
        if not cliente:
            print("Cliente no encontrado."); pausar(); return
    # elegir cantidad y/o asiento
    cantidad = input_int("¿Cuántos billetes vender? ")
    auto = input("Asignación automática de asientos? (S/N): ").strip().upper() != 'N'
    vendidos = 0
    if auto:
        for _ in range(cantidad):
            ok, msg, _ = crear_billete(bus, cliente, billetes)
            print(msg)
            if ok:
                vendidos += 1
            else:
                break
    else:
        for _ in range(cantidad):
            print("Libres:", bus.asientos_disponibles())
            asiento = input_int("Asiento específico: ")
            ok, msg, _ = crear_billete(bus, cliente, billetes, asiento=asiento)
            print(msg)
            if ok:
                vendidos += 1
    if vendidos:
        guardar_billetes(billetes)
        guardar_buses(buses)  # para persistir el estado de billetes por bus
    pausar()

def menu_devoluciones(buses, clientes, billetes):
    print("\n-- Devolución/cancelación --")
    print("1) Devolver los últimos N billetes (LIFO)")
    print("2) Cancelar por ID de billete")
    op = input("Opción: ").strip()
    if op == '1':
        cantidad = input_int("Cantidad a devolver: ")
        ok, msg = devolucio(cantidad, billetes, buses)
        print(msg)
        if ok:
            guardar_billetes(billetes)
            guardar_buses(buses)
    elif op == '2':
        bid = input_int("ID de billete a cancelar: ")
        ok, msg = cancelar_billete(billetes, bid)
        print(msg)
        if ok:
            guardar_billetes(billetes)
            guardar_buses(buses)
    else:
        print("Opción no válida.")
    pausar()

def listar_billetes_por_bus(buses):
    if not buses:
        print("No hay buses."); return
    for bus in buses:
        print(f"\nBus {bus.bus_id} ({bus.placa}) capacidad {bus.capacidad}")
        print("Ocupados:", sorted(bus.asientos_ocupados()))
        for b in sorted(bus.billetes, key=lambda x: x.asiento):
            print("  ", b)

def main():
    buses = cargar_buses()
    clientes = cargar_clientes()
    billetes = cargar_billetes(buses, clientes)

    salir = False
    while not salir:
        opcion = menu_principal()
        if opcion == "1":
            menu_buses(buses)
        elif opcion == "2":
            menu_clientes(clientes, billetes)
        elif opcion == "3":
            menu_billetes(buses, clientes, billetes)
        elif opcion == "4":
            menu_devoluciones(buses, clientes, billetes)
        elif opcion == "5":
            total_plazas = sum(bus.capacidad for bus in buses)
            plazas_vendidas = len(billetes)
            plazas_libres = total_plazas - plazas_vendidas
            estat(total_plazas, plazas_libres, plazas_vendidas)
            pausar()
        elif opcion == "6":
            listar_billetes_por_bus(buses)
            pausar()
        elif opcion == "0":
            salir = True
            print("Saliendo del sistema. ¡Hasta luego!")
        else:
            print("Opción no válida. Por favor, seleccione una opción correcta.")

if __name__ == "__main__":
    main()
