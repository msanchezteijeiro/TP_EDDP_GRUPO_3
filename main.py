# main.py
from redes import construir_red
from itinerarios import construir_itinerario, calcular_costos_y_tiempos, imprimir_costos_y_tiempos, kp1, kp2

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