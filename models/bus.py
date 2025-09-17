class Bus:
    def __init__(self, bus_id, placa, capacidad):
        self.bus_id = bus_id
        self.placa = placa
        self.capacidad = capacidad
        self.billetes = []  # Lista para almacenar billetes asignados a este bus

    def agregar_billete(self, billete):
        if len(self.billetes) < self.capacidad:
            self.billetes.append(billete)
        else:
            raise Exception("Capacidad del bus alcanzada")

    def __str__(self):
        return f"Bus {self.placa} con capacidad {self.capacidad}"
