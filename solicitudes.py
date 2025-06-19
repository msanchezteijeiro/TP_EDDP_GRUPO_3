#PREGUNTAR SI ES NECESARIO VALIDAR LOS DATOS DE LA CONEXION, O SEA, QUE EL MODO SEA VALIDO, ETC

#AVERIGUAR SI PUEDE SER QUE RECIBAMOS VARIAS SOLICITUDES TODAS JUNTAS, O SEA, QUE NO HAYA QUE HACER UNA POR UNA

#Si es asi, preparar una funcion que reciba 

#ver si hace falta validar 

from lector_archivos import Lector_Archivos


#Extraemos los datos de las solicitudes desde el archivo CSV y los decodificamos:
lista_solicitudes = Lector_Archivos.cargar_archivo_como_listas("solicitudes.csv")
solicitudes = Lector_Archivos.decodificar_solicitudes(lista_solicitudes) #es un diccionario
# donde la clave es el id de la solicitud y el valor es otro diccionario con los datos de la solicitud
#ejemplo: {'CARGA_001': {'peso_kg': 70000.0, 'origen': 'Zarate', 'destino': 'Mar_del_Plata'}}


#TESTEAMOS:
if __name__ == "__main__":
    # código de prueba local_

    print(solicitudes)
