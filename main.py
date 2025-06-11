# main.py
from redes import construir_red
from itinerarios import construir_itinerario, calcular_costos_y_tiempos, imprimir_costos_y_tiempos, kp1, kp2
from solicitudes import solicitudes


#este saca la solicitud del csv (chequear), deje el otro abajo por las dudas
if __name__ == "__main__":
    nodos_existentes = construir_red()

    for id_carga, datos in solicitudes.items():
        print(f"\nProcesando solicitud: {id_carga}")
        resultados = construir_itinerario(nodos_existentes, {id_carga: datos})
        evaluados = calcular_costos_y_tiempos(resultados, carga_kg=datos["peso_kg"])
        imprimir_costos_y_tiempos(evaluados)


        print(kp1(evaluados))


        print(kp2(evaluados))

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
    evaluados = calcular_costos_y_tiempos(resultados, carga_kg=70000)
    imprimir_costos_y_tiempos(evaluados) 
    print(kp1(evaluados))
    print(kp2(evaluados))
    #print(evaluados)
'''