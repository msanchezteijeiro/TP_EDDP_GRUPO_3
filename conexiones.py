import csv
from nodos import Nodo
from validaciones import Validaciones as Val
class Conexion():
    #origen  y destino en este caso seria un nodo
    # en este caso el tipo de clase de vehiculos

    def __init__(self, origen: Nodo, destino: Nodo, tipo, distancia: int, restriccion = None, valor_restriccion = None):
        if not(Val.validar_Nodos(origen)):
            raise TypeError("No existe este nodo origen.")
        if not(Val.validar_Nodos(destino)):
            raise TypeError("No existe este nodo destino.")
        if not(Val.validar_Tipos(tipo)):
            raise TypeError("No existe este nodo tipo de vehiculo.")
        if not(Val.validar_int(distancia)):
            raise TypeError("No existe este nodo tipo de vehiculo.")
        self.setOrigen(origen)
        self.setDestino(destino)
        self.setTipo(tipo)    
        self.setDistancia(distancia)
    def setOrigen(self,origen):
        if not(Val.validar_Nodos(origen)):
            raise TypeError("No existe este nodo origen.")
        self.origen = origen

    def getOrigen(self):
        return self.origen
    
    def setOrigen(self,destino):
        if not(Val.validar_Nodos(destino)):
            raise TypeError("No existe este nodo destino.")
        self.destino = destino

    def getDestino(self):
        return self.destino

    def setTipo(self,tipo):
        if not(Val.validar_Tipos(tipo)):
            raise TypeError("No existe este nodo tipo de vehiculo.")
        self.tipo = tipo

    def getTipo(self):
        return self.tipo

    def setDistancia(self,distancia):
        if not(Val.validar_int(distancia)):
            raise TypeError("No existe este nodo tipo de vehiculo.")
        self.distancia = distancia
        
    
    
    























#lo de la restriccion deberia ser asi:
# si tiene restriccion, el dato restriccion sera el tipo, y lo siguiente sera la restriccion en si misma

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
