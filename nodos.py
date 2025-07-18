from validaciones import Validaciones



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



    def agregar_conexion(self, destino, conexion):#funcion q agrega una conexion al nodo
        
        if destino not in self.vecinos: #si el destino no esta en los vecinos, lo agregamos
            self.vecinos[destino] = []

        self.vecinos[destino].append(conexion) #agrega la conexion al diccioario de ese destino

        #Revisamos si el modo estaba en la lista de modos de ese destino, si no estaba lo agregamos.
        if conexion.getModo() not in self.modos_soportados:
            self.modos_soportados.append(conexion.getModo())

    def getVecinos(self):
        return self.vecinos

    def getModosSoportados(self):
        return self.modos_soportados
