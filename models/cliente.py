
class Cliente:
    def __init__(self, cliente_id, nombre, apellido=None):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.apellido = apellido

    def nombre_completo(self):
        if self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre

    def __str__(self):
        return f"Cliente: {self.nombre_completo()}"
