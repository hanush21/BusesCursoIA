class Billete:
    def __init__(self, billete_id, bus, cliente, asiento, fecha):
        self.billete_id = int(billete_id)
        self.bus = bus
        self.cliente = cliente
        self.asiento = int(asiento)
        self.fecha = str(fecha)

    def __str__(self):
        return (f"Billete(id={self.billete_id}, cliente={self.cliente.nombre_completo()}, "
                f"bus={self.bus.placa}, asiento={self.asiento}, fecha={self.fecha})")
