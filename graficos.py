import matplotlib.pyplot as plt
from redes import construir_red
from solicitudes import solicitudes
from itinerarios import construir_itinerario, calcular_costos_y_tiempos
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
    def grafico_linea(valores):
        plt.plot(valores)
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
        

    @staticmethod
    def calcular_acumulados(itinerario, vehiculo, carga_kg):
        distancia_acumulada = []
        tiempo_acumulado = []
        costo_acumulado = []

        total_distancia = 0
        total_tiempo = 0
        total_costo = 0

        for conexion in itinerario.camino:
            distancia = conexion.getDistancia()
            tiempo = vehiculo.calcular_tiempo(conexion)
            costo = vehiculo.calcular_costo_tramo(conexion, carga_kg)

            total_distancia += distancia
            total_tiempo += tiempo
            total_costo += costo

            distancia_acumulada.append(total_distancia)
            tiempo_acumulado.append(total_tiempo)
            costo_acumulado.append(total_costo)

        return distancia_acumulada, tiempo_acumulado, costo_acumulado

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

        plt.grid()
    
    def graficar_itinerario_desde_solicitud(id_solicitud):
        nodos = construir_red()
        datos = solicitudes[id_solicitud]
        print(nodos)
        print({id_solicitud: datos})
        caminos = construir_itinerario(nodos, (id_solicitud,datos))
        itinerarios = calcular_costos_y_tiempos(caminos, datos["peso_kg"])
        if not itinerarios:
            print("No hay itinerarios posibles.")
            return

        # Podés elegir el primero o el mejor según KPI 1
        # itinerario = list(itinerarios.values())[0]
        itinerario = kpi_1(itinerarios)[1]
    # Para comparar todos los itinerarios de esa solicitud
        Grafico.grafico_kpis_itinerarios(itinerarios)

        vehiculo = vehiculos_por_modo[itinerario.getModo()]
        dist, tiempo, costo = Grafico.calcular_acumulados(itinerario, vehiculo, datos["peso_kg"])
        Grafico.grafico_distancia_vs_tiempo(dist, tiempo)
        Grafico.grafico_costo_vs_distancia(costo, dist)    


#Grafico Tiempo vs Distancia Recorrida (FALTA PONER LOS DATOS DE TIEMPO Y DISTANCIA)
#Grafico.grafico_lineal("Tiempo vs Distancia", "Tiempo [min]", "Distancia [km]", )

#Grafico Costo por Distancia Recorrida (FALTA PONER LOS DATOS DE COSTO Y DISTANCIA)
#Grafico.grafico_lineal("Costo vs Distancia", "Costo [$]", "Distancia [km]", )

if __name__ == "__main__":
    # Acá elegís la solicitud que querés visualizar
    Grafico.graficar_itinerario_desde_solicitud("CARGA_001")
    plt.show()