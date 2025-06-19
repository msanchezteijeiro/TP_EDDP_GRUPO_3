import matplotlib.pyplot as plt
import numpy as np
from redes import construir_red
from solicitudes import solicitudes
from itinerarios import construir_itinerario, calcular_costos_y_tiempos, itinerario_por_solicitud
from vehiculos import vehiculos_por_modo
from itinerarios import kpi_1

class Grafico: 
    
    @staticmethod
    def grafico_barras(titulo, nombre_x, nombre_y, lista_x, lista_y):
        plt.title(label= titulo, fontsize=20, color='blue')
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        plt.bar(lista_x, lista_y,color='green',width=0.5)
        plt.grid()
        
        
    @staticmethod
    def grafico_torta(titulo, secciones, cantidades):
        plt.pie(cantidades,labels=secciones, autopct='%1.2f%%')
        plt.title(label=titulo, loc='center', color='blue')
        
    
    @staticmethod 
    def grafico_lineal(titulo, nombre_x, nombre_y, x1, y1): #linea 1 y linea2 son los nombres de las dos lineas
        plt.title(titulo)
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        # Grafica de lineas
        plt.plot(x1,y1,color='green',linewidth=3, marker="o")
        plt.grid()
        


    #from vehiculos import vehiculos_por_modo  CREO Q ESTA ARRIBA

    @staticmethod
    def obtener_datos_distancia_vs_tiempo(tupla_solicitud, itinerarios, resultado_kp1):
        id_carga, datos = tupla_solicitud

        if not itinerarios:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")

        # Usamo el itinearaio recibido por parametro
        _, mejor_itinerario = resultado_kp1
        vehiculo = vehiculos_por_modo[mejor_itinerario.getModo()]

        distancia_acum = [0]
        tiempo_acum = [0]
        total_distancia = 0
        total_tiempo = 0

        for conexion in mejor_itinerario.camino:
            distancia = conexion.getDistancia()
            tiempo = vehiculo.calcular_tiempo(conexion)

            total_distancia += distancia
            total_tiempo += tiempo

            distancia_acum.append(total_distancia)
            tiempo_acum.append(total_tiempo)

        return tiempo_acum, distancia_acum


    @staticmethod
    def obtener_datos_costo_vs_distancia(tupla_solicitud, itinerarios, resultado_kp1):
        id_carga, datos = tupla_solicitud

        if not itinerarios:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")

        _, mejor_itinerario = resultado_kp1
        vehiculo = vehiculos_por_modo[mejor_itinerario.getModo()]

        carga_kg = datos["peso_kg"]
        distancia_acum = [0, 0]
        costo_acum = [0, vehiculo.calcular_costo_carga(mejor_itinerario.camino, carga_kg)]
        total_distancia = 0
        total_costo = vehiculo.calcular_costo_carga(mejor_itinerario.camino, carga_kg)

        for conexion in mejor_itinerario.camino:
            distancia = conexion.getDistancia()
            costo = vehiculo.calcular_costo_tramo(conexion, carga_kg)

            total_distancia += distancia
            total_costo += costo

            distancia_acum.append(total_distancia)
            costo_acum.append(total_costo)

        return distancia_acum, costo_acum


"""
    @staticmethod
    def Cantidad_modo(solicitudes,nodos_disponibles):
        for tupla_solicitud in solicitudes.items():

            itinerarios_final = itinerario_por_solicitud(nodos_disponibles, tupla_solicitud)
        
            cant_modos = []
            for i in itinerarios_final.values():
                cant_modos.append(i.getModo())
            modos = []
            cantidad = []
            for elemento in cant_modos:
                if elemento not in modos:
                    modos.append(elemento)
                    cantidad.append(cant_modos.count(elemento))
            X = np.array(modos)
            Y = np.array(cantidad)

            fig, ax = plt.subplots(figsize=(5, 5))
            ax.bar(X, Y, color='blue')

            ax.set_title('Cantidad de modos en todos los caminos posibles.')
            ax.set_xlabel('Modos')
            ax.set_ylabel('Cantidades')

            plt.show()
"""

"""

    @staticmethod
    def grafico_distancia_vs_tiempo(distancia_acum, tiempo_acum):
        plt.figure()
        plt.title("Distancia Acumulada vs. Tiempo Acumulado")
        plt.xlabel("Tiempo Acumulado [min]")
        plt.ylabel("Distancia Acumulada [km]")
        plt.plot(tiempo_acum, distancia_acum, marker='o')
        plt.grid()

    
    @staticmethod
    def grafico_costo_vs_distancia(costo_acum, distancia_acum):
        plt.figure()
        plt.title("Costo Acumulado vs. Distancia Acumulada")
        plt.xlabel("Distancia Acumulada [km]")
        plt.ylabel("Costo Acumulado [$]")
        plt.plot(distancia_acum, costo_acum, marker='o', color='orange')
        plt.grid()


    @staticmethod
    def grafico_kpis_itinerarios(itinerarios):
        tiempos = []
        costos = []
        ids = []

        for id_, itin in itinerarios.items():
            tiempos.append(itin.tiempo)
            costos.append(itin.costo)
            ids.append(id_)

        plt.figure()
        plt.title("Comparación de Itinerarios: Costo vs Tiempo")
        plt.xlabel("Tiempo Total [min]")
        plt.ylabel("Costo Total [$]")
        plt.scatter(tiempos, costos, color='purple')

        # Etiquetas con el ID encima de cada punto
        for i in range(len(ids)):
            plt.annotate(f"ID {ids[i]}", (tiempos[i], costos[i]), textcoords="offset points", xytext=(5,5), ha='left')

       """


