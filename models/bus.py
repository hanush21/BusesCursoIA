class Bus:
    def __init__(self, bus_id, placa, capacidad):
        self.bus_id = int(bus_id)
        self.placa = str(placa)
        self.capacidad = int(capacidad)
        self.billetes = []

    def agregar_billete(self, billete):
        if len(self.billetes) < self.capacidad:
            self.billetes.append(billete)
        else:
            raise Exception("Capacidad del bus alcanzada")

    def asientos_ocupados(self):
        return sorted([b.asiento for b in self.billetes])

    def asientos_disponibles(self):
        ocupados = set(self.asientos_ocupados())
        return [n for n in range(1, self.capacidad + 1) if n not in ocupados]

    def __str__(self):
        return f"Bus(id={self.bus_id}, placa={self.placa}, capacidad={self.capacidad}, ocupados={len(self.billetes)})"
