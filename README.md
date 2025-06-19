# TP5_EDDP

Este es el repositorio del Grupo 5.

Este proyecto resuelve un problema de planificación de transporte multimodal. 
Dado un conjunto de ciudades (nodos), conexiones disponibles entre ellas y solicitudes de carga, el sistema busca
todos los itinerarios posibles para transportar esa carga cumpliendo restricciones, calcula los costos y tiempos,
y genera visualizaciones gráficas.

Archivos .csv

El programa necesita tres archivos .csv para su correcto funcionamiento.
El estado inicial de la red de transporte, las solicitudes de envio y los nodos disponibles.

1. nodos.csv
Contiene el listado de todos los nodos (ciudades) que forman parte de la red de transporte.
El contenido del archivo: (cheqeuar si hace falta)
nombre
Zarate
Buenos_Aires
Junin
Azul
Mar_del_Plata

Este archivo define los puntos de origen y destino posibles en los itinerarios. Cada nombre debe ser unico.

2. solicitudes.csv

Describe cada solicitud de transporte que debe ser procesada. 

id_carga            peso_kg         origen          destino
CARGA_001           70000           Zarate    Mar_del_plata

Cada solicitud se toma individualmente, t el programa construye los caminos posibles entre origen y destino respetando el modo de transporte

3. conexiones.csv

Define las conexiones entre nodos, con su tipo de transporte, distancia y posibles restricciones. Este archivo sirve para construir la red de transporte y evaluar costos y tiempos.

(poner como se ve el csv)

Notas:
restriccion puede tomar el valor de: "peso_max", "velocidad_max", "prob_mal_tiempo", (tipo) "maritimo" "fluvial"

Si una restriccion esta presente debe tener un valor asociado.


Archivos.py del programa

lector_archivos.py

Este modulo se encarga de la carga, procesamiento y decodificacion de los archivos .csv con los datos de entrada del sistema.

Funciones principales:

"cargar_archivo_como_listas(ruta_archivo)"
Lee un archivo .csv y devuelve una lista de listas con los datos, separando los valores por coma (,) y eliminando saltos de linea.
Incluye manejo de errores ante archivos no encontrados o mal formateados.

"decodificar_conexiones(lista_de_listas)"
Convierte la lista de listas "conexiones.csv" en un diccionario anidado con la siguiente estructura:
{
  "Zarate": {
    "Buenos_Aires": [
      {
        "modo": "Ferroviaria",
        "distancia": 85.0,
        "restriccion": "velocidad_max",
        "valor_restriccion": "80"
      },
      ...
    ]
  },
  ...
}

Este diccionario es clave para poder instanciar los objetos de Conexion.

"decodificar_nodos(lista_de listas)"
Estrae los nombres de los nodos desde nodos.csv y los devuelve como una lista de strings
["Zarate", "Buenos_Aires", "Junin", "Azul", "Mar_del_Plata"]



validaciones.py

Acá se define la clase "Validaciones" la cual agrupa metodos estaticos para validar tipos de datos.
Se utiliza en multiples clases del proyecto para evitar errores en la ejecucion del programa.

La clase "Validaciones" tiene distitnos metodos donde se validan floats, int, str, nombre, tipo de restricciones, valor de las restricciones.

Esta pensada para evitar errores al cargar datosdesde archivos externos o al crear objetos.
IMPORTANTE: no debe importar otras clases del sistema para evitar dependencias circulares.


nodos.py

En este archivo se define la clase "Nodo", que represneta un punto dentro de la red de transporte (ciudad). Cada nodo tiene una conexion hacia otros nodos y los modos de transporte que soporta.

Clase "Nodo"

Los atributos de esta clase:
"nombre": nombre del nodo (se valida al instanciar)
"vecinos": diccionario donde la clave es el nombre de un nodo destino y el valor es una listab de objetos "Conexion" que van desde este nodo hacia al destino.
"modos_soportados": lista de str que representan los modos de transporte disponibles en ese nodo ("ferroviaria", "automotor", etc)

En un principio, en el __init__ se valida e inicializa un nuevo nodo con su nombre, sin conexiones.

Se utilizan los setters con validaciones dentro para evitar errores. 

"agregar_conexion(destino, conexion)
Registra una nueva conexion (objeto de "Conexion") con otro nodo.
Agrega el nombre del destino al diccionario "vecinos".
Si el modo de la conexion no estaba registrado en "modos_soportados", lo agrega.

Se utilizan los getters para devolver la informacion.

Esta clase permite que los nodos se construyan desde un archivos .csv


conexiones.py

Se define la clase "Conexion", que representa un tramo directo entre dos nodos dentro de la red de transporte. Cada conexion tiene un origen, un destino, un modo de transporte y si las hay, restricciones.

Clase "COnexion"

Atributos:
"origen": objeto de tipo "Nodo", punto de partida de la conexion
"destino": objeto de tipo "Nodo", punto final de la conexion
"modo": str que indica el medio de transporte
"distancia": valor numerico en kilometros
"restriccion": (opcional) tipo de restriccion que se aplica a la conexion.
"valor_restriccion": (opcional) valor asociado a la restriccion

Metodos principales:

__init__(): constructor que valida y asigna todos los atributos
set/getOrigen()/set/getDestino(): asigna o devuelve los nodos origen y destino
set/getModo(): valida y asigna el modo de transporte
set/getDistancia(): valida y asigna la distancia
set/getRestriccion()/ set/getValorRestriccion(): validan y asignan posibles restricciones como "peso_max", "velocidad_max", "prob_mal_tiempo", etc
__repr__:m devuelce una representacion legible de la conexion

Se utilizan validaciones de nodos (se asegura que el origen o destino sea una instancia de "Nodo")
Se utilizan validaciones para el modo: chequea si el modo de transporte es uno de los validos.

Esta clase se usa para construir la red de transporte. Cada objeto "Conexion" se agrega al diccionario "vecino" de un nodo, lo que permite explorar las rutas posibles durante el armado del itinerario.


