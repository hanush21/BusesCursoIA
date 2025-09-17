from services.persistence import (
    cargar_buses, cargar_clientes, cargar_billetes,
    guardar_buses, guardar_clientes, guardar_billetes
)
from services.billetes_service import venda, devolucio
from services.billetes_service import estat  # adaptarlo para imprimir según buses

def main():
    buses = cargar_buses()
    clientes = cargar_clientes()
    billetes = cargar_billetes(buses, clientes)

    # Si no hay buses cargados, crear uno inicial para demo
    if not buses:
        from services.bus import Bus
        bus_demo = Bus(bus_id=1, placa="ABC123", capacidad=50)
        buses.append(bus_demo)

    salir = False
    while not salir:
        print("1.- Venta de billetes.")
        print("2.- Devolución de billetes.")
        print("3.- Estado de la venta.")
        print("0.- Salir.")
        pregunta = input("Seleccione una opción: ")
        if pregunta == "1":
            demanda = int(input("Cantidad a vender: "))
            exito, mensaje = venda(demanda, buses, clientes, billetes)
            print(mensaje)
            if exito:
                guardar_buses(buses)
                guardar_clientes(clientes)
                guardar_billetes(billetes)
        elif pregunta == "2":
            cantidad = int(input("Cantidad a devolver: "))
            exito, mensaje = devolucio(cantidad, billetes, buses)
            print(mensaje)
            if exito:
                guardar_buses(buses)
                guardar_clientes(clientes)
                guardar_billetes(billetes)
        elif pregunta == "3":
            total_plazas = sum(bus.capacidad for bus in buses)
            plazas_vendidas = len(billetes)
            plazas_libres = total_plazas - plazas_vendidas
            estat(total_plazas, plazas_libres, plazas_vendidas)
        elif pregunta == "0":
            salir = True
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
