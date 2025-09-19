from typing import List, Optional
from models.bus import Bus

def find_by_id(buses: List[Bus], bus_id: int) -> Optional[Bus]:
    return next((b for b in buses if b.bus_id == int(bus_id)), None)

def create_bus(buses: List[Bus], placa: str, capacidad: int) -> Bus:
    new_id = max([b.bus_id for b in buses], default=0) + 1
    bus = Bus(new_id, placa, int(capacidad))
    buses.append(bus)
    return bus

def update_bus(buses: List[Bus], bus_id: int, placa: Optional[str] = None, capacidad: Optional[int] = None) -> bool:
    bus = find_by_id(buses, bus_id)
    if not bus:
        return False
    if placa is not None:
        bus.placa = placa
    if capacidad is not None:
        capacidad = int(capacidad)
        if capacidad < len(bus.billetes):
            raise ValueError("No puedes reducir la capacidad por debajo de los asientos ya vendidos.")
        bus.capacidad = capacidad
    return True

def delete_bus(buses: List[Bus], bus_id: int) -> bool:
    bus = find_by_id(buses, bus_id)
    if not bus:
        return False
    if bus.billetes:
        raise ValueError("No se puede eliminar un bus con billetes vendidos. Devuelve/cancela los billetes primero.")
    buses.remove(bus)
    return True
