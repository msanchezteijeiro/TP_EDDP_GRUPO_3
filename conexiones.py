from nodos import Nodo
from validaciones import Validaciones

class Conexion():
    #origen  y destino en este caso seria un nodo
    # en este caso el tipo de clase de vehiculos

    def __init__(self, origen: Nodo, destino: Nodo, modo, distancia: int, restriccion = None, valor_restriccion = None):
        
        #CHEQUEAR SI LA VAL VA ACA O NO.
        try:
            if not Conexion.validar_nodo(origen) and not Conexion.validar_nodo(destino):
                raise TypeError ("el destino y el origen no son nodos validos")
            if not Conexion.validar_modo(modo): 
                raise ValueError ("el modo no es valido")
        except TypeError: 
            print (f"la conexion", origen ," ,",destino," ,", modo, " no es valida")
        except ValueError:
            print (f"el modo",modo, "no es valido") 
        
        
        #Seteamos los atributos de la clase:
        
        self.origen = origen
        self.destino = destino 
        self.modo = modo
        self.distancia = distancia
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion


        #FALTA HACER UN METODO PARA IDENTIFICAR LAS RESTRICCIONES Y ASIGNAR LA CORRECTA SI ES QUE EXISTE


    #Definimos los metodos de la clase:
    def setOrigen(self,origen):
        """
        if not(Validaciones.validar_nodo(origen)):   #FALTA DEFINIR validar_nodo en validaciones.py Y FALTA UN TRY PARA ESE RAISERROR
            raise TypeError("No existe este nodo origen.")
        """
        self.origen = origen

    def getOrigen(self):
        return self.origen
    
    def setDestino(self,destino):
        """
        if not(Validaciones.validar_nodo(destino)):   #FALTA DEFINIR validar_nodo en validaciones.py
            raise TypeError("No existe este nodo destino.")
        """
        self.destino = destino

    def getDestino(self):
        return self.destino

    def setModo(self,modo):
        """
        if not(Validaciones.validar_modo(modo)):  #FALTA DEFINIR validar_modo en validaciones.py
            raise TypeError("No existe este modo para estos nodos origen y destino.")
        """
        self.modo = modo.lower() #lower para que no haya errores con mayusculas y minusculas

    def getModo(self):
        return self.modo

    def setDistancia(self,distancia):
        if not(Validaciones.validar_float(distancia)):
            raise TypeError("Se ingreso una distancia inválida.")
        self.distancia = distancia
    
    #YA FUNCIONA! Tal vez convendria ponerla en validaciones.py, y llamarla desde ahi, asi no ocupa tanto espacio.
    def setRestriccion(self, restriccion):
        #como solo hay 4 restricciones o vacio. creo la lista con las restrcciones validas
        #por ahi conviene usar la val de str, como esta la posibilidad de vacio no la uso por las dudas
        #preguntar si tiene sentido que sea None
        restricciones_validas = ["peso_max", "velocidad_max", "prob_mal_tiempo", "tipo", "", None]

        if restriccion is not None and not Validaciones.validar_str(restriccion):
            raise TypeError("La restriccion debe ser una cadena de texto o None.")

        if restriccion not in restricciones_validas:
            raise ValueError(f"Restriccion no reconocida: {restriccion}")
    
        self.restriccion=restriccion

    def getRestriccion(self):
        return self.restriccion
    
    def setValorRestriccion(self, valor):
        #esta puede ser vacio, str, int o float, hace falta validar?
        self.valor_restriccion= valor
    
    def getValorRestriccion(self):
        return self.valor_restriccion

    
    def __repr__(self): #CHEQUERA SI ES NECESARIO
        return (f"Conexion({self.origen} -> {self.destino}, "
                f"modo={self.modo}, distancia={self.distancia} km, "
                f"restriccion={self.restriccion}, valor={self.valor_restriccion})")
    

    #Validaciones:
    
    def validar_modo (modo):
        from vehiculos import Vehiculo  #CHEQUEAR SI ESTO ES VALIDO, me funciono para arreglar importacion circular
        if modo.lower() not in (Vehiculo.getModos()): 
            return False
        else: 
            return True
        
    def validar_nodo(nodo): 
        if not isinstance (nodo, Nodo):
            return False
        else: 
            return True
        
    
 


#Lo de aca abajo va aca?


#lo de la restriccion deberia ser asi:
# si tiene restriccion, el dato restriccion sera el tipo, y lo siguiente sera la restriccion en si misma

import csv

def abrir_csv(nombre_csv):
    origen, destino, tipo, distancia, restriccion, valor_restriccion=[],[],[],[],[],[]
    try:
        with open(nombre_csv,"r", encoding="UTF-8") as archivo:
            lector=csv.reader(archivo)
            for fila in lector:
                origen.append(fila[0])
                destino.append(fila[1])
                tipo.append(fila[2])
                distancia.append(fila[3])
                restriccion.append(fila[4])
                valor_restriccion.append(fila[5])
            print("Se crearon las listas")
    except:
        print("Ocurrio un error.")
    return origen[1:], destino[1:], tipo[1:], distancia[1:], restriccion[1:], valor_restriccion[1:]
