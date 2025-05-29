import Validaciones as Validaciones

class Nodo:
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre):
        if Validaciones.validar_Nombre(nombre):
            self.nombre = nombre
        else:
            raise ValueError("El nombre del nodo no es valido")
    
    def getNombre(self):
        return  self.nombre


        
