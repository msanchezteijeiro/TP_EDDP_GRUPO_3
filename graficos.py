import matplotlib.pyplot as plt
import numpy as np
from vehiculos import Vehiculo

class Grafico: 
    
    @staticmethod
    def grafico_barras(titulo, nombre_x, nombre_y, lista_x, lista_y, ticksy):
        plt.title(label= titulo, fontsize=10, color='black')
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        plt.bar(lista_x, lista_y,color='green',width=0.5)
        plt.grid()
        plt.xticks(rotation=0, ha='center')
        plt.yticks(ticksy)
        
    @staticmethod
    def grafico_torta(titulo, secciones, cantidades):
        plt.pie(cantidades,labels=secciones, autopct='%1.2f%%')
        plt.title(label=titulo, loc='center', color='blue')
        
    @staticmethod 
    def grafico_lineal(titulo, nombre_x, nombre_y, x1, y1, descripción, color): #linea 1 y linea2 son los nombres de las dos lineas
        plt.title(titulo,fontsize=10, color='black')
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        # Grafica de lineas
        plt.plot(x1,y1,color=color,linewidth=3, marker="o",label=descripción)
        plt.grid()
        plt.legend()
        


    @staticmethod
    def graf_distancia_vs_tiempo(tupla_solicitud, itinerarios_final, resultado_indicador_rend_tiempo, vehiculos_por_modo):
        id_carga, datos = tupla_solicitud

        if not itinerarios_final:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")

        # Usamo el itinearaio recibido por parametro
        nro_itinerario, mejor_itinerario = resultado_indicador_rend_tiempo
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

        Grafico.grafico_lineal(f'{id_carga} / Itinerario N°{nro_itinerario}: Optimiza el Tiempo / Modo {mejor_itinerario.getModo().capitalize()}\n\nDistancia Acumulada vs. Tiempo Acumulado', "Tiempo Acumulado [min]", "Distancia Acumulada [km]", tiempo_acum, distancia_acum,"Distancia recorrida","black")

        plt.show()


    @staticmethod
    def graf_tiempo_vs_costo(tupla_solicitud, itinerarios_final, resultado_indicador_rend_costo, vehiculos_por_modo):
        id_carga, datos = tupla_solicitud

        if not itinerarios_final:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")

        nro_itinerario , mejor_itinerario = resultado_indicador_rend_costo
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
        Grafico.grafico_lineal(f'{id_carga} / Itinerario N°{nro_itinerario}: Optimiza el Costo / Modo {mejor_itinerario.getModo().capitalize()}\n\nDistancia Acumulada vs. Tiempo Acumulado', "Distancia Acumulada [km]", "Costo Acumulado [$]", distancia_acum, costo_fijo,"Costo fijo por carga","red")
        Grafico.grafico_lineal(f'{id_carga} / Itinerario N°{nro_itinerario}: Optimiza el Costo / Modo {mejor_itinerario.getModo().capitalize()}\n\nDistancia Acumulada vs. Tiempo Acumulado',"Distancia Acumulada [km]", "Costo Acumulado [$]", distancia_acum, costo_acum, "Costo por kilómetro","yellow")
        
        plt.show()


    @staticmethod
    def graf_combustible_vs_distancia(tupla_solicitud, itinerarios_final, resultado_indicador_rend_combustible, vehiculos_por_modo):
        id_carga, datos = tupla_solicitud

        if not itinerarios_final:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")

        nro_itinerario, mejor_itinerario = resultado_indicador_rend_combustible
        vehiculo = vehiculos_por_modo[mejor_itinerario.getModo().lower()]
        carga_kg = datos["peso_kg"]

        distancia_acum = [0]
        consumo_acum = [0]
        total_distancia = 0
        total_consumo = 0

        for conexion in mejor_itinerario.camino:
            distancia = conexion.getDistancia()
            consumo = vehiculo.calcular_combustible(distancia, conexion, carga_kg)

            total_distancia += distancia
            total_consumo += consumo

            distancia_acum.append(total_distancia)
            consumo_acum.append(total_consumo)

        Grafico.grafico_lineal(f'{id_carga} / Itinerario N°{nro_itinerario}: Optimiza el Consumo / Modo {mejor_itinerario.getModo().capitalize()}\n\nConsumo Acumulado vs. Distancia Acumulada', "Distancia Acumulada [km]", "Consumo Acumulado [litros]", distancia_acum, consumo_acum, "Consumo de combustible", "green")

        plt.show()


    @staticmethod
    def graf_cantidad_vs_modo(itinerarios_final,tupla_solicitud,vehiculos_por_modo):
        id_carga, datos = tupla_solicitud
        if not itinerarios_final:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")
        cant_modos = []
        for i in itinerarios_final.values():
            cant_modos.append(i.getModo())
        modos = []
        cantidad = []
        for elemento in cant_modos:
            if elemento not in modos:
                modos.append(elemento)
                cantidad.append(cant_modos.count(elemento))
        for vehiculo in vehiculos_por_modo.keys():
            if not(vehiculo in modos):
                modos.append(vehiculo)
                cantidad.append(0)
        X = np.array([m.capitalize() for m in modos])
        Y = np.array(cantidad)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.bar(X, Y, color='blue')

        ax.set_title(f'{id_carga}:\n\nCantidad de Caminos Posibles por Modo')
        ax.set_xlabel('Modo')
        ax.set_ylabel('Cantidad')

        plt.show()

    @staticmethod
    def graf_carga_por_unidad (resultado_indicador_rend_tiempo, tupla_solicitud):
        id_carga, datos = tupla_solicitud
        if not resultado_indicador_rend_tiempo:
            raise ValueError(f"No hay itinerarios disponibles para la solicitud {id_carga}.")
        carga = datos['peso_kg']
        modo = resultado_indicador_rend_tiempo[1].getModo()
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
                    resto = carga
                    cargas.append(carga)
                    cant_vehiculos += 1
                    vehiculos.append(cant_vehiculos)
                    carga = 0 
                carga_max = vehiculo.getCapacidad()
        nros_vehiculos = np.array(vehiculos)
        ticks = []
        for i in range(1,6):
            ticks.append(int(i * carga_max / 5))
        try:
            ticks.append(resto)
        except:
            pass
        
        x = nros_vehiculos.astype(str)
        y = np.array(cargas)
        Grafico.grafico_barras(f'{id_carga} / Itinerario N°{resultado_indicador_rend_tiempo[0]}: Optimiza el Tiempo / Modo {modo.capitalize()}\n\nCarga por Vehiculo', "Vehiculo N°", "Carga [kg]", x, y,sorted(ticks))
        
        """
        if len(nros_vehiculos) != 1:
            x = nros_vehiculos.astype(str)
            y = np.array(cargas)
            Grafico.grafico_barras(f'{id_carga} / Itinerario N°{resultado_indicador_rend_tiempo[0]}: Optimiza el Tiempo / Modo {modo.capitalize()}\n\nCarga por vehiculo', "Vehiculo N°", "Carga [kg]", x, y,sorted(ticks))
        
        else:
            nros_vehiculos = np.append(nros_vehiculos,[2])
            cargas.append(0)
            x = nros_vehiculos.astype(str)
            y = np.array(cargas)
            Grafico.grafico_barras(f'{id_carga} / Itinerario N°{resultado_indicador_rend_tiempo[0]}: Optimiza el Tiempo / Modo {modo.capitalize()}\n\nCarga por vehiculo', "Vehiculo N°", "Carga [kg]", x, y,sorted(ticks))
        """
        
        plt.show()
        


