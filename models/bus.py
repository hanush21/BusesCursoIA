class Bus:
    def init(self, bus_id, placa, capacidad):
        self.bus_id = bus_id
        self.placa = placa
        self.capacidad = capacidad
        self.billetes = []

    def agregar_billete(self, billete):
        if len(self.billetes) < self.capacidad:
            self.billetes.append(billete)
        else:
            raise Exception("Capacidad del bus alcanzada")

    def str(self):
        return f"Bus {self.placa} con capacidad {self.capacidad}"