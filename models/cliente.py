class Cliente:
    def __init__(self, cliente_id, nombre, apellido=None):
        self.cliente_id = int(cliente_id)
        self.nombre = str(nombre)
        self.apellido = str(apellido) if apellido else None

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}" if self.apellido else self.nombre

    def __str__(self):
        return f"Cliente(id={self.cliente_id}, nombre={self.nombre_completo()})"
