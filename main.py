# main.py
from redes import construir_red
from itinerarios import construir_itinerario, calcular_costos_y_tiempos, imprimir_itinerario_final, kpi_1, kpi_2, imprimir_kpi_1, imprimir_kpi_2
from solicitudes import solicitudes


if __name__ == "__main__":

    #aca creo q va un try:

    nodos_existentes = construir_red()

    for id_carga, datos in solicitudes.items(): #datos es un dict con claves (peso_kg, origen, destino)
        print("\n\n" + ("-" * 150))
        print(f"\nProcesando solicitud: {id_carga} | Peso = {datos["peso_kg"]:<.2f}kg | {datos["origen"]} → {datos["destino"]}")
        
        resultados = construir_itinerario(nodos_existentes, {id_carga: datos}) #fusionar estas dos en una sola funcion
        itinerarios_final = calcular_costos_y_tiempos(resultados, carga_kg=datos["peso_kg"]) #asi aca en el main sale una sola
        
        imprimir_itinerario_final(itinerarios_final)

        resultado_kpi_1 = kpi_1(itinerarios_final)
        resultado_kpi_2 = kpi_2(itinerarios_final)

        imprimir_kpi_1(resultado_kpi_1)
        imprimir_kpi_2(resultado_kpi_2)



