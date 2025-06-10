from redes import construir_red

# Definimos la función que busca todos los caminos posibles entre dos nodos, con un solo modo de transporte y sin ciclos

def encontrar_caminos_para_solicitud(nodos, solicitud):
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




#TESTEAMOS:
if __name__ == "__main__":
    # código de prueba local_

    prueba = encontrar_caminos_para_solicitud(nodos_existentes, {
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
    


