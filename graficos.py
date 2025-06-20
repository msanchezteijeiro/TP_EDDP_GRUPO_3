import matplotlib.pyplot as plt
import numpy as np
from vehiculos import Vehiculo

class Grafico: 
    
    @staticmethod
    def grafico_barras(titulo, nombre_x, nombre_y, lista_x, lista_y):
        plt.title(label= titulo, fontsize=10, color='black')
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        plt.bar(lista_x, lista_y,color='green',width=0.5)
        plt.grid()
        plt.xticks(rotation=0, ha='center')
        
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
    def graf_distancia_vs_tiempo(tupla_solicitud, itinerarios_final, itineario_elegido, vehiculos_por_modo):
        id_carga, datos = tupla_solicitud

        if not itinerarios_final:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")

        # Usamo el itinearaio recibido por parametro
        _, mejor_itinerario = itineario_elegido
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

        Grafico.grafico_lineal("Distancia Acumulada vs. Tiempo Acumulado", "Tiempo Acumulado [min]", "Distancia Acumulada [km]", tiempo_acum, distancia_acum)

        plt.show()


    @staticmethod
    def graf_tiempo_vs_costo(tupla_solicitud, itinerarios_final, itineario_elegido, vehiculos_por_modo):
        id_carga, datos = tupla_solicitud

        if not itinerarios_final:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")

        _, mejor_itinerario = itineario_elegido
        vehiculo = vehiculos_por_modo[mejor_itinerario.getModo()]

        carga_kg = datos["peso_kg"]
        distancia_acum = [0]
        costo_acum = [0]
        costo_fijo = [vehiculo.calcular_costo_carga(mejor_itinerario.camino, carga_kg)]
        total_distancia = 0
        total_costo = 0

        for conexion in mejor_itinerario.camino:
            distancia = conexion.getDistancia()
            costo = vehiculo.calcular_costo_tramo(conexion, carga_kg)

            total_distancia += distancia
            total_costo += costo

            distancia_acum.append(total_distancia)
            costo_acum.append(total_costo)
            costo_fijo.append(vehiculo.calcular_costo_carga(mejor_itinerario.camino, carga_kg))

        grafico2 = Grafico.grafico_lineal("Costo Acumulado vs. Distancia Acumulada", "Distancia Acumulada [km]", "Costo Acumulado [$]", distancia_acum, costo_acum)
        grafico3 = Grafico.grafico_lineal("Costo Acumulado vs. Distancia Acumulada", "Distancia Acumulada [km]", "Costo Acumulado [$]", distancia_acum, costo_fijo)
            
        plt.show()


    @staticmethod
    def graf_cantidad_vs_modo(itinerarios_final):
        
        cant_modos = []
        for i in itinerarios_final.values():
            cant_modos.append(i.getModo())
        modos = []
        cantidad = []
        for elemento in cant_modos:
            if elemento not in modos:
                modos.append(elemento)
                cantidad.append(cant_modos.count(elemento))
        X = np.array([m.capitalize() for m in modos])
        Y = np.array(cantidad)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.bar(X, Y, color='blue')

        ax.set_title('Cantidad de Caminos Posibles por Modo')
        ax.set_xlabel('Modo')
        ax.set_ylabel('Cantidad')

        plt.show()

    @staticmethod
    def graf_carga_por_unidad (itinerario_final, solicitud):
        carga = solicitud[1]['peso_kg']
        modo = itinerario_final[1].getModo()
        cant_vehiculos = 0
        vehiculos = []
        cargas = []
        for vehiculo in Vehiculo.vehiculos: 
            if vehiculo.getModo() == modo.lower(): 
                while carga >= vehiculo.getCapacidad():
                    cargas.append(vehiculo.getCapacidad())
                    cant_vehiculos += 1
                    vehiculos.append(cant_vehiculos)
                    carga -= vehiculo.getCapacidad()
                if carga > 0: 
                    cargas.append(carga)
                    cant_vehiculos += 1
                    vehiculos.append(cant_vehiculos)
                    carga = 0 
                    
        
        nros_vehiculos = np.array(vehiculos)
        x = nros_vehiculos.astype(str)
        y = np.array(cargas)
        Grafico.grafico_barras('Carga por vehiculo', "Vehiculo nro", "Carga [kg]", x, y)
        plt.show()
        


