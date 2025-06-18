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

