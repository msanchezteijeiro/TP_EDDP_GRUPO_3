from lector_archivos import Lector_Archivos
from nodos import Nodo
from conexiones import Conexion


#INSTANCIAMOS NODOS A PARTIR DE nodos.csv

def instanciar_nodos():
    lista_nodos = Lector_Archivos.cargar_archivo_como_listas("nodos.csv")
    nombres_nodos = Lector_Archivos.decodificar_nodos(lista_nodos)

    # Creamos un diccionario de nodos, donde la clave es el nombre del nodo y el valor es una instancia de Nodo
    nodos = {}
    for nombre in nombres_nodos:
        try:
            nodos[nombre] = Nodo(nombre)
        except ValueError as e:
            raise ValueError(f"Error creando nodo '{nombre}': {e}. Nodo omitido.")
    
    return nodos

#INSTANCIAMOS LAS CONEXIONES A PARTIR DE conexiones.csv

def instanciar_conexiones(nodos):

    lista_conexiones = Lector_Archivos.cargar_archivo_como_listas("conexiones.csv")
    diccionario_conexiones = Lector_Archivos.decodificar_conexiones(lista_conexiones)

    # Recorremos el diccionario de conexiones donde las claves son nodos origen y cada valor es otro dic con 
    # cada nodos destino y los datos de la conexion (modo, distancia, restriccion, valor_restriccion)

    for origen, destinos in diccionario_conexiones.items(): #para cada par llave-valor

        # verificamos que el nodo origen este permitido!
        if origen not in nodos:
            print(f"Nodo origen '{origen}' no está definido en nodos.csv. Se ignora.")
            continue  
        
        for destino, lista_conexiones in destinos.items(): 

            #un ejemplo es: destino = "Buenos_Aires" y lista_modos_conexion = [{'modo': 'Ferroviaria', 'distancia': 85.0, 'restriccion': 'velocidad_max', 'valor_restriccion': '80'}, ...]

            # Verificamos que el nodo destino este permitido!
            if destino not in nodos:
                print(f"Nodo destino '{destino}' no está definido en nodos.csv. Se ignora.")
                continue

            # Recorremos todas las conexiones entre este par origen-destino
            #osea por cada diccionario dentro de la lista conexiones, instanciamos un objeto Conexion:

            for c in lista_conexiones: #cada c es un modo de conexion entre esos dos nodos, con datos distintos (restricciones, etc)
                
                try:
                    # Creamos un objeto de tipo Conexion con los datos correspondientes
                    conexion = Conexion(
                        origen=nodos[origen],
                        destino=nodos[destino],
                        modo=c["modo"],
                        distancia=c["distancia"],
                        restriccion=c["restriccion"],
                        valor_restriccion=c["valor_restriccion"]
                    )

                    nodos[origen].agregar_conexion(destino, conexion)
                    #revisar que no haya conexion duplicada
                    conexion_inversa = Conexion(
                        origen=nodos[destino],
                        destino=nodos[origen],
                        modo=c["modo"],
                        distancia=c["distancia"],
                        restriccion=c["restriccion"],
                        valor_restriccion=c["valor_restriccion"]
                    )
                    nodos[destino].agregar_conexion(origen, conexion_inversa)

                except (ValueError, TypeError) as e:
                    raise ValueError(f"Error creando conexión entre '{origen}' y '{destino}' via '{c['modo']}': {e}. Registro omitido.")


def construir_red(): #YA NO NECESITA NINGUN MANEJO DE ERRO, se manejaron al instanciar Nodos y Conexiones arriba.
    nodos_existentes = instanciar_nodos()
    instanciar_conexiones(nodos_existentes)
    return nodos_existentes

