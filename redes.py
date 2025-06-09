

#INSTANCIAMOS NODOS A PARTIR DE nodos.csv

from lector_archivos import cargar_archivo_como_listas, decodificar_nodos
from nodos import Nodo


def instanciar_nodos():
    lista_nodos = cargar_archivo_como_listas("nodos.csv")
    nombres_nodos = decodificar_nodos(lista_nodos)

    # Creamos un diccionario de nodos, donde la clave es el nombre del nodo y el valor es una instancia de Nodo
    # Estamos suponiendo que el archivo nodos.csv se recibirá una unica vez, este codigo no contempla que se agreguen o eliminen nodos permitidos
    # tambien suponemos que los nombres de nodos son unicos, si no lo fueran, se sobreescribirian los nodos con el mismo nombre
    # PREGUNTAR SI ESTO ESTA BIEN O NO!!! tal vez esto deberia ser una funcion que tolere estos cambios

    nodos = {}
    for nombre in nombres_nodos:
        nodos[nombre] = Nodo(nombre)
    
    return nodos

#---------------------------------------------------------------------------------

#INSTANCIAMOS LAS CONEXIONES A PARTIR DE conexiones.csv

from lector_archivos import decodificar_conexiones
from conexiones import Conexion

def instanciar_conexiones(nodos):

    lista_conexiones = cargar_archivo_como_listas("conexiones.csv")
    diccionario_conexiones = decodificar_conexiones(lista_conexiones)



    # Recorremos el diccionario de conexiones donde las claves son nodos origen y cada valor es otro dic con 
    # cada nodos destino y los datos de la conexion (modo, distancia, restriccion, valor_restriccion)


    for origen, destinos in diccionario_conexiones.items(): #para cada par llave-valor

        # verificamos que el nodo origen este permitido!
        if origen not in nodos:
            print(f"Nodo origen '{origen}' no está definido en nodos.csv. Se ignora.")
            continue  # Lo aprendi en google, REVISAR SI SE PUEDE USAR (pass no se podia): 
                        #salta directamente a la siguiente iteración, saltándose el resto del código dentro del loop actual.
                        #sino es facil de reemplazar usando un if y un else englobando todo el resto del código


        #cada origen tiene como valor un diccionario donde las claves son los destinos y los valores una lista de las conexiones q tiene (todo en subdiccionarios):

        """
        Ejemplo: BORRAR DESPUES:

        {'Zarate': {'Buenos_Aires': [{'modo': 'Ferroviaria', 'distancia': 85.0, 'restriccion': 'velocidad_max', 'valor_restriccion': '80'},
        {'modo': 'Automotor', 'distancia': 85.0, 'restriccion': None, 'valor_restriccion': None}, 
        {'modo': 'Fluvial', 'distancia': 85.0, 'restriccion': 'tipo', 'valor_restriccion': 'fluvial'}], 
        'Junin': [{'modo': 'Ferroviaria', 'distancia': 185.0, 'restriccion': None, 'valor_restriccion': None}, 
        {'modo': 'Automotor', 'distancia': 185.0, 'restriccion': 'peso_max', 'valor_restriccion': '15000'}]},....aca continuaria otro origen....
        .....}

        - Organizado mas lindo:
        Origen: Zarate
        ➜ Destino: Buenos_Aires
            - Modo: Ferroviaria, Distancia: 85.0 km, Restricción: velocidad_max = 80
            - Modo: Automotor, Distancia: 85.0 km
            - Modo: Fluvial, Distancia: 85.0 km, Restricción: tipo = fluvial
        ➜ Destino: Junin
            - Modo: Ferroviaria, Distancia: 185.0 km
            - Modo: Automotor, Distancia: 185.0 km, Restricción: peso_max = 15000
        """

        #recorremos esos diccionarios internos para crear las conexiones, 
        #usamos destinos.items() para obtener los pares clave-valor de cada destino y sus datos de conexion
        for destino, lista_conexiones in destinos.items(): #osea for cada destino y sus modos de conexion....

            #un ejemplo es: destino = "Buenos_Aires" y lista_modos_conexion = [{'modo': 'Ferroviaria', 'distancia': 85.0, 'restriccion': 'velocidad_max', 'valor_restriccion': '80'}, ...]

            # Verificamos que el nodo destino este permitido!
            if destino not in nodos:
                print(f"Nodo destino '{destino}' no está definido en nodos.csv. Se ignora.")
                continue #REVISAR LO MISMO Q ANTES

            # Recorremos todas las conexiones entre este par origen-destino
            #osea por cada disccionario dentro de la lista conexiones, instanciamos un objeto Conexion:

            for c in lista_conexiones: #cada c es un modo de conexion entre esos dos nodos, con datos distintos (restricciones, etc)

                # Creamos un objeto de tipo Conexion con los datos correspondientes
                conexion = Conexion(
                    origen=nodos[origen],
                    destino=nodos[destino],
                    modo=c["modo"],
                    distancia=c["distancia"],
                    restriccion=c["restriccion"],
                    valor_restriccion=c["valor_restriccion"]
                )

                # Agregamos esta conexión al nodo origen, usamos el método agregar_conexion q esta en la clase Nodo
                # REVISAR SI ESTO ESTA BIEN
                nodos[origen].agregar_conexion(destino, conexion)



def construir_red():
    nodos_existentes = instanciar_nodos()
    instanciar_conexiones(nodos_existentes)
    return nodos_existentes


#PARA EL Q LEA:
#esto instanciaria todas las conexiones y nodos usando UNA SOLA VEZ los archivos nodos.csv y conexiones.csv
#cada conexion queda guardad como un objeto dentro de cada nodo, en el diccionario VECINOS de ese nodo.
#osea el diccionario VECINOS de un nodo, tendra como clave el destino y como valor una lista de objetos Conexion que conectan ese nodo origen con el destino.
#PREGUNTAR SI ESTO ESTA BIEN, O SI HAY Q HACERLO DE OTRA MANERA, POR EJEMPLO, CARGAR LOS NODOS Y CONEXIONES EN UN SOLO DICCIONARIO

#en resumen, a las redes de transporte se las accede eligiendo un nodo origen y viendo sus vecinos.


#TESTEAMOS:
if __name__ == "__main__":
    # código de prueba local_

    nodos_existentes = construir_red()

    # Prueba
    print(nodos_existentes)

    print("Vecinos de Zarate:")
    print(nodos_existentes["Zarate"].vecinos)

    print(nodos_existentes)




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
    datos = list(solicitud.values())[0]
    origen = datos["origen"]
    destino = datos["destino"]

    # Lista de modos válidos (podés cambiarla si tenés otra forma de validarlos)
    modos_disponibles = ["ferroviario", "automotor", "maritimo", "aereo"]

    # Función recursiva para buscar caminos
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

    # Recorremos todos los modos posibles y buscamos caminos para cada uno
    for modo in modos_disponibles:
        if origen in nodos and destino in nodos:
            buscador_caminos(actual=origen, destino=destino, camino=[], visitados=[], modo=modo)

    return resultados



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
    print("Caminos encontrados:")
    for modo, caminos in prueba.items():
        print(f"\nModo: {modo}")
        for camino in caminos:
            print(" -> ".join([f"{conexion.origen.nombre} -> {conexion.destino.nombre}" for conexion in camino]))
    


