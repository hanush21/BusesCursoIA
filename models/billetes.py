class Billete:
    def init(self, billete_id, bus, cliente, asiento, fecha):
        self.billete_id = billete_id
        self.bus = bus
        self.cliente = cliente
        self.asiento = asiento
        self.fecha = fecha

    def str(self):
        return (f"Billete {self.billete_id} para {self.cliente.nombre_completo()} en "
                f"bus {self.bus.placa} asiento {self.asiento} fecha {self.fecha}")
