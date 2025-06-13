from nodos import Nodo
from validaciones import Validaciones

#conexiones.py

class Conexion():
    #origen  y destino en este caso seria un nodo
    def __init__(self, origen: Nodo, destino: Nodo, modo:str, distancia: int, restriccion = None, valor_restriccion = None):   

        #Seteamos los atributos de la clase:
        self.setOrigen(origen)
        self.setDestino(destino)
        self.setModo(modo)
        self.setDistancia(distancia)
        self.setRestriccion(restriccion)
        self.setValorRestriccion(valor_restriccion)

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
    
    def getDistancia(self):
        return self.distancia
    
    def setRestriccion(self, restriccion):
        if not Validaciones.validar_tipo_restriccion(restriccion):
            raise ValueError(f"Tipo de restriccion no valido: {restriccion}")
        self.restriccion=restriccion

    def getRestriccion(self):
        return self.restriccion
    
    def setValorRestriccion(self, valor_restriccion):
        #esta puede ser vacio, str, int o float, hace falta validar? PREGUNTAR
        if not Validaciones.validar_valor_restriccion(valor_restriccion):
            raise ValueError(f"Valor de restriccion no reconocido: {valor_restriccion}")
        self.valor_restriccion= valor_restriccion
    
    def getValorRestriccion(self):
        return self.valor_restriccion

    def __repr__(self): #CHEQUERA SI ES NECESARIO
        return (f"Conexion({self.getOrigen()} -> {self.getDestino()}, "
                f"modo={self.getModo()}, distancia={self.getDistancia()} km, "
                f"restriccion={self.getRestriccion()}, valor={self.getValorRestriccion()})")
    
    #Validaciones:
    @staticmethod
    def validar_modo (modo):
        modos_validos = {"ferroviaria", "automotor", "fluvial", "aerea"}
        if modo.lower() not in modos_validos:
            return False
        else: 
            return True
        
        
    
    @staticmethod
    def validar_nodo(nodo): 
        if not isinstance (nodo, Nodo):
            return False
        else: 
            return True
        
