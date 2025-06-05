import csv

def cargar_conexiones(ruta_archivo):
    """
    Lee un archivo CSV de conexiones y devuelve un diccionario con los contenidos

    Formato que espera encontrar en el CSV:
    origen,destino,tipo,distancia_km,restriccion,valor_restriccion

    Retorna:
        dict: conexiones[origen][destino] = {'distancia': x, 'modo': y}
    """
    conexiones = {}

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # Saltamos la primera línea (cabecera)
    for linea in lineas[1:]:
        partes = linea.strip().split(",")
        if len(partes) < 4:
            continue  # línea mal formada

        origen = partes[0]
        destino = partes[1]
        modo = partes[2]
        restriccion = None if partes[4] == "" else partes[4]
        valor_restriccion = None if partes[5] == "" else partes[5]

        try:
            distancia = float(partes[3])
        except ValueError:
            continue  # distancia inválida

        if origen not in conexiones:
            conexiones[origen] = {}
        
        if destino not in conexiones[origen]:
                conexiones[origen][destino] = []		

        conexiones[origen][destino].append({
            "modo": modo,
            "distancia": distancia,
            "restriccion": restriccion,
            "valor_restriccion": valor_restriccion
        })

    return conexiones




def cargar_nodos(ruta_archivo):
    """
    Lee un CSV con una columna 'nombre' y devuelve una lista de objetos Nodo.
    """
    nodos = []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    for linea in lineas[1:]:  # Saltamos cabecera
        nombre = linea.strip()
        nodos.append(nombre)

    return nodos




def cargar_solicitudes(ruta_archivo):
    """
    Lee un CSV con solicitudes de transporte y devuelve un diccionario
    donde la clave es el id_carga y el valor es un diccionario con el resto de la info.
    """
    solicitudes = {}

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    for linea in lineas[1:]:  # Saltar cabecera
        partes = linea.strip().split(",")
        if len(partes) < 4:
            continue

        id_carga = partes[0]
        try:
            peso = float(partes[1])
        except ValueError:
            continue  # peso inválido

        origen = partes[2]
        destino = partes[3]

        solicitudes[id_carga] = {
            "peso_kg": peso,
            "origen": origen,
            "destino": destino
        }

    return solicitudes


def cargar_archivo(ruta_archivo):
    """
    Detecta el tipo de archivo CSV según su cabecera y llama a la función adecuada.
    Retorna: dict o list según el contenido.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        cabecera = archivo.readline().strip().split(",")

    if set(cabecera) >= {"origen", "destino", "tipo", "distancia_km"}:
        return cargar_conexiones(ruta_archivo)
    elif "nombre" in cabecera:
        return cargar_nodos(ruta_archivo)
    elif set(cabecera) >= {"id_carga", "peso_kg", "origen", "destino"}:
        return cargar_solicitudes(ruta_archivo)
    else:
        raise ValueError("No se reconoce el tipo de archivo por su cabecera.")




#PRUEBAS DE COMO LEER LOS ARCHIVOS:

#Imprime las conexiones de manera estructurada
#Es solo para leerlo.

def imprimir_conexiones(conexiones):
    for origen, destinos in conexiones.items():
        print(f"\nOrigen: {origen}")
        for destino, lista_conexiones in destinos.items():
            print(f"  ➜ Destino: {destino}")
            for conexion in lista_conexiones:
                modo = conexion['modo']
                distancia = conexion['distancia']
                restriccion = conexion['restriccion']
                valor = conexion['valor_restriccion']
                print(f"    - Modo: {modo}, Distancia: {distancia} km", end="")
                if restriccion and valor:
                    print(f", Restricción: {restriccion} = {valor}")
                else:
                    print()




conexiones = cargar_conexiones("conexiones.csv")
print(conexiones)

imprimir_conexiones(conexiones)

nodos = cargar_nodos("nodos.csv")

print(nodos)


solicitudes = cargar_solicitudes("solicitudes.csv")
print(solicitudes)