class Producto:
    def __init__(self, nombre, precio, tipo, inventario):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.inventario = inventario
        self.iva = precio * 0.16
        self.precio_neto = precio + self.iva

class Bebida(Producto):
    def __init__(self, nombre, precio, tipo, inventario, alcochol):
        super().__init__(nombre, precio, tipo, inventario)
        self.alcohol = alcochol
        self.iva = precio * 0.16
        self.precio_neto = precio + self.iva

    def mostrar(self):
        print(f"Nombre: {self.nombre}\nPrecio: {self.precio_neto}\nUnidades disponibles: {self.inventario}\nAlcohólica: {self.alcohol}")

    def mostrar2(self):
        print(f"{self.nombre}  {self.precio} $")

    def cambiar_inv(self):
        self.inventario -= 1

class Comida(Producto):
    def __init__(self, nombre, precio, tipo, inventario, empa_prep=None):
        super().__init__(nombre, precio, tipo, inventario)
        self.empa_prep = empa_prep
        self.iva = precio * 0.16
        self.precio_neto = precio + self.iva

    def mostrar(self):
        print(f"Nombre: {self.nombre}\nPrecio {self.precio_neto}\nUnidades disponibles: {self.inventario}")

    def mostrar2(self):
        print(f"{self.nombre}  {self.precio} $")

    def cambiar_inv(self):
        self.inventario -= 1