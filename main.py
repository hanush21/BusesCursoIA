def estat(total_plazas, plazas_libres, plazas_vendidas):
    """Función para mostrar el estado de la venta."""
    print(f"Total: {total_plazas}")
    print(f"Libre: {plazas_libres}")
    print(f"Vendido: {plazas_vendidas}")

def venda(demanda, plazas_libres, plazas_vendidas):
    """Función para vender billetes."""
    if demanda <= plazas_libres and demanda > 0:
        plazas_libres -= demanda
        plazas_vendidas += demanda
        mensaje = f"Se vendieron {demanda} billetes"
        exito = True
    else:
        mensaje = "Error"
        exito = False
    return plazas_libres, plazas_vendidas, mensaje, exito

def devolucio(devolucion, plazas_total, plazas_libres, plazas_vendidas):
    """Función para devolver billetes."""
    if devolucion <= plazas_vendidas and devolucion > 0 and (plazas_libres + devolucion) <= plazas_total:
        plazas_libres += devolucion
        plazas_vendidas -= devolucion
        mensaje = f"Se devolvieron {devolucion} billetes"
        exito = True
    else:
        mensaje = "Error"
        exito = False
    return plazas_libres, plazas_vendidas, mensaje, exito

def estat(total_plazas, plazas_libres, plazas_vendidas):
    """Función para mostrar el estado de la venta."""
    print(f"Total: {total_plazas}")
    print(f"Libre: {plazas_libres}")
    print(f"Vendido: {plazas_vendidas}")


def main():
    total_plazas = int(input("Ingrese el número de asientos\n"))
    plazas_libres = total_plazas
    plazas_vendidas = 0
    salir = False
    print("1.- Venta de billetes.")
    print("2.- Devolución de billetes.")
    print("3.- Estado de la venta.")
    print("0.- Salir.")
    estat(total_plazas, plazas_libres, plazas_vendidas)
    while not salir:
        pregunta = input()
        if pregunta == "1":
            plazas_demanda = int(input())
            plazas_libres, plazas_vendidas, mensaje, exito = venda(plazas_demanda, plazas_libres, plazas_vendidas)
            print(mensaje)
            if exito:
                estat(total_plazas, plazas_libres, plazas_vendidas)
        elif pregunta == "2":
            plazas_devolucion = int(input())
            plazas_libres, plazas_vendidas, mensaje, exito = devolucio(plazas_devolucion, total_plazas, plazas_libres, plazas_vendidas)
            print(mensaje)
            if exito:
                estat(total_plazas, plazas_libres, plazas_vendidas)
        elif pregunta == "3":
            pass  # No mostrar estado aquí
        elif pregunta == "0":
            salir = True
        else:
            print("Opción no válida. Por favor, seleccione una opción correcta.")

if __name__ == "__main__":
    main()