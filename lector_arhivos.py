import csv

def cargar_conexiones(ruta_archivo):
    """
    Lee un archivo CSV de conexiones y devuelve un diccionario de adyacencia.

    Formato esperado por línea:
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
        try:
            distancia = float(partes[3])
        except ValueError:
            continue  # distancia inválida

        if origen not in conexiones:
            conexiones[origen] = {}

        conexiones[origen][destino] = {
            "distancia": distancia,
            "modo": modo
        }

    return conexiones

conexiones = cargar_conexiones("conexiones.csv")

print(conexiones["Zarate"]["Junin"]["distancia"])  # ➜ 185.0

#FALTARIA CORREGIR que pasa si tenemos en el csv dos veces el mismo origen y destino con dos modos distintos:
#esto generaria un error, ya que el diccionario no permite claves duplicadas.
#tambien ver si se rompe si hay dos conexiones iguales en todo menos la restriccion que seria diferente