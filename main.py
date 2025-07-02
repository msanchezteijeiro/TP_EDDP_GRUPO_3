from redes import construir_red
from solicitudes import extraer_solicitudes
from vehiculos import instanciar_vehiculos
from itinerarios import Itinerario
from graficos import Grafico



if __name__ == "__main__":
    try:
        #Construyo la Red
        nodos_disponibles = construir_red()

        #Extraemos las solicitudes de los csv
        solicitudes = extraer_solicitudes()

        #Instancio los vehiculos: 
        vehiculos_por_modo, ferroviaria, automotor, fluvial, aerea = instanciar_vehiculos()

        #RECORRO SOLICITUDES:
        for tupla_solicitud in solicitudes.items(): 
            id_carga, datos = tupla_solicitud #datos es un dict con claves (peso_kg, origen, destino)
            print("\n\n" + ("-" * 150))
            print(f"\nProcesando solicitud: {id_carga} | Peso = {datos['peso_kg']:<.2f}kg | {datos['origen']} → {datos['destino']}")
        
            itinerarios_final = Itinerario.itinerario_por_solicitud(nodos_disponibles, tupla_solicitud, vehiculos_por_modo)
            Itinerario.imprimir_itinerario_final(itinerarios_final)
            

            resultado_indicador_rend_tiempo = Itinerario.indicador_rend_tiempo(itinerarios_final)
            resultado_indicador_rend_costo = Itinerario.indicador_rend_costo(itinerarios_final)
            resultado_indicador_rend_combustible = Itinerario.indicador_rend_combustible(itinerarios_final, vehiculos_por_modo, tupla_solicitud)

            Itinerario.imprimir_indicador_rend_tiempo(resultado_indicador_rend_tiempo)
            Itinerario.imprimir_indicador_rend_costo(resultado_indicador_rend_costo)
            Itinerario.imprimir_indicador_rend_combustible(resultado_indicador_rend_combustible)


            #Grafico de Distancia Acumulada vs. Tiempo Acumulado: : Para el Itinerario KPI 1
            Grafico.graf_distancia_vs_tiempo(tupla_solicitud, itinerarios_final, resultado_indicador_rend_tiempo, vehiculos_por_modo)

            #Grafico de Costo Acumulado vs Distancia Acumulada: Para el Itinerario KPI 2
            Grafico.graf_tiempo_vs_costo(tupla_solicitud, itinerarios_final, resultado_indicador_rend_costo, vehiculos_por_modo)

            #Grafico de Cantidad de Caminos Posibles por Modo:
            Grafico.graf_cantidad_vs_modo(itinerarios_final, tupla_solicitud,vehiculos_por_modo)
            
            #Grafico de carga por vehiculo por cantidad de vehiculos:
            Grafico.graf_carga_por_unidad(resultado_indicador_rend_tiempo, tupla_solicitud)
 

            
    except Exception as e:
        print(f'Error: {e}')

