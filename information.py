class Informacion:
    def __init__(self, modo: str, camino: list, costo: float, tiempo: float):
        #crear esto para guardar mejor la informacion
        self.modo = modo
        self.camino = camino
        self.costo = costo
        self.tiempo = tiempo

        
    def __repr__(self):
        camino_str = " -> ".join(
            f"{c.origen.nombre} → {c.destino.nombre} ({c.distancia} km)" for c in self.camino
        )
        return (f"Modo: {self.modo}\n"
                f"Camino: {camino_str}\n"
                f"Costo Total: ${self.costo:.2f}\n"
                f"Tiempo Total: {self.tiempo:.2f} minutos")