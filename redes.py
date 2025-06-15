from lector_archivos import cargar_archivo_como_listas, decodificar_nodos, decodificar_conexiones
from nodos import Nodo
from conexiones import Conexion

#redes.py
#INSTANCIAMOS NODOS A PARTIR DE nodos.csv

def instanciar_nodos():
    lista_nodos = cargar_archivo_como_listas("nodos.csv")
    nombres_nodos = decodificar_nodos(lista_nodos)

    # Creamos un diccionario de nodos, donde la clave es el nombre del nodo y el valor es una instancia de Nodo
    # Estamos suponiendo que el archivo nodos.csv se recibirá una unica vez, este codigo no contempla que se agreguen o eliminen nodos permitidos
    # tambien suponemos que los nombres de nodos son unicos, si no lo fueran, se sobreescribirian los nodos con el mismo nombre
    # PREGUNTAR SI ESTO ESTA BIEN O NO!!! tal vez esto deberia ser una funcion que tolere estos cambios

    nodos = {}
    for nombre in nombres_nodos:
        try:
            nodos[nombre] = Nodo(nombre)
        except ValueError as e:
            print(f"Error creando nodo '{nombre}': {e}. Nodo omitido.")
    
    return nodos

#---------------------------------------------------------------------------------

#INSTANCIAMOS LAS CONEXIONES A PARTIR DE conexiones.csv

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
                
                try: #CAPTURAMOS CUALQUIER ERROR INSTANCIANDO UNA CONEXION
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
                    print(f"Error creando conexión entre '{origen}' y '{destino}' via '{c['modo']}': {e}. Registro omitido.")


def construir_red(): #YA NO NECESITA NINGUN MANEJO DE ERRO, se manejaron al instanciar Nodos y Conexiones arriba.
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

    try:
        nodos_existentes = construir_red()
    except Exception as e:
        print("Error al contruir la red: {e}")

"""
    # Prueba
    print(nodos_existentes)

    print("Vecinos de Zarate:")
    print(nodos_existentes["Zarate"].vecinos)

    print(nodos_existentes)
"""


