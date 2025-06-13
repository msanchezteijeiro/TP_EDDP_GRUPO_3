# main.py
from redes import construir_red
from itinerarios import construir_itinerario, calcular_costos_y_tiempos, imprimir_costos_y_tiempos, kp1, kp2
from solicitudes import solicitudes


#este saca la solicitud del csv (chequear), deje el otro abajo por las dudas
if __name__ == "__main__":

    #aca creo q va un try:

    nodos_existentes = construir_red()

    for id_carga, datos in solicitudes.items():
        print(f"\n\nProcesando solicitud: {id_carga}")
        resultados = construir_itinerario(nodos_existentes, {id_carga: datos})
        itinerarios_final = calcular_costos_y_tiempos(resultados, carga_kg=datos["peso_kg"])
        imprimir_costos_y_tiempos(itinerarios_final)


        print(kp1(itinerarios_final))


        print(kp2(itinerarios_final))

#no se porque no aparecen todos los vehiculos en la terminal, habria que chequear
'''
if __name__ == "__main__":
    nodos_existentes = construir_red()
    solicitud = {
        'CARGA_001': {
            'peso_kg': 70000.0,
            'origen': 'Zarate',
            'destino': 'Mar_del_Plata'
        }
    }
    resultados = construir_itinerario(nodos_existentes, solicitud)
    itinerarios_final = calcular_costos_y_tiempos(resultados, carga_kg=70000)
    imprimir_costos_y_tiempos(evaitinerarios_finalluados) 
    print(kp1(itinerarios_final))
    print(kp2(itinerarios_final))
    #print(itinerarios_final)
'''