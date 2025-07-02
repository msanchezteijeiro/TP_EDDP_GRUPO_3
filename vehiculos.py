import random
from validaciones import Validaciones
from conexiones import Conexion



class Vehiculo: 
    modos = []
    vehiculos = []
    @classmethod
    def getModos(cls):
        return cls.modos
    

    def __init__ (self, capacidad: float, rendimiento: float, modo=None):
        self.modo = modo
        self.setCapacidad(capacidad)
        self.setRendimiento(rendimiento)
        Vehiculo.vehiculos.append(self)
    
    def setCapacidad (self, capacidad): 
        if not Validaciones.validar_float (capacidad) and not Validaciones.validar_int (capacidad): 
            raise ValueError (f"la capacidad {capacidad} no es valida")
        self.capacidad = capacidad
    
    def setRendimiento(self, rendimiento): 
        if not Validaciones.validar_float(rendimiento) and not Validaciones.validar_int(rendimiento) and rendimiento <= 0: 
            raise ValueError (f"el rendimiento {rendimiento} no es valido")
        self.rendimiento = rendimiento
    
    def getModo (self): 
        return self.modo

    def getCapacidad (self): 
        return self.capacidad
    
    def getRendimiento(self): 
        return self.rendimiento
    
    def calcular_cant_vehiculos(self):
        raise NotImplementedError("La subclase debe implementar calcular_cant_vehiculos")

    def calcular_costo_carga(self):
        raise NotImplementedError("La subclase debe implementar calcular_costo_carga")

    def calcular_costo_tramo(self):
        raise NotImplementedError("La subclase debe implementar calcular_costo_tramo")

    def calcular_tiempo(self):
        raise NotImplementedError("La subclase debe implementar calcular_tiempo")
    
    def calcular_combustible(self, distancia, conexion, carga): 
        combustible_usado = self.calcular_cant_vehiculos(conexion, carga) * self.rendimiento * distancia
        return combustible_usado


class Ferroviaria (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_kg, distancia_quiebre, costo_por_km_min, costo_por_km_max, rendimiento, modo='ferroviaria'):    
        super().__init__(capacidad, rendimiento)
        self.setModo (modo)
        self.setVelocidad(velocidad)
        self.setCosto_fijo(costo_fijo)
        self.setCosto_por_kg(costo_por_kg)
        self.setDistancia_quiebre(distancia_quiebre)
        self.setCosto_por_km_min(costo_por_km_min)
        self.setCosto_por_km_max(costo_por_km_max)
        Vehiculo.modos.append(modo.lower())
    
    def setVelocidad (self, velocidad): 
        if not Validaciones.validar_int(velocidad) and not Validaciones.validar_float(velocidad): 
            raise TypeError ("la velocidad debe ser un numero")
        self.velocidad = velocidad
    
    def setCosto_fijo (self, costo_fijo):
        if not Validaciones.validar_int(costo_fijo) and not Validaciones.validar_float(costo_fijo): 
            raise TypeError ("el costo fijo debe ser un numero") 
        self.costo_fijo = costo_fijo 
    
    def setCosto_por_kg(self, costo_por_kg): 
        if not Validaciones.validar_int(costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
            raise TypeError ("el costo_por_kg debe ser un numero")
        self.costo_por_kg = costo_por_kg
    
    def setModo (self, modo):
        if not Validaciones.validar_str(modo):
            raise TypeError(f"el modo tiene que ser una cadena str")       
        if not Conexion.validar_modo(modo): 
            raise ValueError("el modo no es uno de los cuatro permitidos")
        self.modo = modo.lower()
        
    def setDistancia_quiebre (self, distancia_quiebre):
        if not Validaciones.validar_int(distancia_quiebre) and not Validaciones.validar_float(distancia_quiebre): 
            raise TypeError ("la distancia de quiebre debe ser un numero")
        self.distancia_quiebre = distancia_quiebre
    
    def setCosto_por_km_min (self, costo_por_km_min):
        if not Validaciones.validar_int(costo_por_km_min) and not Validaciones.validar_float(costo_por_km_min): 
            raise TypeError ("el costo por km minimo debe ser un numero")
        self.costo_por_km_min = costo_por_km_min
        
    def setCosto_por_km_max (self, costo_por_km_max):
        if not Validaciones.validar_int(costo_por_km_max) and not Validaciones.validar_float(costo_por_km_max): 
            raise TypeError ("el costo por km maximo debe ser un numero")
        self.costo_por_km_max = costo_por_km_max
        
    
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def getDistancia_quiebre (self):
        return self.distancia_quiebre
    
    def getCosto_por_km_min (self):
        return self.costo_por_km_min
    
    def getCosto_por_km_max (self):
        return self.costo_por_km_max
    
    def calcular_cant_vehiculos(self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')

        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos
    
    def calcular_costo_carga(self, lista_conexiones, carga):      
        costo_carga = (carga * self.costo_por_kg)

        return costo_carga

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        if conexion.getDistancia() < self.distancia_quiebre:
            costo_por_km = self.costo_por_km_max
        else:
            costo_por_km = self.costo_por_km_min
        
        costo_tramo_por_vehiculo = (conexion.getDistancia() * costo_por_km) + self.costo_fijo 

        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)
        
        return costo_tramo
    
    def calcular_tiempo (self, conexion):
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        
        velocidad = self.velocidad #fijo el valor
        if conexion.getRestriccion() == 'velocidad_max': 
            if self.velocidad > float(conexion.getValorRestriccion()):
                velocidad = float(conexion.getValorRestriccion()) #se renombra velocidad en ese tramo si se cumple, si no, no

        tiempo_minutos = (conexion.getDistancia()/velocidad)*60
        return tiempo_minutos


class Automotor (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_km, carga_quiebre, costo_por_kg_min, costo_por_kg_max, rendimiento, modo = "automotor"):
        super().__init__(capacidad, rendimiento)
        self.setModo (modo)
        self.setVelocidad(velocidad)
        self.setCosto_fijo(costo_fijo)
        self.setCosto_por_km(costo_por_km)
        self.setCarga_quiebre(carga_quiebre)
        self.setCosto_por_kg_min(costo_por_kg_min)
        self.setCosto_por_kg_max(costo_por_kg_max)
        
        Vehiculo.modos.append(modo.lower())
        
    def setVelocidad (self, velocidad): 
        if not Validaciones.validar_int(velocidad) and not Validaciones.validar_float(velocidad): 
            raise TypeError ("la velocidad debe ser un numero")
        self.velocidad = velocidad
    
    def setCosto_fijo (self, costo_fijo):
        if not Validaciones.validar_int(costo_fijo) and not Validaciones.validar_float(costo_fijo): 
            raise TypeError ("el costo fijo debe ser un numero") 
        self.costo_fijo = costo_fijo 
    
    def setCosto_por_km (self, costo_por_km): 
        if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
            raise TypeError ("el costo por km debe ser un numero")
        self.costo_por_km = costo_por_km
    
    def setModo (self, modo):
        if not Validaciones.validar_str(modo):
            raise TypeError(f"el modo tiene que ser una cadena str")       
        if not Conexion.validar_modo(modo): 
            raise ValueError("el modo no es uno de los cuatro permitidos")
        self.modo = modo.lower()
        
    def setCarga_quiebre (self, carga_quiebre):
        if not Validaciones.validar_int(carga_quiebre) and not Validaciones.validar_float(carga_quiebre): 
            raise TypeError ("la carga de quiebre debe ser un numero")
        self.carga_quiebre = carga_quiebre
        
        
        
    def setCosto_por_kg_min (self, costo_por_kg_min):
        if not Validaciones.validar_int (costo_por_kg_min) and not Validaciones.validar_float(costo_por_kg_min): 
            raise TypeError ("el costo por kg minimo debe ser un numero")
        self.costo_por_kg_min = costo_por_kg_min
        
    def setCosto_por_kg_max (self, costo_por_kg_max):
        if not Validaciones.validar_int (costo_por_kg_max) and not Validaciones.validar_float(costo_por_kg_max): 
            raise TypeError ("el costo por kg maximo debe ser un numero")
        self.costo_por_kg_max = costo_por_kg_max
        
        
    
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_km (self):
        return self.costo_por_km
    
    def getCarga_quiebre (self):
        return self.carga_quiebre
    def getCosto_por_kg_min (self):
        return self.costo_por_kg_min
    def getCosto_por_kg_max (self):
        return self.costo_por_kg_max
    
    def calcular_cant_vehiculos(self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        capacidad = self.capacidad
        if conexion.getRestriccion() == 'peso_max': 
            if self.capacidad > float(conexion.getValorRestriccion()):
                capacidad = float(conexion.getValorRestriccion()) #se renombra capacidad en ese tramo

        cant_vehiculos = (carga + capacidad - 1)//capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    #Funcion auxiliar:
    def calcular_costo_carga_por_vehiculo(self, carga):
        if carga < self.carga_quiebre:
            costo_por_kg = self.costo_por_kg_min
        else:
            costo_por_kg = self.costo_por_kg_max

        costo_carga_por_vehiculo = (carga * costo_por_kg)

        return costo_carga_por_vehiculo

    def calcular_costo_carga(self, lista_conexiones, carga):
        capacidad = self.capacidad
        
        #Itera sobre la lista de conexiones y busca la menor restriccion de capacidad 
        for conexion in lista_conexiones:
            if not isinstance (conexion, Conexion): 
                raise TypeError ('No se ingreso una conexion valida')

            if conexion.getRestriccion() == 'peso_max':
                if capacidad > float(conexion.getValorRestriccion()):
                    capacidad = float(conexion.getValorRestriccion()) #se renombra capacidad en ese tramo
        
        #Aca se calcula el costo por cada vehiculo usado
        cant_vehiculos = int((carga + capacidad - 1)//capacidad) #division con redondeo hacia arriba
        cant_vehiculos_llenos = cant_vehiculos - 1

        carga_restante = carga
        for i in range(cant_vehiculos_llenos):
            carga_restante -= capacidad

        costo_carga = (self.calcular_costo_carga_por_vehiculo(capacidad) * cant_vehiculos_llenos) + (self.calcular_costo_carga_por_vehiculo(carga_restante))
        return costo_carga

    def calcular_costo_tramo(self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        costo_tramo_por_vehiculo = (conexion.getDistancia() * self.costo_por_km) + self.costo_fijo 
        
        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)
        return costo_tramo

    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.getDistancia()/self.velocidad)*60
        return tiempo_minutos


class Fluvial (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_por_km, costo_por_kg, costo_fijo_fluvial, costo_fijo_maritimo, rendimiento, modo = "fluvial"):
        super().__init__(capacidad, rendimiento)
        self.setModo(modo)
        self.setVelocidad(velocidad)
        self.setCosto_por_km(costo_por_km)
        self.setCosto_por_kg(costo_por_kg)
        self.setCosto_fijo_fluvial(costo_fijo_fluvial)
        self.setCosto_fijo_maritimo(costo_fijo_maritimo)
        
        Vehiculo.modos.append(modo.lower())
        
    def setVelocidad (self, velocidad): 
        if not Validaciones.validar_int(velocidad) and not Validaciones.validar_float(velocidad): 
            raise TypeError ("la velocidad debe ser un numero")
        self.velocidad = velocidad
    
    def setCosto_por_km (self, costo_por_km): 
        if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
            raise TypeError ("el costo por km debe ser un numero")
        self.costo_por_km = costo_por_km

    def setCosto_por_kg (self, costo_por_kg):
        if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
            raise TypeError ("el costo por kg debe ser un numero")
        self.costo_por_kg = costo_por_kg
        
    def setModo (self, modo):
        if not Validaciones.validar_str(modo):
            raise TypeError(f"el modo tiene que ser una cadena str")       
        if not Conexion.validar_modo(modo): 
            raise ValueError("el modo no es uno de los cuatro permitidos")
        self.modo = modo.lower()

    def setCosto_fijo_fluvial (self, costo_fijo_fluvial): 
        if not Validaciones.validar_int (costo_fijo_fluvial) and not Validaciones.validar_float(costo_fijo_fluvial): 
            raise TypeError ("el costo fijo fluvial debe ser un numero")
        self.costo_fijo_fluvial = costo_fijo_fluvial

    def setCosto_fijo_maritimo (self, costo_fijo_maritimo): 
        if not Validaciones.validar_int (costo_fijo_maritimo) and not Validaciones.validar_float(costo_fijo_maritimo): 
            raise TypeError ("el costo fijo maritimo debe ser un numero")
        self.costo_fijo_maritimo = costo_fijo_maritimo


    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def getCosto_fijo_fluvial (self):
        return self.costo_fijo_fluvial
    
    def getCosto_fijo_maritimo (self):
        return self.costo_fijo_maritimo
    

    def calcular_cant_vehiculos(self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')

        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    def calcular_costo_carga(self, lista_conexiones, carga):
        costo_carga = (carga * self.getCosto_por_kg())

        return costo_carga

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        if conexion.getRestriccion() == 'tipo':
            if conexion.getValorRestriccion() == 'fluvial': 
                costo_fijo = self.getCosto_fijo_fluvial()
            elif conexion.getValorRestriccion() == 'maritimo':
                costo_fijo = self.getCosto_fijo_maritimo()
            else:
                raise ValueError (f"El campo obligatorio {conexion.getValorRestriccion()} vino vacío (None).")
        else:
            raise ValueError (f"El campo obligatorio {conexion.getRestriccion()} vino vacío (None).")
        
        costo_tramo_por_vehiculo = (conexion.getDistancia() * self.getCosto_por_km()) + costo_fijo

        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)
        
        return costo_tramo

    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.getDistancia()/self.velocidad)*60
        return tiempo_minutos


class Aerea (Vehiculo): 
    def __init__ (self, capacidad, costo_fijo, costo_por_km, costo_por_kg, vel_buen_tiempo, vel_mal_tiempo, rendimiento, modo = "aerea"):
        super().__init__(capacidad, rendimiento)
        self.setModo(modo)
        self.setCosto_fijo(costo_fijo)
        self.setCosto_por_km(costo_por_km)
        self.setCosto_por_kg(costo_por_kg)
        self.setVel_buen_tiempo(vel_buen_tiempo)
        self.setVel_mal_tiempo(vel_mal_tiempo)
        
        Vehiculo.modos.append(modo.lower())
        
    def setCosto_fijo (self, costo_fijo):  
        if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
            raise TypeError ("El costo fijo debe ser un numero")            
        self.costo_fijo = costo_fijo
    
    def setCosto_por_km (self, costo_por_km): 
        if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
            raise TypeError ("el costo por km debe ser un numero")
        self.costo_por_km = costo_por_km

    def setCosto_por_kg (self, costo_por_kg):
        if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
            raise TypeError ("el costo por kg debe ser un numero")
        self.costo_por_kg = costo_por_kg
        
    def setModo (self, modo):
        if not Validaciones.validar_str(modo):
            raise TypeError(f"el modo tiene que ser una cadena str")       
        if not Conexion.validar_modo(modo): 
            raise ValueError("el modo no es uno de los cuatro permitidos")
        self.modo = modo.lower()

    def setVel_buen_tiempo (self, vel_buen_tiempo): 
        if not Validaciones.validar_int(vel_buen_tiempo) and not Validaciones.validar_float(vel_buen_tiempo): 
            raise TypeError ("la velocidad debe ser un numero")
        self.vel_buen_tiempo = vel_buen_tiempo

    def setVel_mal_tiempo (self, vel_mal_tiempo): 
        if not Validaciones.validar_int(vel_mal_tiempo) and not Validaciones.validar_float(vel_mal_tiempo): 
            raise TypeError ("la velocidad debe ser un numero")
        self.vel_mal_tiempo = vel_mal_tiempo

        
    def getCosto_fijo (self): 
        return self.costo_fijo   
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def getVel_buen_tiempo (self): 
        return self.vel_buen_tiempo
    
    def getVel_mal_tiempo (self): 
        return self.vel_mal_tiempo

    
    def calcular_cant_vehiculos(self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    def calcular_costo_carga(self, lista_conexiones, carga):
        costo_carga = (carga * self.getCosto_por_kg())

        return costo_carga

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        costo_tramo_por_vehiculo = (conexion.getDistancia() * self.getCosto_por_km()) + self.getCosto_fijo()
        
        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)
        
        return costo_tramo
        
    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        
        velocidad = self.getVel_buen_tiempo()
        if conexion.getRestriccion() == "prob_mal_tiempo":
            
            try:
                prob_mal_tiempo = float(conexion.getValorRestriccion())
                if not(0<=prob_mal_tiempo<=1):
                    raise ValueError
                
                num_random = random.random()
                if num_random < prob_mal_tiempo: #hay mal tiempo, uso menor velocidad
                    velocidad = self.getVel_mal_tiempo()

                #si num_random es mayor o igual, no hay mal tiempo, me quedo con la mayor velocidad definida antes

            except (ValueError, TypeError): #nos cubrimos de que se haya filtrado un None, "", o algo q no sea numerico.
                raise ValueError("La probabilidad de mal tiempo no es un valor numérico entre 0 y 1.")
        tiempo_minutos = (conexion.getDistancia()/velocidad)*60
        return tiempo_minutos



#definicion de los vehiculos
def instanciar_vehiculos():

    try: #no se pasa por parametro aquellos valores que dependen de algo, se calculan por metodos
        ferroviaria = Ferroviaria(150000, 100, 100, 3, 200, 15, 20, 3) #capacidad, velocidad, costo_fijo, costo_por_kg, distancia_quiebre, costo_por_km_min, costo_por_km_max, rendimiento
        automotor = Automotor(30000, 80, 30, 5, 15000, 1, 2, 2) #capacidad, velocidad, costo_fijo, costo_por_km, carga_quiebre, costo_por_kg_min, costo_por_kg_max, rendimiento
        fluvial = Fluvial(100000, 40, 15, 2, 500, 1500, 45) #capacidad, velocidad, costo_por_km, costo_por_kg, costo_fijo_fluvial, costo_fijo_maritimo, rendimiento
        aerea =  Aerea(5000, 750, 40, 10, 600, 400, 3.5) #capacidad, costo_fijo, costo_por_km, costo_por_kg, vel_buen_tiempo, vel_mal_tiempo, rendimiento

        vehiculos_por_modo = {
            "ferroviaria": ferroviaria,
            "automotor": automotor,
            "fluvial": fluvial,
            "aerea": aerea
        }

    except TypeError as e:
        print(f"Error: {e}") #print vehiculos invalidos
    except Exception as e:
        print(f"Error: {e}")

    return vehiculos_por_modo, ferroviaria, automotor, fluvial, aerea


