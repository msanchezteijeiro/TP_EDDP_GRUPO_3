from nodos import Nodo
from validaciones import Validaciones

#conexiones.py

class Conexion():
    #origen  y destino en este caso seria un nodo
    # en este caso el tipo de clase de vehiculos

    def __init__(self, origen: Nodo, destino: Nodo, modo:str, distancia: int, restriccion = None, valor_restriccion = None):
        
        #CHEQUEAR SI LA VAL VA ACA O NO.
        try:
            if not Conexion.validar_nodo(origen):
                raise TypeError (f"el nodo origen {origen} no es valido")
            if not Conexion.validar_nodo(destino):
                raise TypeError (f"el nodo destino {destino} no es valido")
            if not Conexion.validar_modo(modo):
                raise ValueError(f"El modo {modo} no es valido")
            if not(Validaciones.validar_float(distancia)):
                raise TypeError("Se ingreso una distancia inválida.")
            
            restricciones_validas = ["peso_max", "velocidad_max", "prob_mal_tiempo", "tipo", "", None]
            if restriccion is not None and not Validaciones.validar_str(restriccion):
                raise TypeError("La restriccion debe ser una cadena de texto o None.")
            if restriccion not in restricciones_validas:
                raise ValueError(f"Restriccion no reconocida: {restriccion}")
            
        except Exception as e: 
            print (f"La conexion", origen ," ,",destino," ,", modo, " no es valida. Error: {e}")
        
        
        #Seteamos los atributos de la clase:
        
        self.origen = origen
        self.destino = destino 
        self.modo = modo.lower()
        self.distancia = distancia
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion


        #FALTA HACER UN METODO PARA IDENTIFICAR LAS RESTRICCIONES Y ASIGNAR LA CORRECTA SI ES QUE EXISTE


    #Definimos los metodos de la clase:
    def setOrigen(self,origen):
        if not Conexion.validar_nodo(origen):
                raise TypeError (f"el nodo origen {origen} no es valido")
        self.origen = origen

    def getOrigen(self):
        return self.origen
    
    def setDestino(self,destino):
        if not Conexion.validar_nodo(destino):
            raise TypeError (f"el nodo destino {destino} no es valido")
        self.destino = destino

    def getDestino(self):
        return self.destino

    def setModo(self,modo):
        if not Conexion.validar_modo(modo):
            raise ValueError(f"El modo {modo} no es valido")
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
        #esta puede ser vacio, str, int o float, hace falta validar? PREGUNTAR
        self.valor_restriccion= valor
    
    def getValorRestriccion(self):
        return self.valor_restriccion

    
    def __repr__(self): #CHEQUERA SI ES NECESARIO
        return (f"Conexion({self.origen} -> {self.destino}, "
                f"modo={self.modo}, distancia={self.distancia} km, "
                f"restriccion={self.restriccion}, valor={self.valor_restriccion})")
    

    #Validaciones:
    #por ahi conviene hacer un modos_validos = {"aerea", "automotor", "ferroviaria", "fluvial"} porque son estaticos
    @staticmethod
    def validar_modo (modo):
        from vehiculos import Vehiculo  #CHEQUEAR SI ESTO ES VALIDO, me funciono para arreglar importacion circular
        if modo.lower() not in (Vehiculo.getModos()): 
            return False
        else: 
            return True
    
    @staticmethod
    def validar_nodo(nodo): 
        if not isinstance (nodo, Nodo):
            return False
        else: 
            return True
        
