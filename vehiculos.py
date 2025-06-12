from validaciones import Validaciones
from conexiones import Conexion

#PREGUNTAR LO DE COSTO POR KG!!!!!
#PREGUNTAR LO DE PROB MAL TIEMPO!!!

class Vehiculo: 
    modos = []

    @classmethod
    def getModos(cls):
        return cls.modos

    def __init__ (self, modo: str, capacidad: float): #que modo sea none y el set de modo este en los subvehiculos
        try: 
            if not Validaciones.validar_str (modo): 
                raise TypeError (f"el modo tiene que ser una cadena str")        
            if not Validaciones.validar_float (capacidad) and not Validaciones.validar_int (capacidad): #ESTA BIEN, con FLOAT solo no alcanza
                raise ValueError (f"la capacidad {capacidad} no es valida")

        except Exception as e: 
            print(f"El Vehiculo no es valido: {e}")
        
        self.modo = modo.lower() #agregar .lower() si se quiere que sea case insensitive
        self.capacidad = capacidad
        self.modos.append(modo.lower()) #agregar el modo a la lista de modos

    def setModo (self, modo):
        try: 
            if not Validaciones.validar_str(modo):
                raise TypeError(f"el modo tiene que ser una cadena str")       
            if not Conexion.validar_modo(modo, Vehiculo.modos): 
                raise ValueError("el modo no es uno de los cuatro permitidos")
        except TypeError as e: 
            print(f"Error: {e}")
        except ValueError as e: 
            print(f"Error: {e}")
         
        self.modo = modo.lower() #lower()
    
    def setCapacidad (self, capacidad): 
        try: 
            if not Validaciones.validar_float (capacidad) and not Validaciones.validar_int (capacidad): 
                raise ValueError (f"la capacidad {capacidad} no es valida")
        except ValueError as e:
            print (f"Error: {e}")
        self.capacidad = capacidad
    
    def getModo (self): 
        return self.modo

    def getCapacidad (self): 
        return self.capacidad


class Ferroviaria (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_fijo, costo_por_kg, modo ='ferroviaria'):
        try: #esto no
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError as e: #esto no (no hay q capturar el error aca.)
            print(f"El vehiculo a seleccionado no es valido: {e}") 
            
        super().__init__(modo, capacidad)
        self.velocidad = velocidad
        self.costo_fijo = costo_fijo
        self.costo_por_kg = costo_por_kg
    
    def setVelocidad (self, velocidad): 
        try: 
            if not Validaciones.validar_int(velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.velocidad = velocidad
    
    def setCosto_fijo (self, costo_fijo):
        try: 
            if not Validaciones.validar_int(costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.costo_fijo = costo_fijo 
    
    def setCosto_por_kg(self, costo_por_kg): 
        try: 
            if not Validaciones.validar_int(costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError as e:
            print(f"Error: {e}")
        
        self.costo_por_kg = costo_por_kg
        
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_kg (self):
        return self.costo_por_kg

    #El error que estoy intentando corregir es que la parte de (carga * self.costo_por_kg) deberia ser general de todo el itinerario
    #El problema para sumarlo directo al final, es...

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        if conexion.distancia < 200:
            costo_por_km = 20
        else:
            costo_por_km = 15
        
        costo_tramo_por_vehiculo = (conexion.distancia * costo_por_km) + self.costo_fijo #VER SI USAR GETDISTANCIA
        
        return costo_tramo_por_vehiculo
    
    def calcular_costo_carga(self, lista_conexiones, carga): #PREGUNTAR LO DE COSTO POR KG!!!!!        
        costo_carga = (carga * self.costo_por_kg)

        return costo_carga

    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')

        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos
    
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
        try: 
            if not Validaciones.validar_int(costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
            if not Validaciones.validar_int(costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
            if not Validaciones.validar_int(velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError as e:
            print(f"El vehiculo aerea seleccionado no es valido: {e}") 
            
        super().__init__(modo, capacidad)
        self.velocidad = velocidad
        self.costo_fijo = costo_fijo
        self.costo_por_km = costo_por_km
        
    def set_Velocidad (self, velocidad): 
        try: 
            if not Validaciones.validar_int(velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.velocidad = velocidad
    
    def setCosto_fijo (self, costo_fijo):
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.costo_fijo = costo_fijo 
    
    def setCosto_por_km (self, costo_por_km): 
        try: 
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo por km debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
    
        self.costo_por_km = costo_por_km
    
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_fijo (self): 
        return self.costo_fijo
    
    def getCosto_por_km (self):
        return self.costo_por_km
    
    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        costo_tramo_por_vehiculo = (conexion.distancia * self.costo_por_km) + self.costo_fijo #VER SI USAR GETDISTANCIA
        
        return costo_tramo_por_vehiculo
    
    #Funcion auxiliar:
    def calcular_costo_carga_por_vehiculo(self, carga):
        if carga < 150000:
            costo_por_kg = 1
        else:
            costo_por_kg = 2

        costo_carga_por_vehiculo = (carga * costo_por_kg)

        return costo_carga_por_vehiculo
    
    """
    def calcular_costo_carga (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        #Esto es para ver que capacidad se usa dependiendo de la restriccion:
        capacidad = self.capacidad
        if conexion.restriccion == 'peso_max': #VER SI USAR GETRESTRICCION!!! 
            if self.capacidad > float(conexion.valor_restriccion): #PREGUNTAR SI ACA SE ROMPE O SE DIVIDE EN MAS AUTOS
                capacidad = float(conexion.valor_restriccion) #se renombra capacidad en ese tramo

        #Aca se calcula el costo por cada vehiculo usado
        cant_vehiculos_entera = self.calcular_cant_vehiculos(conexion, carga)

        carga_restante = carga
        for i in range(cant_vehiculos_entera - 1):
            carga_restante -= capacidad

        costo_carga = (self.calcular_costo_carga_por_vehiculo(capacidad) * cant_vehiculos_entera) + self.calcular_costo_carga_por_vehiculo(carga_restante)

        return costo_carga
    """


    def calcular_costo_carga(self, lista_conexiones, carga):
        
        capacidad = self.capacidad #REVISAR SI ESTO NO ES MEJOR PARA TODOS LOS VEHICULOS
        
        #Itera sobre la lista de conexiones y busca la menor restriccion de capacidad 
        for conexion in lista_conexiones:
            if conexion.restriccion == 'peso_max': #VER SI USAR GETRESTRICCION!!! 
                if capacidad > float(conexion.valor_restriccion): #PREGUNTAR SI ACA SE ROMPE O SE DIVIDE EN MAS AUTOS
                    capacidad = float(conexion.valor_restriccion) #se renombra capacidad en ese tramo
        
        #Aca se calcula el costo por cada vehiculo usado
        cant_vehiculos_entera = self.calcular_cant_vehiculos(conexion, carga)

        carga_restante = carga
        for i in range(int(cant_vehiculos_entera) - 1):
            carga_restante -= capacidad

        costo_carga = (self.calcular_costo_carga_por_vehiculo(capacidad) * cant_vehiculos_entera) + self.calcular_costo_carga_por_vehiculo(carga_restante)

        return costo_carga



    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        capacidad = self.capacidad
        if conexion.restriccion == 'peso_max': #VER SI USAR GETRESTRICCION!!! 
            if self.capacidad > float(conexion.valor_restriccion): #PREGUNTAR SI ACA SE ROMPE O SE DIVIDE EN MAS AUTOS
                capacidad = float(conexion.valor_restriccion) #se renombra capacidad en ese tramo

        cant_vehiculos = (carga + capacidad - 1)//capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.distancia/self.velocidad)*60
        return tiempo_minutos


class Fluvial (Vehiculo): 
    def __init__ (self, capacidad, velocidad, costo_por_km, costo_por_kg, modo = "fluvial"):
        try: 
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError as e:
            print(f"El vehiculo fluvial seleccionado no es valido: {e}") 
            
        super().__init__(modo, capacidad)
        self.velocidad = velocidad
        self.costo_por_km = costo_por_km
        self.costo_por_kg = costo_por_kg
        
        
    def set_Velocidad (self, velocidad): 
        try: 
            if not Validaciones.validar_int (velocidad) and not Validaciones.validar_float(velocidad): 
                raise TypeError ("la velocidad debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.velocidad = velocidad
    
    def setCosto_por_kg (self, costo_por_kg):
        try: 
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo por kg debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.costo_por_kg = costo_por_kg
    
    def setCosto_por_km (self, costo_por_km): 
        try: 
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
    
        self.costo_por_km = costo_por_km
    
    def getVelocidad (self): 
        return self.velocidad
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    

    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        if conexion.restriccion == 'tipo': #VER SI USAR GETRESTRICCION!!!
            if conexion.valor_restriccion == 'fluvial': 
                costo_fijo = 500
            elif conexion.valor_restriccion == 'maritimo':
                costo_fijo = 1500
            else:
                raise ValueError ("El campo obligatorio 'restriccion' vino vacío (None).")
        else:
            raise ValueError ("El campo obligatorio 'restriccion' vino vacío (None).")
        
        costo_tramo_por_vehiculo = (conexion.distancia * self.costo_por_km) + costo_fijo #VER SI USAR GETDISTANCIA
        
        return costo_tramo_por_vehiculo
    
    def calcular_costo_carga(self, lista_conexiones, carga): #PREGUNTAR LO DE COSTO POR KG!!!!!
        costo_carga = (carga * self.costo_por_kg)

        return costo_carga

    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')

        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos

    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        tiempo_minutos = (conexion.distancia/self.velocidad)*60
        return tiempo_minutos


class Aerea (Vehiculo): 
    def __init__ (self, capacidad, costo_fijo, costo_por_km, costo_por_kg, modo = "aerea"):
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo_por_kg debe ser un numero")
        except TypeError as e:
            print(f"El vehiculo aerea seleccionado no es valido: {e}") 
            
        super().__init__(modo, capacidad)
        self.costo_fijo = costo_fijo
        self.costo_por_km = costo_por_km
        self.costo_por_kg = costo_por_kg
        
        
    def setCosto_fijo (self, costo_fijo): 
        try: 
            if not Validaciones.validar_int (costo_fijo) and not Validaciones.validar_float(costo_fijo): 
                raise TypeError ("el costo fijo debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.cosot_fijo = costo_fijo
    
    def setCosto_por_kg (self, costo_por_kg):
        try: 
            if not Validaciones.validar_int (costo_por_kg) and not Validaciones.validar_float(costo_por_kg): 
                raise TypeError ("el costo por kg debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")
            
        self.costo_por_kg = costo_por_kg
    
    def setCosto_por_km (self, costo_por_km): 
        try: 
            if not Validaciones.validar_int (costo_por_km) and not Validaciones.validar_float(costo_por_km): 
                raise TypeError ("el costo_por_km debe ser un numero")
        except TypeError as e: 
            print(f"Error: {e}")

        self.costo_por_km = costo_por_km
    
    def getCosto_fijo (self): 
        return self.costo_fijo   
    
    def getCosto_por_km (self): 
        return self.costo_por_km
    
    def getCosto_por_kg (self):
        return self.costo_por_kg
    
    
    def calcular_costo_tramo (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        costo_tramo_por_vehiculo = (conexion.distancia * self.costo_por_km) + self.costo_fijo #VER SI USAR GETDISTANCIA
        
        return costo_tramo_por_vehiculo
    
    def calcular_costo_carga(self, lista_conexiones, carga): #revisar
        costo_carga = (carga * self.costo_por_kg)

        return costo_carga

    def calcular_cant_vehiculos (self, conexion, carga):
        if not isinstance (conexion, Conexion): 
            raise TypeError ('No se ingreso una conexion valida')
        
        cant_vehiculos = (carga + self.capacidad - 1)//self.capacidad #division con redondeo hacia arriba

        return cant_vehiculos
        
    def calcular_tiempo (self, conexion): 
        if not isinstance (conexion, Conexion):
            raise TypeError ('No se ingreso una conexion valida')
        
        if conexion.restriccion == "prob_mal_tiempo": #PREGUNTAR BIEN QUE ONDA ESTO!!!!
            velocidad = 400
        else: 
            velocidad = 600

        tiempo_minutos = (conexion.distancia/velocidad)*60
        return tiempo_minutos




#DEFINICION DE LOS VEHICULO: NO BORRAR!!

#no se pasa por parametro aquellos valores que dependen de algo, se calculan por metodos

try:
    ferroviaria = Ferroviaria(150000, 100, 100, 3) #capacidad, velocidad, costo_fijo, costo_por_kg
    automotor = Automotor(30000, 80, 30, 5) #capacidad, velocidad, costo_fijo, costo_por_km
    fluvial = Fluvial(100000, 40, 15, 2) #capacidad, velocidad, costo_por_km, costo_por_kg
    aerea =  Aerea(5000, 750, 40, 10) #capacidad, costo_fijo, costo_por_km, costo_por_kg
except TypeError as e:
    print(f"Error: {e}") #print vehiculos invalidos
except Exception as e:
    print(f"Error: {e}")


vehiculos_por_modo = {
    "ferroviaria": ferroviaria,
    "automotor": automotor,
    "fluvial": fluvial,
    "aerea": aerea
}


#TESTEAMOS:
if __name__ == "__main__":
    # código de prueba local_
    print(ferroviaria)
    print(automotor)
    print(fluvial)
    print(aerea)


#TAL VEZ deberiamos tener definidas las funciones de calcular_costo y calcular_tiempo en la clase Vehiculo, 
# y que cada vehiculo las implemente, o sea, que cada vehiculo tenga su propia implementacion de esas funciones.
#PREGUNTAR SI ES NECESARIO

#arreglamos los costos, aunque algunas condiciones me parece que no hacian falta, de las clases de los ferroviarios, fluvial, etc
#quedaron iguales que en la tabla de la consigna 
# parametros como el costo por kilometro habria que pasarlo en el innit
