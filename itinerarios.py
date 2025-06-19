from redes import construir_red
from vehiculos import Vehiculo, vehiculos_por_modo #creo que Vehiculo se puede sacar porque no lo llamamos en nigun momento
from nodos import Nodo
from conexiones import Conexion
#creo que no hace falta importar estas clases pero no se, lo dejo por las dudas

#Definimos clase Itinerario:
class Itinerario: #LE FALTAN GETS A LAS COSAS (SOBRE todo AL TIEMPO Y CARGA PARA LOS KPI) REVISARRR
    def __init__(self, modo: str, camino: list, costo: float, tiempo: float):
        
        self.setModo(modo)
        self.setCamino(camino)
        self.setCosto(costo)
        self.setTiempo(tiempo)

    def setModo(self, modo):
        self.modo = modo

    def setCamino(self, camino):
        self.camino = camino

    def setCosto(self, costo):
        self.costo = costo

    def setTiempo(self, tiempo):
        self.tiempo = tiempo

    def getModo(self):
        return self.modo

    def getCamino(self):
        return self.camino

    def getCosto(self):
        return self.costo

    def getTiempo(self):
        return self.tiempo
    #ver si hace falta validar algo, yp diria que no, son todos datos ya validados previamente PREGUNTAR!!

    def __repr__(self):
        rec_fin = [self.getCamino()[0].getOrigen().getNombre()]
        for conexion in self.getCamino():
            rec_fin.append(conexion.getDestino().getNombre())
        camino_str = " -> ".join(rec_fin)
        #aca c.getOrigen() trae un nodo y el getNombre trae el nombre de ese nodo. lo mismo para el destino
        SANGRIA = "  "
        return (f"{SANGRIA}● Modo: {self.modo.capitalize()}\n"
                f"{SANGRIA}● Itinerario: {camino_str}\n"
                f"{SANGRIA}● Costo Total: ${self.costo:.2f}\n"
                f"{SANGRIA}● Tiempo Total (min): {self.tiempo:.2f} minutos\n"
                f"{SANGRIA}● Tiempo Total (HH:MM:SS): {self.formatear_tiempo_minutos(self.tiempo)}")
    
    @staticmethod
    def formatear_tiempo_minutos(tiempo_en_min):
        from datetime import timedelta
        return str(timedelta(minutes=tiempo_en_min))
    

# Definimos la función que busca todos los caminos posibles entre dos nodos, con un solo modo de transporte y sin ciclos
def construir_itinerario(nodos, solicitud_tupla): #nodos es un..., solicitud_tupla es una tupla con id_carga y datos
    
    itinerarios_base = {}

    # Extraemos de la tupla, el diccionario datos (el id no nos interesa por ahora)
    _, datos = solicitud_tupla #pues se que no usare id_carga
    
    origen = datos["origen"]        #extraigo el origen y destino de la solicitud
    destino = datos["destino"]

    # Lista de modos disponibles construida a partir del nodo origen:
    modos_disponibles = nodos[origen].getModosSoportados()
        #nos traemos los modos de transporte que soporta el nodo origen, q son los unicos que podemos usar para buscar caminos

    # Función recursiva para buscar caminos:
    def buscador_caminos(actual, destino, camino, visitados, modo):
        # Caso base: si llegamos al destino, guardamos el camino actual
        if actual == destino:
            if modo not in itinerarios_base:
                itinerarios_base[modo] = []
            itinerarios_base[modo].append(list(camino))  # copiamos el camino actual
            return

        # Marcamos el nodo como visitado (agregamos a la lista)
        visitados.append(actual)

        # Recorremos todos los vecinos del nodo actual
        for vecino, conexiones in nodos[actual].getVecinos().items(): #nodos[actual].getVecinos().items() (por ahi podemos hacer un getVecinos())

            # Si el vecino ya fue visitado, lo salteamos para evitar ciclos
            if vecino in visitados:
                continue

            # Recorremos todas las conexiones hacia ese vecino
            for conexion in conexiones:
                # Si el modo coincide con el modo actual...
                if conexion.getModo() == modo:
                    camino.append(conexion)              # agregamos la conexión al camino actual
                    buscador_caminos(vecino, destino, camino, visitados, modo)  # llamamos recursivamente desde el vecino
                    camino.pop()                         # volvemos para atrás (backtracking)

        visitados.pop() # Desmarcamos el nodo actual para permitir su uso en otros caminos

    # Recorremos todos los modos posibles y buscamos caminos para cada uno, con la funcion recursiva definida arriba
    for modo in modos_disponibles:
        if origen in nodos and destino in nodos:
            buscador_caminos(actual=origen, destino=destino, camino=[], visitados=[], modo=modo)

    return itinerarios_base #itinerarios_base es un diccionario, en el que la clave es "modo" y el valor es lista de las conexiones que usa ese camino
                       #Ejemplo: {...,'fluvial': [[Conexion(Nodo(Zarate) -> Nodo(Buenos_Aires)), Conexion(Nodo(Buenos_Aires) -> Nodo(Mar_del_Plata)]],...}
                        #Del modo fluvial hay un solo itinerario, que va de Zarate a Buenos Aires y de ahi a Mar del Plata.


#AGREGAMOS EL TEMA DE COSTOS:
def calcular_costos_y_tiempos(itinerarios_base, carga_kg):
    itinerarios_final = {}
    id_actual = 1

    for modo, caminos in itinerarios_base.items(): #modo es un str, caminos una lista de listas con las conexiones.
        vehiculo = vehiculos_por_modo.get((modo.lower())) #del diccionario vehiculos_por_modo, se el objeto vehiculo correspondiente al modo
        if vehiculo is None:
            continue #osea si no existe ese vehiculo este ni siquiera es analizado, ni aparecera en el dict "itinerarios_final" devuelto

        for camino in caminos: #camino es una lista de objetos conexion
            costo_total_camino = vehiculo.calcular_costo_carga(camino, carga_kg)
            tiempo_total_camino = 0

            for conexion in camino:
                costo_total_camino += vehiculo.calcular_costo_tramo(conexion, carga_kg)
                tiempo_total_camino += vehiculo.calcular_tiempo(conexion)
            info = Itinerario(modo, camino, costo_total_camino, tiempo_total_camino)
            itinerarios_final[id_actual] = info
            id_actual += 1

    return itinerarios_final #es un dict: clave: id, valor: objeto itinerario correspondiente


#Funcion unificada que llamo desde el main:

def itinerario_por_solicitud(nodos_existentes, solicitud_tupla):
    itinerario_sin_costos = construir_itinerario(nodos_existentes, solicitud_tupla)
    # Extraemos de la tupla, el diccionario datos
    _, datos = solicitud_tupla #pues se que no usare id_carga
    
    itinerarios_final_por_solicitud = calcular_costos_y_tiempos(itinerario_sin_costos, datos["peso_kg"]) #asi aca en el main sale una sola
    
    return itinerarios_final_por_solicitud



#Funcion para imprimir tabla itinerarios
def imprimir_itinerario_final(itinerarios_final):

    if not itinerarios_final:
        print(f"\nNo existen itinerarios posibles para la solicitud pedida.")

    else:
        print("")
        print(f"{'ID':<4} | {'Modo':<12} | {'Costo Total':<12} | {'Tiempo Total (min)':<20} | Itinerario")
        print("-" * 125)
        
        for id_, itinerario in itinerarios_final.items():
            camino_limpio = [itinerario.getCamino()[0].getOrigen().getNombre()] #empiezo lista con el primer nodo origen 
            
            camino_limpio += [c.getDestino().getNombre() for c in itinerario.getCamino()] #le agregamos solo los destinos de cada conexion
            camino_str = " → ".join(camino_limpio) #transformamos la lista final en un str
            print(f"{id_:<4} | {itinerario.getModo().capitalize():<12} | ${itinerario.getCosto():<11.2f} | {itinerario.getTiempo():<20.2f} | {camino_str}")



#Este es el del timepo que le pasa como parametro el diccionario con los posibles caminos
def kpi_1(itinerarios_final):

    if not itinerarios_final:
        return None #como tiene un return, si entra a este if, termina la funcion

    tiempo_min = float('inf')
    id_res = None
    res = None
    for (id, itinerario) in itinerarios_final.items():
        if itinerario.getTiempo() < tiempo_min:
            tiempo_min = itinerario.getTiempo()
            id_res = id
            res = itinerario
    par_res = (id_res, res) #tupla
    return par_res


#Este es el del costo: devuelve el camino con menor costo total
def kpi_2(itinerarios_final): 

    if not itinerarios_final:
        return None #como tiene un return, si entra a este if, termina la funcion

    costo_min = None
    id_res = None
    res = None
    for id, itinerario in itinerarios_final.items():
        if costo_min is None:
            costo_min = itinerario.getCosto()
            id_res = id
            res = itinerario
        elif itinerario.getCosto() < costo_min:
            costo_min = itinerario.getCosto()
            id_res = id
            res = itinerario
    par_res = (id_res, res) #tupla

    return par_res 



#Funciones para imprimir KPIs:

def imprimir_kpi_1(par_res):
    if not par_res:
        print("\n\nNo hay itinerarios disponibles para KPI 1.")
    else:
        id_res = par_res[0]
        res = par_res[1]
        print("\n\nMEJOR ITINERARIO SEGÚN: → | KPI 1: Minimizar el Tiempo Total de Entrega |")
        print("-" * 72)
        print(f"El itinerario {id_res} es el mejor.\n")
        print(res)

def imprimir_kpi_2(par_res):
    if not par_res:
        print("\n\nNo hay itinerarios disponibles para KPI 2.")
    else:
        id_res = par_res[0]
        res = par_res[1]
        print("\n\nMEJOR ITINERARIO SEGÚN: → | KPI 2: Minimizar el Costo Total del Transporte |")
        print("-" * 75)
        print(f"El itinerario {id_res} es el mejor.\n")
        print(res)




