from redes import construir_red
from vehiculos import Vehiculo, vehiculos_por_modo

#Definimos clase Itinerario:

class Itinerario:
    def __init__(self, modo: str, camino: list, costo: float, tiempo: float):
        #crear esto para guardar mejor la informacion del itinerario
        #preguntar si hace falta validar
        #agregar getters y setters??
        self.modo = modo
        self.camino = camino
        self.costo = costo
        self.tiempo = tiempo

        
    def __repr__(self):
        camino_str = " -> ".join(
            f"{c.origen.nombre} → {c.destino.nombre} ({c.distancia} km)" for c in self.camino
        )
        return (f"Modo: {self.modo}\n"
                f"Camino: {camino_str}\n"
                f"Costo Total: ${self.costo:.2f}\n"
                f"Tiempo Total: {self.tiempo:.2f} minutos")



# Definimos la función que busca todos los caminos posibles entre dos nodos, con un solo modo de transporte y sin ciclos

def construir_itinerario(nodos, solicitud):
    """
    Dada una solicitud, encuentra todos los caminos posibles entre origen y destino,
    respetando:
    - el mismo modo de transporte en todo el camino
    - que no se repita ningún nodo

    Parámetros:
    - nodos: diccionario con los objetos Nodo instanciados
    - solicitud: diccionario con formato {'CARGA_001': {'peso_kg': 70000.0, 'origen': 'Zarate', 'destino': 'Mar_del_Plata'}}

    Devuelve:
    - diccionario con claves = modo de transporte, valores = lista de caminos posibles (cada uno como lista de conexiones)
    """
    
    resultados = {}

    # Extraemos el único valor de la solicitud
    datos = list(solicitud.values())[0] #extraemos el primer (y único) valor del diccionario de solicitud
                                        #osea "datos" es un diccionario con los datos de la solicitud
    
    origen = datos["origen"]        #extraigo el origen y destino de la solicitud
    destino = datos["destino"]

    # Lista de modos disponibles construida a partir del nodo origen:
    modos_disponibles = nodos[origen].modos_soportados
        #nos traemos los modos de transporte que soporta el nodo origen, q son los unicos que podemos usar para buscar caminos


    # Función recursiva para buscar caminos:
    def buscador_caminos(actual, destino, camino, visitados, modo):
        # Caso base: si llegamos al destino, guardamos el camino actual
        if actual == destino:
            if modo not in resultados:
                resultados[modo] = []
            resultados[modo].append(list(camino))  # copiamos el camino actual
            return

        # Marcamos el nodo como visitado (agregamos a la lista)
        visitados.append(actual)

        # Recorremos todos los vecinos del nodo actual
        for vecino, conexiones in nodos[actual].vecinos.items():

            # Si el vecino ya fue visitado, lo salteamos para evitar ciclos
            if vecino in visitados:
                continue

            # Recorremos todas las conexiones hacia ese vecino
            for conexion in conexiones:
                # Si el modo coincide con el modo actual...
                if conexion.modo == modo:
                    camino.append(conexion)              # agregamos la conexión al camino actual
                    buscador_caminos(vecino, destino, camino, visitados, modo)  # llamamos recursivamente desde el vecino
                    camino.pop()                         # volvemos para atrás (backtracking)

        # Desmarcamos el nodo actual para permitir su uso en otros caminos
        visitados.pop()


    # Recorremos todos los modos posibles y buscamos caminos para cada uno, con la funcion recursiva definida arriba
    for modo in modos_disponibles:
        if origen in nodos and destino in nodos:
            buscador_caminos(actual=origen, destino=destino, camino=[], visitados=[], modo=modo)

    return resultados #resultados es un diccionario, en el que la clave es "modo" y el valor es lista de las conexiones que usa ese camino
                       #Ejemplo: {...,'fluvial': [[Conexion(Nodo(Zarate) -> Nodo(Buenos_Aires)), Conexion(Nodo(Buenos_Aires) -> Nodo(Mar_del_Plata)]],...}
                        #Del modo fluvial hay un solo itinerario, que va de Zarate a Buenos Aires y de ahi a Mar del Plata.

#preguntar por temas de complejidad, igual si es una red de grafos chica, no deberia dar problema 

#AGREGAMOS EL TEMA DE COSTOS:



def calcular_costos_y_tiempos(resultados, carga_kg): #cambie esta funcion para que evaluados salga como un diccionario que tenga como clave un id 
    #y que guarde como valor, el objeto de la clase infromacion recien creada. esto baja la complejidad de lo que estmaos haciendo 
    evaluados = {}
    id_actual = 1

    for modo, caminos in resultados.items(): #modo es un str, caminos una lista de listas con las conexiones.
        vehiculo = vehiculos_por_modo.get((modo.lower())) #del diccionario vehiculos_por_modo, se el objeto vehiculo correspondiente al modo
        if vehiculo is None:
            continue #osea si no existe ese vehiculo este ni siquiera es analizado, ni aparecera en el dict "evaluados" devuelto

        for camino in caminos: #camino es una lista de objetos conexion
            costo_total = 0
            tiempo_total = 0
            for conexion in camino:
                try:
                    costo_total += vehiculo.calcular_costo(conexion, carga_kg)
                    tiempo_total += vehiculo.calcular_tiempo(conexion)
                except Exception as e:
                    print(f"Error al calcular para {conexion}: {e}")
                    continue

            info = Itinerario(modo, camino, costo_total, tiempo_total)
            evaluados[id_actual] = info
            id_actual += 1

    return evaluados



def imprimir_costos_y_tiempos(evaluados):
    print(f"{'ID':<4} | {'Modo':<12} | {'Costo Total':<12} | {'Tiempo Total (min)':<20} | Camino")
    print("-" * 100)
    
    for id_, info in evaluados.items(): #CHEQUEAR SI HAY Q USAR LOS GETS de origen y nombre (de conexion y nodo)
        camino_limpio = [info.camino[0].origen.nombre] #empiezo lista con el primer nodo origen 
        camino_limpio += [c.destino.nombre for c in info.camino] #le agregamos solo los destinos de cada conexion
        camino_str = " → ".join(camino_limpio) #transformamos la lista final en un str

        print(f"{id_:<4} | {info.modo:<12} | ${info.costo:<11.2f} | {info.tiempo:<20.2f} | {camino_str}")




def kp1(evaluados):
    #este es el del timepo que le pasa como parametro el diccionario con los posibles caminos
    #el costo total esta mal pero el timepo bien
    tiempo_min = 0
    res = None
    for (clave, valor) in evaluados.items():#preguntar si se puede usar, inf
        tiempo_min += valor.tiempo
    for (clave, valor) in evaluados.items():
        if tiempo_min> valor.tiempo:
            tiempo_min=valor.tiempo
            res = valor
    print("Mejor itinerario según KPI 1 (menor tiempo):")
    return res

def kp2(evaluados): 
    # Este es el del costo: devuelve el camino con menor costo total
    costo_min = None
    res = None

    for clave, valor in evaluados.items():
        if costo_min is None:
            costo_min = valor.costo
            res = valor
        elif valor.costo < costo_min:
            costo_min = valor.costo
            res = valor
    print("Mejor itinerario según KPI 2 (menor costo):")
    return res




"""
#TESTEAMOS:
if __name__ == "__main__":
    # código de prueba local_

    nodos_existentes = construir_red()  # Cargamos la red de transporte

    # Definimos una solicitud de carga
    prueba = construir_itinerario(nodos_existentes, {
        'CARGA_001': {
            'peso_kg': 70000.0,
            'origen': 'Zarate',
            'destino': 'Mar_del_Plata'
        }
    })

    print(prueba)


    #Mini codigo q imprime los caminos encontrados de manera mas linda:
    print("Caminos encontrados:")
    for modo, caminos in prueba.items():
        print(f"\nModo: {modo}")
        for camino in caminos:
            print(" -> ".join([f"{conexion.origen.nombre} -> {conexion.destino.nombre}" for conexion in camino]))



    evaluados = calcular_costos_y_tiempos(prueba, carga_kg=5000)
    imprimir_costos_y_tiempos(evaluados)
"""



