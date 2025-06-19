# main.py
import matplotlib.pyplot as plt
from redes import construir_red
from vehiculos import instanciar_vehiculos
from itinerarios import itinerario_por_solicitud, imprimir_itinerario_final, kpi_1, kpi_2, imprimir_kpi_1, imprimir_kpi_2
from solicitudes import solicitudes
from graficos import Grafico



if __name__ == "__main__":
    try:
    #Construyo la Red
        nodos_disponibles = construir_red()

        #Instancio los vehiculos:  NO FUNCIONA SI LOS INSTANCIAMOS ACA!!! REVISAR (sino quedaran en vehiculos)
        #vehiculos_por_modo, ferroviaria, automotor, fluvial, aerea = instanciar_vehiculos()

        #RECORRO SOLICITUDES:
        for tupla_solicitud in solicitudes.items(): 
            id_carga, datos = tupla_solicitud #datos es un dict con claves (peso_kg, origen, destino)
            print("\n\n" + ("-" * 150))
            print(f"\nProcesando solicitud: {id_carga} | Peso = {datos['peso_kg']:<.2f}kg | {datos['origen']} → {datos['destino']}")
        
            itinerarios_final = itinerario_por_solicitud(nodos_disponibles, tupla_solicitud)
            imprimir_itinerario_final(itinerarios_final)

            resultado_kpi_1 = kpi_1(itinerarios_final)
            resultado_kpi_2 = kpi_2(itinerarios_final)
            imprimir_kpi_1(resultado_kpi_1)
            imprimir_kpi_2(resultado_kpi_2)



            #Grafico de Costo Acumulado vs Distancia Acumulada: Para el Itinerario KPI 1
            tiempo_acum, distancia_acum_t = Grafico.obtener_datos_distancia_vs_tiempo(tupla_solicitud, itinerarios_final, resultado_kpi_1)

            #print(distancia_acum_t)
            #print(tiempo_acum)

            grafico1 = Grafico.grafico_lineal("Distancia Acumulada vs. Tiempo Acumulado", "Tiempo Acumulado [min]", "Distancia Acumulada [km]", tiempo_acum, distancia_acum_t)

            plt.show()


            #Grafico de Costo Acumulado vs Distancia Acumulada: Para el Itinerario KPI 2
            distancia_acum_c, costo_acum = Grafico.obtener_datos_costo_vs_distancia(tupla_solicitud, itinerarios_final, resultado_kpi_2)

            #print(distancia_acum_c)
            #print(costo_acum)

            grafico1 = Grafico.grafico_lineal("Costo Acumulado vs. Distancia Acumulada", "Distancia Acumulada [km]", "Costo Acumulado [$]", distancia_acum_c, costo_acum)


            plt.show()





    except Exception as e:
        print(f'Error: {e}')


