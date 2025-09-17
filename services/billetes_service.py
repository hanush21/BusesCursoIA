from models.bus import Bus
from models.cliente import Cliente
from models.billetes import Billete

def estat(total_plazas, plazas_libres, plazas_vendidas):
    print(f"Total de asientos: {total_plazas}")
    print(f"Plazas libres: {plazas_libres}")
    print(f"Plazas vendidas: {plazas_vendidas}")

def venda(demanda, buses, clientes, billetes):
    total_capacidad = sum(bus.capacidad for bus in buses)
    plazas_vendidas = len(billetes)
    plazas_libres = total_capacidad - plazas_vendidas

    if demanda <= plazas_libres and demanda > 0:
        nueva_id = max([b.billete_id for b in billetes], default=0) + 1
        billetes_generados = 0
        for bus in buses:
            capacidad_disponible = bus.capacidad - len(bus.billetes)
            while capacidad_disponible > 0 and billetes_generados < demanda:
                # Crear Cliente anónimo para demo
                cliente = Cliente(cliente_id=0, nombre="Anonimo")
                clientes.append(cliente)
                asiento = len(bus.billetes) + 1
                fecha = "2025-09-17"  # fecha fija para demo
                billete = Billete(nueva_id, bus, cliente, asiento, fecha)
                bus.agregar_billete(billete)
                billetes.append(billete)
                nueva_id += 1
                billetes_generados += 1
                capacidad_disponible -= 1
        mensaje = f"Se vendieron {demanda} billetes"
        exito = True
    else:
        mensaje = "Error: plazas insuficientes o cantidad inválida"
        exito = False
    return exito, mensaje

def devolucio(cantidad, billetes, buses):
    if cantidad <= len(billetes) and cantidad > 0:
        for _ in range(cantidad):
            billete = billetes.pop()
            bus = billete.bus
            if billete in bus.billetes:
                bus.billetes.remove(billete)
        mensaje = f"Se devolvieron {cantidad} billetes"
        exito = True
    else:
        mensaje = "Error: no se puede devolver esa cantidad"
        exito = False
    return exito, mensaje