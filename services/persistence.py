import csv
from services.bus import Bus
from services.cliente import Cliente
from services.billete import Billete
from datetime import datetime

# Archivos CSV
BUSES_FILE = 'data/buses.csv'
CLIENTES_FILE = 'data/clientes.csv'
BILLETES_FILE = 'data/billetes.csv'

def guardar_buses(buses):
    with open(BUSES_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['bus_id', 'placa', 'capacidad'])
        for bus in buses:
            writer.writerow([bus.bus_id, bus.placa, bus.capacidad])

def cargar_buses():
    buses = []
    try:
        with open(BUSES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bus = Bus(int(row['bus_id']), row['placa'], int(row['capacidad']))
                buses.append(bus)
    except FileNotFoundError:
        pass
    return buses

def guardar_clientes(clientes):
    with open(CLIENTES_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['cliente_id', 'nombre', 'apellido'])
        for cliente in clientes:
            writer.writerow([cliente.cliente_id, cliente.nombre, cliente.apellido or ""])

def cargar_clientes():
    clientes = []
    try:
        with open(CLIENTES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cliente = Cliente(int(row['cliente_id']), row['nombre'], row['apellido'])
                clientes.append(cliente)
    except FileNotFoundError:
        pass
    return clientes

def guardar_billetes(billetes):
    with open(BILLETES_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['billete_id', 'bus_id', 'cliente_id', 'asiento', 'fecha'])
        for billete in billetes:
            writer.writerow([billete.billete_id, billete.bus.bus_id, billete.cliente.cliente_id, billete.asiento, billete.fecha])

def cargar_billetes(buses, clientes):
    billetes = []
    try:
        with open(BILLETES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bus = next((b for b in buses if b.bus_id == int(row['bus_id'])), None)
                cliente = next((c for c in clientes if c.cliente_id == int(row['cliente_id'])), None)
                fecha = row['fecha']
                if bus and cliente:
                    billete = Billete(int(row['billete_id']), bus, cliente, int(row['asiento']), fecha)
                    billetes.append(billete)
                    bus.billetes.append(billete)  # Asignar billete al bus
    except FileNotFoundError:
        pass
    return billetes
