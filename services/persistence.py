import csv
import os
from models.bus import Bus
from models.cliente import Cliente
from models.billetes import Billete

BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BUSES_FILE = os.path.join(BASE_DIR, "data", "buses.csv")
CLIENTES_FILE = os.path.join(BASE_DIR, "data", "clientes.csv")
BILLETES_FILE = os.path.join(BASE_DIR, "data", "billetes.csv")

def guardar_buses(buses):
    os.makedirs(os.path.dirname(BUSES_FILE), exist_ok=True)
    with open(BUSES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["bus_id", "placa", "capacidad"])
        for bus in buses:
            writer.writerow([bus.bus_id, bus.placa, bus.capacidad])

def cargar_buses():
    buses = []
    try:
        with open(BUSES_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                buses.append(Bus(int(row["bus_id"]), row["placa"], int(row["capacidad"])))
    except FileNotFoundError:
        pass
    return buses

def guardar_clientes(clientes):
    os.makedirs(os.path.dirname(CLIENTES_FILE), exist_ok=True)
    with open(CLIENTES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cliente_id", "nombre", "apellido"])
        for c in clientes:
            writer.writerow([c.cliente_id, c.nombre, c.apellido or ""])

def cargar_clientes():
    clientes = []
    try:
        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clientes.append(Cliente(int(row["cliente_id"]), row["nombre"], row.get("apellido") or None))
    except FileNotFoundError:
        pass
    return clientes

def guardar_billetes(billetes):
    os.makedirs(os.path.dirname(BILLETES_FILE), exist_ok=True)
    with open(BILLETES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["billete_id", "bus_id", "cliente_id", "asiento", "fecha"])
        for billete in billetes:
            writer.writerow([
                billete.billete_id,
                billete.bus.bus_id,
                billete.cliente.cliente_id,
                billete.asiento,
                billete.fecha
            ])

def cargar_billetes(buses, clientes):
    billetes = []
    try:
        with open(BILLETES_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bus = next((b for b in buses if b.bus_id == int(row["bus_id"])), None)
                cliente = next((c for c in clientes if c.cliente_id == int(row["cliente_id"])), None)
                if bus and cliente:
                    billete = Billete(int(row["billete_id"]), bus, cliente, int(row["asiento"]), row["fecha"])
                    billetes.append(billete)
                    bus.billetes.append(billete)
    except FileNotFoundError:
        pass
    return billetes
