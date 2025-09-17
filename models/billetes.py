class Billete:
    def __init__(self, billete_id, bus, cliente, asiento, fecha):
        self.billete_id = billete_id
        self.bus = bus           # Objeto bus
        self.cliente = cliente   # Objeto cliente
        self.asiento = asiento
        self.fecha = fecha

    def __str__(self):
        return (f"Billete {self.billete_id} para {self.cliente.nombre_completo()} en "
                f"bus {self.bus.placa} asiento {self.asiento} fecha {self.fecha}")
