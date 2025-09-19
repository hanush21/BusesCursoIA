from typing import List, Optional
from models.cliente import Cliente

def find_by_id(clientes: List[Cliente], cliente_id: int) -> Optional[Cliente]:
    return next((c for c in clientes if c.cliente_id == int(cliente_id)), None)

def create_cliente(clientes: List[Cliente], nombre: str, apellido: str = None) -> Cliente:
    new_id = max([c.cliente_id for c in clientes], default=0) + 1
    c = Cliente(new_id, nombre, apellido)
    clientes.append(c)
    return c

def update_cliente(clientes: List[Cliente], cliente_id: int, nombre: Optional[str] = None, apellido: Optional[str] = None) -> bool:
    c = find_by_id(clientes, cliente_id)
    if not c:
        return False
    if nombre is not None:
        c.nombre = nombre
    if apellido is not None:
        c.apellido = apellido
    return True

def delete_cliente(clientes: List[Cliente], cliente_id: int, billetes: list) -> bool:
    c = find_by_id(clientes, cliente_id)
    if not c:
        return False
    if any(billete.cliente.cliente_id == c.cliente_id for billete in billetes):
        raise ValueError("No se puede eliminar un cliente con billetes asociados. Cancela los billetes primero.")
    clientes.remove(c)
    return True
