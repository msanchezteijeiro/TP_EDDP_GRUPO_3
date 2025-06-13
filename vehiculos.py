from validaciones import Validaciones
from conexiones import Conexion


class Vehiculo: 
    modos = []

    @classmethod
    def getModos(cls):
        return cls.modos

    def __init__ (self, modo: str, capacidad: float): #que modo sea none y el set de modo este en los subvehiculos REVISARRR
        
        self.setModo(modo) #agregar .lower() si se quiere que sea case insensitive
        self.setCapacidad(capacidad)
        self.modos.append(modo.lower()) #agrega el modo a la lista de modos

    def setModo (self, modo):
        if not Validaciones.validar_str(modo):
            raise TypeError(f"el modo tiene que ser una cadena str")       
        if not Conexion.validar_modo(modo): 
            raise ValueError("el modo no es uno de los cuatro permitidos")
        self.modo = modo.lower() #lower()
    
    def setCapacidad (self, capacidad): 
        if not Validaciones.validar_float (capacidad) and not Validaciones.validar_int (capacidad): 
            raise ValueError (f"la capacidad {capacidad} no es valida")
        self.capacidad = capacidad
    
    def getModo (self): 
        return self.modo

    def getCapacidad (self): 
        return self.capacidad


class Ferroviaria (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_kg, modo ='ferroviaria'):    
        super().__init__(modo, capacidad)
        self.setVelocidad(velocidad)
        self.setCosto_fijo(costo_fijo)
        self.setCosto_por_kg(costo_por_kg)
    
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
        
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_kg (self):
        return self.costo_por_kg

    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')

        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos
    
    def calcular_costo_carga(self, lista_conexiones, carga): #PREGUNTAR LO DE COSTO POR KG!!!!!        
        costo_carga = (carga * self.costo_por_kg)

        return costo_carga

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        if conexion.distancia < 200:
            costo_por_km = 20
        else:
            costo_por_km = 15
        
        costo_tramo_por_vehiculo = (conexion.distancia * costo_por_km) + self.costo_fijo #VER SI USAR GETDISTANCIA

        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)
        
        return costo_tramo
    
    def calcular_tiempo (self, conexion): #CHEQUEAR SI CUANDO SE USAN ESTAS FUNCIONES SE USA UN EXCEPT PARA EL ERROR
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        
        velocidad = self.velocidad #fijo el valor
        if conexion.restriccion == 'velocidad_max': #VER SI USAR GETRESTRICCION!!!
            if self.velocidad > float(conexion.valor_restriccion):
                velocidad = float(conexion.valor_restriccion) #se renombra velocidad en ese tramo si se cumple, si no, no
                #HABRIA QUE HACER UNA VALIDACION DE QUE NO DA ERROR HACER ESTO!! PREGUNTAR

        tiempo_minutos = (conexion.distancia/velocidad)*60
        return tiempo_minutos


class Automotor (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_km, modo = "automotor"):
        super().__init__(modo, capacidad)
        self.setVelocidad(velocidad)
        self.setCosto_fijo(costo_fijo)
        self.setCosto_por_km(costo_por_km)
    
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
    
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_km (self):
        return self.costo_por_km
    
    
    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        capacidad = self.capacidad
        if conexion.restriccion == 'peso_max': #VER SI USAR GETRESTRICCION!!! 
            if self.capacidad > float(conexion.valor_restriccion): #PREGUNTAR SI ACA SE ROMPE O SE DIVIDE EN MAS AUTOS
                capacidad = float(conexion.valor_restriccion) #se renombra capacidad en ese tramo

        cant_vehiculos = (carga + capacidad - 1)//capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    #Funcion auxiliar:
    def calcular_costo_carga_por_vehiculo(self, carga):
        if carga < 15000:
            costo_por_kg = 1
        else:
            costo_por_kg = 2

        costo_carga_por_vehiculo = (carga * costo_por_kg)

        return costo_carga_por_vehiculo

    def calcular_costo_carga(self, lista_conexiones, carga):
        
        capacidad = self.capacidad #REVISAR SI ESTO NO ES MEJOR PARA TODOS LOS VEHICULOS
        
        #Itera sobre la lista de conexiones y busca la menor restriccion de capacidad 
        for conexion in lista_conexiones:
            if not isinstance (conexion, Conexion): 
                raise TypeError ('No se ingreso una conexion valida')

            if conexion.restriccion == 'peso_max': #VER SI USAR GETRESTRICCION!!! 
                if capacidad > float(conexion.valor_restriccion): #PREGUNTAR SI ACA SE ROMPE O SE DIVIDE EN MAS AUTOS
                    capacidad = float(conexion.valor_restriccion) #se renombra capacidad en ese tramo
        
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
        
        costo_tramo_por_vehiculo = (conexion.distancia * self.costo_por_km) + self.costo_fijo #VER SI USAR GETDISTANCIA
        
        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)

        return costo_tramo

    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.distancia/self.velocidad)*60
        return tiempo_minutos


class Fluvial (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_por_km, costo_por_kg, modo = "fluvial"):
        super().__init__(modo, capacidad)
        self.setVelocidad(velocidad)
        self.setCosto_por_km(costo_por_km)
        self.setCosto_por_kg(costo_por_kg)
        
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

    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')

        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    def calcular_costo_carga(self, lista_conexiones, carga): #PREGUNTAR LO DE COSTO POR KG!!!!!
        costo_carga = (carga * self.costo_por_kg)

        return costo_carga

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        if conexion.restriccion == 'tipo': #VER SI USAR GETRESTRICCION!!!
            if conexion.valor_restriccion == 'fluvial': 
                costo_fijo = 500
            elif conexion.valor_restriccion == 'maritimo':
                costo_fijo = 1500
            else:
                raise ValueError (f"El campo obligatorio {conexion.valor_restriccion} vino vacío (None).")
        else:
            raise ValueError (f"El campo obligatorio {conexion.restriccion} vino vacío (None).")
        
        costo_tramo_por_vehiculo = (conexion.distancia * self.costo_por_km) + costo_fijo #VER SI USAR GETDISTANCIA

        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)
        
        return costo_tramo

    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.distancia/self.velocidad)*60
        return tiempo_minutos


class Aerea (Vehiculo): 
    def __init__ (self, capacidad, costo_fijo, costo_por_km, costo_por_kg, modo = "aerea"):
        super().__init__(modo, capacidad)
        self.setCosto_fijo(costo_fijo)
        self.setCosto_por_km(costo_por_km)
        self.setCosto_por_kg(costo_por_kg)
        
    def setCosto_fijo (self, costo_fijo):  
        if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
            raise TypeError ("el costo fijo debe ser un numero")            
        self.cosot_fijo = costo_fijo
    
    def setCosto_por_km (self, costo_por_km): 
        if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
            raise TypeError ("el costo por km debe ser un numero")
        self.costo_por_km = costo_por_km

    def setCosto_por_kg (self, costo_por_kg):
        if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
            raise TypeError ("el costo por kg debe ser un numero")
        self.costo_por_kg = costo_por_kg
    
    def getCosto_fijo (self): 
        return self.costo_fijo   
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    def calcular_costo_carga(self, lista_conexiones, carga): #revisar
        costo_carga = (carga * self.costo_por_kg)

        return costo_carga

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        costo_tramo_por_vehiculo = (conexion.distancia * self.costo_por_km) + self.costo_fijo #VER SI USAR GETDISTANCIA
        
        costo_tramo = costo_tramo_por_vehiculo * self.calcular_cant_vehiculos(conexion, carga)
        
        return costo_tramo
        
    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        
        velocidad = 600

        if conexion.restriccion == "prob_mal_tiempo": #PREGUNTAR BIEN QUE ONDA ESTO!!!!
            float(conexion.valor_restriccion)
            try:
                prob_mal_tiempo = float(conexion.valor_restriccion)
                
                import random
                num_random = random.random()
            
                if num_random < prob_mal_tiempo: #hay mal tiempo, uso menor velocidad
                    velocidad = 400

                #Si num_random es mayor o igual, no hay mal tiempo, me quedo con la mayor velocidad definida antes

            except (ValueError, TypeError): #nos cubrimos de que se haya filtrado un None, "", o algo q no sea numerico.
                print(f"Se definió una restriccion de probabilidad de mal tiempo pero el campo {conexion.valor_restriccion} no posee un valor númerico (int o float). Se asume que no hay restricción.")

        tiempo_minutos = (conexion.distancia/velocidad)*60
        return tiempo_minutos



#DEFINICION DE LOS VEHICULO: NO BORRAR!!
def instanciar_vehiculos():

    try: #no se pasa por parametro aquellos valores que dependen de algo, se calculan por metodos
        ferroviaria = Ferroviaria(150000, 100, 100, 3) #capacidad, velocidad, costo_fijo, costo_por_kg
        automotor = Automotor(30000, 80, 30, 5) #capacidad, velocidad, costo_fijo, costo_por_km
        fluvial = Fluvial(100000, 40, 15, 2) #capacidad, velocidad, costo_por_km, costo_por_kg
        aerea =  Aerea(5000, 750, 40, 10) #capacidad, costo_fijo, costo_por_km, costo_por_kg

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

#Instanciamos las variables: ESTO SE PODRIA MOVER A Itinerarios.py REVISAR!!!
vehiculos_por_modo, ferroviaria, automotor, fluvial, aerea = instanciar_vehiculos()

#TESTEAMOS:
if __name__ == "__main__":
    # código de prueba local_
    print(ferroviaria)
    print(automotor)
    print(fluvial)
    print(aerea)



