from services.billetes_service import estat, venda, devolucio
from services.bus import Bus
from services.cliente import Cliente
from services.billete import Billete

def main():
    total_plazas = int(input("Ingrese el número de asientos\n"))
    plazas_libres = total_plazas
    plazas_vendidas = 0

    # Para ejemplificar múltiples buses y clientes en el futuro:
    buses = []
    clientes = []
    billetes = []

    salir = False
    print("1.- Venta de billetes.")
    print("2.- Devolución de billetes.")
    print("3.- Estado de la venta.")
    print("0.- Salir.")
    estat(total_plazas, plazas_libres, plazas_vendidas)
    while not salir:
        pregunta = input("Seleccione una opción: ")
        if pregunta == "1":
            plazas_demanda = int(input("Ingrese cantidad a vender: "))
            plazas_libres, plazas_vendidas, mensaje, exito = venda(plazas_demanda, plazas_libres, plazas_vendidas)
            print(mensaje)
            if exito:
                estat(total_plazas, plazas_libres, plazas_vendidas)
        elif pregunta == "2":
            plazas_devolucion = int(input("Ingrese cantidad a devolver: "))
            plazas_libres, plazas_vendidas, mensaje, exito = devolucio(plazas_devolucion, total_plazas, plazas_libres, plazas_vendidas)
            print(mensaje)
            if exito:
                estat(total_plazas, plazas_libres, plazas_vendidas)
        elif pregunta == "3":
            estat(total_plazas, plazas_libres, plazas_vendidas)
        elif pregunta == "0":
            salir = True
        else:
            print("Opción no válida. Por favor, seleccione una opción correcta.")

if __name__ == "__main__":
    main()
