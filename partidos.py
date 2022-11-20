class Partido:
    def __init__(self, local, visitante, fecha, estadio, id, asientos_ocup=[]):
        self.local = local
        self.visitante = visitante
        self.fecha = fecha
        self.estadio = estadio
        self.id = id
        self.asientos_ocup = asientos_ocup

    def mostrar_datos(self):
        print(f"{self.local.nombre} VS {self.visitante.nombre}\nFecha: {self.fecha}\nEstadio: {self.estadio.nombre}\nId: {self.id}")