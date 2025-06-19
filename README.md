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
Ejemplo del contenido del archivo:
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
Ejemplo de como seria el contenido del csv:

origen,destino,tipo,distancia_km,restriccion,valor_restriccion
Zarate,Buenos_Aires,Ferroviaria,85,velocidad_max,80

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
"vecinos": diccionario donde la clave es el nombre de un nodo destino y el valor es una lista de objetos "Conexion" que van desde este nodo hacia al destino.
"modos_soportados": lista de str que representan los modos de transporte disponibles en ese nodo ("ferroviaria", "automotor", etc)

En un principio, en el __init__ se valida e inicializa un nuevo nodo con su nombre, sin conexiones.

Se utilizan los setters con validaciones dentro para evitar errores. 

"agregar_conexion(destino, conexion)
Registra una nueva conexion (objeto de "Conexion") con otro nodo.
Se agregan tanto de origen a destino como de destino a origen.
Agrega el nombre del destino al diccionario "vecinos".
Si el modo de la conexion no estaba registrado en "modos_soportados", lo agrega.

Se utilizan los getters para devolver la informacion.

Esta clase permite que los nodos se construyan desde un archivos ".csv"


conexiones.py

Se define la clase "Conexion", que representa un tramo directo entre dos nodos dentro de la red de transporte. Cada conexion tiene un origen, un destino, un modo de transporte y si las hay, restricciones.

Clase "COnexion"

Atributos:
"origen": objeto de tipo "Nodo", punto de partida de la conexion
"destino": objeto de tipo "Nodo", punto final de la conexion
"modo": str que indica el medio de transporte (por ejemplo: "automotor")
"distancia": valor numerico en kilometros
"restriccion": (opcional), str o None, tipo de restriccion que se aplica a la conexion.
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



vehiculos.py

Aca se implementa la clase "Vehiculo" y sus cuatro subclases que representan distintos modos de transporte disponibles:

-Ferroviaria
.Automotor
-Fluvial
-Aerea

Cada clase esta presonalizada para calcular:
-El tiempo necesario para recorrer una conexion.
-El costo total del tramo (con posibles restricciones o costos fijos)
-La cantidad de vehiculos requeridos segun la carga.

Clases definidas:

"Vehiculo" (clase base)
Atributos comunes: "modo", "capacidad"
-Metodos:
set/getModo
set/getCapacidad
getModos (metodo de clase para conocer los modos registrados)

Clase "Ferroviaria"
-Costo por kg y costo fijo por tramo.
-Costo del tramo depende de la distancia (menor o mayor a 200km)
-Afectada por la restriccion de "velocidad_max"

Clase "Automotor"
-Costo por km+ costo fijo por tramo.
-El costo de la carga depende del peso por vehiculo.
-Afectada por la restriccion de "peso_max"

Clase "Fluvial"
-Usa costos por km y por kg.
-Costo fijo varia segun el tipo de via ("fluvial" o "maritimo").
-Afectada por la restriccion "tipo"

Clase "Aerea"
-TIene costos fijos y variables por km y por kg.
-Puede verse afectada por la probabilidad de mal tiempo ("prob_mal_timepo"), lo cual disminuyela velocidad de vuelo de 600km/h a 400km/h.

Nota importante:
Todas las clases validan:
-Tipos de datos (int, float, str)
-La existencia y tipo de las restricciones aplicadas a cada conexion.

Funcion importante: "instanciar_vehiculos()"
Es la funcion encargada de crear los objetos reales de cada tipo de vehiculo (ferroviario, automotor, fluvial o aereo) con valores predeterminados como capacidad, velocidas, costos, etc
Inicializa todos los transportes.
Devuelve "vehiculos_por_modo", diccionario con las claves "ferroviaria", "automotor", "fluvial" y "aerea"



redes.py

Este archivo es responsable de construir la red de nodos y sus conexiones a partir de los archivos "nodos.csv" y "conexiones.csv".

Funciones principales:
-"instanciar_nodos()"
Lee los nombres de los nodos desde "nodos.csv" y crea un diccionario con objetos Nodo, usando como clave el nombre de cada uno.
Si un nombre no es valido, se lanza un error y se omite ese nodo.

-"instanciar_conexiones(nodos)"
A partir del archivo "conexiones.csv", crea objetos Conexion entre los nodos instanciados.
Cada conexion se agrega tanto al nodo de origen como al nodo de destino, simulando una red bidireccional.
Tambien se controlan errores por conexiones invalidas o referencia a nodos que no existen.

-"construir_red()"
Es la funcion principal que se llama desde otros modulos.
Ejecuta las funciones anteriores y devuelve el diccionario con todos los nodos y sus respectivas conexiones.

Nota:
La red se presenta como un diciconario de nodos y cada nodo guarda a sus vecinos en un diccionario interno (nodo.vecinos), donde:
-La clave es el nombre del nodo vecino (destino)
-El valor es una lista de objetos Conexion que van hacia ese vecino.
-Se incluye manejo de errores ante datos invalido o archivos incompletos


solicitudes.py

Se encarga de leer y preparar las solicitudes de transporte desde el archivo "solicitudes.csv".

-Carga del archivo
Utiliza "cargar_archivo_como_listas()" y "decodificar_solicitudes()" desde lector_archivos.py para procesar el CSV.

-Estructura
Las solicitudes se almacenan en un diccionario donde:
-La clave es el ID de la solicitud (por ejemplo: "CARGA_001").
-El valor es otro diccionario con: 
"peso_kg": peso total a transportar (float)
"origen": nodo de partida
"destino": nodo de llegada



intinerarios.py

Este archivo genera, evalua e imprime los itinerarios de transporte entre dos nodos segun la solicitud de carga.

Clase Itinerario:
Representa un posible camino para transportar una carga con un modo de transporte especifico.

Atributos:
modo: modo de trnasporte usado (str)
camino: lista de objetos Conexion que conforman el recorrido
costo: costo total de viaje
timepo: duracion total en minutos

Metodos:
Getters: (getModo, getCamino, etc)
__repr__: imprime el itinerario de forma legible
formatear_tiempo_minutos: convierte minutos a formato HH:MM:SS

"construir_itinerario(nodos, solicitud_tupla)"
-Usa una busqueda recursiva sin ciclos para encontrar toods los caminos posibles de un nodo origen a uno destino, pero usando solo un modo de transporte a la vez.
-Devuelve un diccionario con claves=modos de transporte, y valores=lista de listas de conexiones.

"calcular_costos_y_tiempos(itinerarios_base, carga_kg)"
Para cada camino encontrado, calcula:
-EL costo total(costo carga+ costos de tramo)
-El tiempo total sumando los timepos de cada tramo
-Devuelve un diccionario con claves numericas (IDs) y valores que son objeto Itinerario.

"itinerario_por_solicitud(nodos_existentes, solicitud_tupla)"
-Ejecuta la busqueda de caminos y los calculos de los costos y tiempos
-Funcion que se llama desde el main

"imprimir_itinerario_final(itinerarios_final)"
-Muestra todos los itinerarios generados en formato tabla:
ID, Modo, COsto total, Tiempo total , camino

"kpi_1(itinerarios_final)"
Minimiza el timepo total

"kpi_2(itinerarios_final)"
Minimiza el costo total

Cada uno retorna una tupla (ID, itinerario) correspondiente al mejor caso.



main.py

Archivo principal del TP. Ejecuta todo el proceso de planificacion de transporte desde la lectura de archivos hasta la impresion de resultados y KPIs.

Funcionalidad:
1. Construye la red de nodos y conexiones
"nodos_disponibles=construir_red()"
-Carga los archivos "nodos.csv" y "conexiones.csv"
-Instancia los nodos y conexiones correspondientes, validando todo.

2. Carga las solicitudes desde "solicitudes.csv"
Cada solicitud indica:
-Peso de la carga
-Nodo origen
-Nodo destino

3. Para cada solicitud:
-Se generan todos los itinerarios posibles (uno por modo de transporte)
-Se calculan costos y tiempos
-Se imprime una tabla resumen
-Se evaluan los KPIs.

La salida esperada es que por cada solicitud, el programa imprimira:
-Tabla con todos los itinerarios posibles
-Mejor itinerario segun KPI1
-Mejor itinerario segun KPI2

Notas:
El archivo incluye un try-except general para atrapar errores en la ejecucion.
-Los vehiculos deben estar instanciados en vehiculos.py.


# Instructivo de ejecución deprograma


