

class Cliente:
    def init(self, cliente_id, nombre, apellido=None):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.apellido = apellido

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}" if self.apellido else self.nombre

    def str(self):
        return f"Cliente: {self.nombre_completo()}"