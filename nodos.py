from validaciones import Validaciones


#IMPORTANTE: Ver si hay q validar como validamos a setNombre, a las otras funciones (agregar_conexion, etc)

class Nodo:
    def __init__(self, nombre: str):
        self.setNombre(nombre)
        self.modos_soportados = []  # lista de strs, con los modos ya registrados, ej:"aerea", seria como si ese ciudad tiene o no aeropuerto
        self.vecinos = {}  #es un dict, donde la clave es el destino (str) y el valor es una lista con cada objeto conexion que conecta este nodo con el destino

    def setNombre(self, nombre):
        if Validaciones.validar_nombre(nombre):
            self.nombre = nombre
        else:
            raise ValueError("El nombre del nodo no es valido")
    
    def getNombre(self):
        return  self.nombre
    
    def __repr__(self): #Revisar si es necesario
        return f"Nodo({self.nombre})"

    #tal vez deberia agregar un get vecinos y usarlo en lugar de acceder directamente al atributo vecinos
    #PREGUNTAR SI ES NECESARIO


    def agregar_conexion(self, destino, conexion):#funcion q agrega una conexion al nodo
        #agregar validacion de conexion??
        
        if destino not in self.vecinos: #si el destino no esta en los vecinos, lo agregamos
            self.vecinos[destino] = []

        self.vecinos[destino].append(conexion) #agrega la conexion al diccioario de ese destino

        #Revisamos si el modo estaba en la lista de modos de ese destino, si no estaba lo agregamos.
        if conexion.modo not in self.modos_soportados:
            self.modos_soportados.append(conexion.modo)

    def getVecinos(self):
        return self.vecinos

    def getModosSoportados(self):
        return self.modos_soportados
