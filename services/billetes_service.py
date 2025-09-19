from datetime import date
from typing import List, Tuple, Optional
from models.bus import Bus
from models.cliente import Cliente
from models.billetes import Billete

def estat(total_plazas: int, plazas_libres: int, plazas_vendidas: int) -> None:
    print(f"Total de asientos: {total_plazas}")
    print(f"Plazas libres: {plazas_libres}")
    print(f"Plazas vendidas: {plazas_vendidas}")

def _next_billete_id(billetes: List[Billete]) -> int:
    return max([b.billete_id for b in billetes], default=0) + 1

def crear_billete(bus: Bus, cliente: Cliente, billetes: List[Billete], asiento: Optional[int] = None, fecha: Optional[str] = None) -> Tuple[bool, str, Optional[Billete]]:
    if fecha is None:
        fecha = str(date.today())
    
    libres = bus.asientos_disponibles()
    if not libres:
        return False, "Bus sin plazas disponibles", None
    if asiento is not None:
        if asiento not in libres:
            return False, f"Asiento {asiento} no disponible en bus {bus.placa}", None
    else:
        asiento = libres[0]
    new_id = _next_billete_id(billetes)
    billete = Billete(new_id, bus, cliente, asiento, fecha)
    bus.agregar_billete(billete)
    billetes.append(billete)
    return True, f"Billete creado: {billete}", billete

def cancelar_billete(billetes: List[Billete], billete_id: int) -> Tuple[bool, str]:
    target = next((b for b in billetes if b.billete_id == int(billete_id)), None)
    if not target:
        return False, "Billete no encontrado"
    
    if target in target.bus.billetes:
        target.bus.billetes.remove(target)
    billetes.remove(target)
    return True, f"Billete {billete_id} cancelado"

def venda(demanda: int, buses: List[Bus], clientes: List[Cliente], billetes: List[Billete]) -> Tuple[bool, str]:
    
    total_capacidad = sum(b.capacidad for b in buses)
    plazas_vendidas = len(billetes)
    plazas_libres = total_capacidad - plazas_vendidas
    if demanda <= 0:
        return False, "La demanda debe ser mayor que 0"
    if demanda > plazas_libres:
        return False, f"No hay plazas suficientes. Disponibles: {plazas_libres}"
    if not clientes:
        clientes.append(Cliente(1, "Anonimo"))
    cliente = clientes[0]
    vendidos = 0
    
    for bus in buses:
        while bus.asientos_disponibles() and vendidos < demanda:
            ok, msg, _ = crear_billete(bus, cliente, billetes)
            if not ok:
                return False, msg
            vendidos += 1
        if vendidos == demanda:
            break
    return True, f"Se vendieron {vendidos} billetes"

def devolucio(cantidad: int, billetes: List[Billete], buses: List[Bus]) -> Tuple[bool, str]:
    if cantidad <= 0:
        return False, "La cantidad debe ser mayor que 0"
    if cantidad > len(billetes):
        return False, "Error: no se puede devolver esa cantidad"
    for _ in range(cantidad):
        billete = billetes.pop()  # último vendido
        if billete in billete.bus.billetes:
            billete.bus.billetes.remove(billete)
    return True, f"Se devolvieron {cantidad} billetes"