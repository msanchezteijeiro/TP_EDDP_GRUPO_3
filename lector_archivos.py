import csv
#lector_archivos.py

class Lector_Archivos:
    
    @staticmethod
    def cargar_archivo_como_listas(ruta_archivo):
        """
        Lee cualquier CSV y devuelve una lista de listas.
        Cada línea del archivo se convierte en una sublista de strings.
        """
        filas = []
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    partes = linea.strip().split(",")
                    filas.append(partes)
        except FileNotFoundError:
            print(f"Error: no se encontro el archivo {ruta_archivo}")
        except Exception as e:
            print(f"Error al leer el archivo {ruta_archivo}: {e}")

        return filas



#Esta decodifica la lista_conexiones y la transforma en un diccionario de conexiones:
    @staticmethod
    def decodificar_conexiones(lista_de_listas):
        """
        Lee un archivo CSV de conexiones y devuelve un diccionario con los contenidos

        Formato que espera encontrar en el CSV:
        origen,destino,tipo,distancia_km,restriccion,valor_restriccion

        Retorna:
            dict: conexiones[origen][destino] = {'distancia': x, 'modo': y}
        """
        conexiones = {}

        for partes in lista_de_listas[1:]:  # Saltamos cabecera
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



#Esta decodifica una lista de listas con nombres de nodos y devuelve una lista de strings:
#SEGURAMENTE ES INUTIL y REEMPLAZABLE directamente por una funcion que cargue solici
    @staticmethod
    def decodificar_solicitudes(lista_de_listas):
        """
        Procesa una lista de listas con solicitudes de transporte y devuelve un diccionario.
        """
        solicitudes = {}

        for partes in lista_de_listas[1:]:  # Saltamos cabecera
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



#Esta decodifica una lista de listas con nombres de nodos y devuelve una lista de strings:
#SEGURAMENTE ES INUTIL y REEMPLAZABLE directamente por una funcion que instancie directamente los nodos:
#esta funcion estaria en el modulo Nodos.py
    @staticmethod
    def decodificar_nodos(lista_de_listas):
        """
        Procesa una lista de listas con nombres de nodos y devuelve una lista de strings.
        """
        nodos = []

        for fila in lista_de_listas[1:]:  # Saltamos cabecera
            if fila:
                nodos.append(fila[0])

        return nodos



#PRUEBAS DE COMO LEER LOS ARCHIVOS: #de aca para abajo se puede borrar

#Imprime las conexiones de manera estructurada
#Es solo para leerlo.
    @staticmethod
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


if __name__ == "__main__":
    # código de prueba local_


    lista_conexiones = Lector_Archivos.cargar_archivo_como_listas("conexiones.csv")
    conexiones = Lector_Archivos.cargar_archivo_como_listasdecodificar_conexiones(lista_conexiones)
    print(conexiones)
    Lector_Archivos.imprimir_conexiones(conexiones)



    lista_nodos = Lector_Archivos.cargar_archivo_como_listas("nodos.csv")
    nodos = Lector_Archivos.decodificar_nodos(lista_nodos)
    print(nodos)

    lista_solicitudes = Lector_Archivos.cargar_archivo_como_listas("solicitudes.csv")
    solicitudes = Lector_Archivos.decodificar_solicitudes(lista_solicitudes)
    print(solicitudes)