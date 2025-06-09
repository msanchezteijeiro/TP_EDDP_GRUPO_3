from validaciones import *
from conexiones import *

class Vehiculos: 
    modos = ["Ferroviario", "Automotor", "Maritimo", "Aereo"]
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
        try: 
            if not Validaciones.validar_str (modo): 
                raise TypeError (f"el el modo tiene que ser una cadena str")       
            if not Validaciones.validar_modo (modo, Vehiculos.modos): 
                raise ValueError ("el modo no es valida")
        except TypeError: 
            print("el modo ingresado no es un numero")
        except ValueError: 
            print ("el modo no es uno de los cuatro permitidos")
         
        self.modo = modo
    
    def setCapacidad (self, capacidad): 
        try: 
            if not Validaciones.validar_float (capacidad) and not Validaciones.validar_int (capacidad): 
                raise ValueError (f"la capacidad {capacidad} no es valida")
        except ValueError:
            print ("la capacidad ingresada no es valida")
        self.capacidad = capacidad
    
    def getModo (self): 
        return self.modo

    def getCapacidad (self): 
        return self.capacidad
    
class Ferroviario (Vehiculos): 
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_kg, modo='Ferroviario'):
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError:
            print("el vehiculo aereo seleccionado no es valido") 
            
        super().__init__(modo, capacidad)
        self.velocidad = velocidad
        self.costo_fijo = costo_fijo
        self.costo_por_kg = costo_por_kg
    
    def setVelocidad (self, velocidad): 
        try: 
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError: 
            print("la nueva velocidad debe ser un numero")
            
        self.velocidad = velocidad
    
    def setCosto_fijo (self, costo_fijo):
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
        except TypeError: 
            print ("el nuevo costo fijo debe ser un numero")
            
        self.costo_fijo = costo_fijo 
    
    def setCosto_por_kg (self, costo_por_kg): 
        try: 
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError:
            print ("el nuuevo costo por kg debe ser un numero")
        
        self.costo_por_kg = costo_por_kg
        
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def calcular_costo (self, conexion, carga): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        if conexion.distancia < 200: 
            costo = conexion.distancia * 20 + self.costo_por_kg * carga + self.costo_fijo
        elif conexion.distancia >= 200: 
            costo = conexion.distancia * 15 + self.costo_por_kg * carga + self.costo_fijo
        return costo
    
    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.distancia/self.velocidad)*60
        return tiempo_minutos
        
class Automotor (Vehiculos): 
    
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_km, modo = "Automotor"):
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError:
            print("el vehiculo aereo seleccionado no es valido") 
            
        super().__init__(modo, capacidad)
        self.velocidad = velocidad
        self.costo_fijo = costo_fijo
        self.costo_por_km = costo_por_km
        
    def set_Velocidad (self, velocidad): 
        try: 
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError: 
            print("la nueva velocidad debe ser un numero")
            
        self.velocidad = velocidad
    
    def setCosto_fijo (self, costo_fijo):
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
        except TypeError: 
            print ("el nuevo costo fijo debe ser un numero")
            
        self.costo_fijo = costo_fijo 
    
    def setCosto_por_km (self, costo_por_km): 
        try: 
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo por km debe ser un numero")
        except TypeError: 
            print ("el nuuevo costo por km debe ser un numero")
    
        self.costo_por_km = costo_por_km
    
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_km (self):
        return self.costo_por_km
    
    def calcular_costo (self, conexion, carga): 
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        if carga < 150000: 
            costo = conexion.distancia * self.costo_por_km + carga * 1 + self.costo_fijo
        elif carga >= 150000: 
            costo = conexion.distancia * self.costo_por_km + carga * 2 + self.costo_fijo
        return costo
    
    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.distancia/self.velocidad)*60
        return tiempo_minutos
    
class Maritimo (Vehiculos): 
    def __init__ (self, capacidad, velocidad, costo_por_km, costo_por_kg, modo = "Maritimo"):
        try: 
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError:
            print("el vehiculo maritimo seleccionado no es valido") 
            
        super().__init__(modo, capacidad)
        self.velocidad = velocidad
        self.costo_por_km = costo_por_km
        self.costo_por_kg = costo_por_kg
        
        
    def set_Velocidad (self, velocidad): 
        try: 
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError: 
            print("la nueva velocidad debe ser un numero")
            
        self.velocidad = velocidad
    
    def setCosto_por_kg (self, costo_por_kg):
        try: 
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo por kg debe ser un numero")
        except TypeError: 
            print ("el nuevo costo por kg debe ser un numero")
            
        self.costo_por_kg = costo_por_kg
    
    def setCosto_por_km (self, costo_por_km): 
        try: 
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
        except TypeError: 
            print ("el nuuevo costo por km debe ser un numero")
    
        self.costo_por_km = costo_por_km
    
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def calcular_costo (self, conexion, carga): 
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        if conexion.valor_restriccion == 'fluvial': 
            costo = conexion.distancia * self.costo_por_km + carga * self.costo_por_kg + 500
        elif conexion.valor_restriccion == 'maritimo':
            costo = conexion.distancia * self.costo_por_km + carga * self.costo_por_kg + 1500
        return costo
    
    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.distancia/self.velocidad)*60
        return tiempo_minutos
    
class Aereo (Vehiculos): 
    def __init__ (self, capacidad, costo_fijo, costo_por_km, costo_por_kg, modo = "Aereo"):
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError:
            print("el vehiculo aereo seleccionado no es valido") 
            
        super().__init__(modo, capacidad)
        self.costo_fijo = costo_fijo
        self.costo_por_km = costo_por_km
        self.costo_por_kg = costo_por_kg
        
        
    def set_Velocidad (self, costo_fijo): 
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError: 
            print("la nueva velocidad debe ser un numero")
            
        self.cosot_fijo = costo_fijo
    
    def setCosto_fijo (self, costo_por_kg):
        try: 
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo por kg debe ser un numero")
        except TypeError: 
            print ("el nuevo costo por kg debe ser un numero")
            
        self.costo_por_kg = costo_por_kg
    
    def setCosto_por_km (self, costo_por_km): 
        try: 
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
        except TypeError: 
            print ("el nuuevo costo por km debe ser un numero")

        self.costo_por_km = costo_por_km
    
    def getCosto_fijo (self): 
        return self.costo_fijo   
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def calcular_costo (self, conexion, carga): 
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        costo = conexion.distancia * self.costo_por_km + self.costo_fijo + carga * self.costo_por_kg
        return costo
        
    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        pass
    

ferroviario = Ferroviario(15000, 100, 100, 3)
automotor = Automotor(30000, 80, 30, 5)
maritimo = Maritimo(100000, 40, 15, 2)
aereo =  Aereo(5000, 750, 40, 10)
