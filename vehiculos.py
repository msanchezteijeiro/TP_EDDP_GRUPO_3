from validaciones import *

class Vehiculos: 
    modos_permitidos = ["ferroviario", "automotor", "maritimo", "aereo"]
    def __init__ (self, modo: str, velocidad: float, capacidad: float, costo_fijo: float, costo_por_km: float, costo_por_kg: float): 
        if not Validaciones.validar_str (modo): 
            raise TypeError (f"el el modo tiene que ser una cadena str")        
        if not Validaciones.validar_modos(modo, Vehiculos.modos_permitidos): 
            raise ValueError (f"el modo {modo} no es valido")
        if not Validaciones.validar_float (velocidad) and not Validaciones.validar_int (velocidad): 
            raise ValueError (f"la velocidad {velocidad} no es valida")
        if not Validaciones.validar_float (capacidad) and not Validaciones.validar_int (capacidad): 
            raise ValueError (f"la capacidad {capacidad} no es valida")
        if not Validaciones.validar_float (costo_fijo) and not Validaciones.validar_int (costo_fijo): 
            raise ValueError (f"el costo fijo {costo_fijo} no es valido")
        if not Validaciones.validar_float (costo_por_km) and not Validaciones.validar_int (costo_por_km): 
            raise ValueError (f"el costo por kilometro {costo_por_km} no es valido")
        if not Validaciones.validar_float (costo_por_kg) and not Validaciones.validar_int (costo_por_kg): 
            raise ValueError (f"el costo por kilogramo {costo_por_kg} no es valido")
        
        self.setModo(modo)
        self.setVelocidad (velocidad)
        self.setCapacidad(capacidad)
        self.setCosto_fijo (costo_fijo)
        self.setCosto_por_km (costo_por_km)
        self.setCosto_por_kg (costo_por_kg)
        

    def setModo (self, modo):
        self.modo = modo
        
    def setVelocidad (self, velocidad): 
         self.velocidad = velocidad
         
    def setCapacidad (self, capacidad): 
        self.capacidad = capacidad
        
    def setCosto_fijo (self, costo_fijo): 
        self.costo = costo_fijo
        
    def setCosto_por_km (self, costo_por_km): 
        self.costo_por_km = costo_por_km
        
    def setCosto_por_kg (self, costo_por_kg): 
        self.costo_por_kg = costo_por_kg
        
vehiculo1 = Vehiculos('ferroviario', 20, 500, 2000.0, 250.0, 250.0)

