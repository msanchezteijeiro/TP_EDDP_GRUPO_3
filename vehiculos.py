from Validaciones import *
from conexiones import *

class Vehiculos: 

    def __init__ (self, modo: str, capacidad: float):
        try: 
            if not Validaciones.validar_str (modo): 
                raise TypeError (f"el el modo tiene que ser una cadena str")        
            if not Validaciones.validar_float (capacidad) and not Validaciones.validar_int (capacidad): 
                raise ValueError (f"la capacidad {capacidad} no es valida")

        except: 
            print(f"El Vehiculo no es valido")
        
        self.setModo(modo)
        self.setCapacidad(capacidad)

    def setModo (self, modo):
        self.modo = modo
    
    def setCapacidad (self, capacidad): 
        self.capacidad = capacidad
        

class Ferroviario (Vehiculos): 
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_kg, modo='Ferroviario'):
        super.__init__(modo, capacidad)
        self.velocidad = velocidad
        self.costo_fijo = costo_fijo
        self.costo_por_kg = costo_por_kg
    
    def calcular_costo (self, conexion, solicitud): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        if conexion.distancia < 200: 
            costo = conexion.distancia * 20 + self.costo_por_kg * solicitud.carga + self.costo_fijo
        
    