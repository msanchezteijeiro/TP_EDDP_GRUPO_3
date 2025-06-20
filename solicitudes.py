from lector_archivos import Lector_Archivos

#Extraemos los datos de las solicitudes desde el archivo CSV y los decodificamos:
lista_solicitudes = Lector_Archivos.cargar_archivo_como_listas("solicitudes.csv")
solicitudes = Lector_Archivos.decodificar_solicitudes(lista_solicitudes) #es un diccionario


#Prueba local:
if __name__ == "__main__":

    print(solicitudes)

