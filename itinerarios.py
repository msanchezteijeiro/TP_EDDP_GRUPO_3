from datetime import timedelta

class Itinerario:
    def __init__(self, modo: str, camino: list, costo: float, tiempo: float):
        
        self.setModo(modo)
        self.setCamino(camino)
        self.setCosto(costo)
        self.setTiempo(tiempo)

    def setModo(self, modo):
        self.modo = modo

    def setCamino(self, camino):
        self.camino = camino

    def setCosto(self, costo):
        self.costo = costo

    def setTiempo(self, tiempo):
        self.tiempo = tiempo

    def getModo(self):
        return self.modo

    def getCamino(self):
        return self.camino

    def getCosto(self):
        return self.costo

    def getTiempo(self):
        return self.tiempo


    def __repr__(self):
        rec_fin = [self.getCamino()[0].getOrigen().getNombre()]
        for conexion in self.getCamino():
            rec_fin.append(conexion.getDestino().getNombre())
        camino_str = " -> ".join(rec_fin)
        #aca c.getOrigen() trae un nodo y el getNombre trae el nombre de ese nodo. lo mismo para el destino
        SANGRIA = "  "
        return (f"{SANGRIA}● Modo: {self.modo.capitalize()}\n"
                f"{SANGRIA}● Itinerario: {camino_str}\n"
                f"{SANGRIA}● Costo Total: ${self.costo:.2f}\n"
                f"{SANGRIA}● Tiempo Total (min): {self.tiempo:.2f} minutos\n"
                f"{SANGRIA}● Tiempo Total (HH:MM:SS): {self.formatear_tiempo_minutos(self.tiempo)}")
    
    @staticmethod
    def formatear_tiempo_minutos(tiempo_en_min):
        return str(timedelta(minutes=tiempo_en_min))
    

    #función que busca todos los caminos posibles entre dos nodos, con un solo modo de transporte y sin ciclos
    @staticmethod
    def buscador_caminos(nodos, actual, destino, camino, visitados, modo, itinerarios_base):
        #si ya llegmos al destino, termina el árbol
        if actual == destino:
            if modo not in itinerarios_base:
                itinerarios_base[modo] = []
            itinerarios_base[modo].append(list(camino))
            return itinerarios_base

        #marcamos el nodo como visitado
        visitados.append(actual)

        for vecino, conexiones in nodos[actual].getVecinos().items():
            if vecino in visitados:
                continue

            for conexion in conexiones:
                if conexion.getModo() == modo:
                    camino.append(conexion)
                    Itinerario.buscador_caminos(nodos, vecino, destino, camino, visitados, modo, itinerarios_base)
                    camino.pop()

        visitados.pop()
        return itinerarios_base 

    @staticmethod
    def construir_itinerario(nodos, solicitud_tupla):
        itinerarios_base = {}

        _, datos = solicitud_tupla
        origen = datos["origen"]
        destino = datos["destino"]

        modos_disponibles = nodos[origen].getModosSoportados()

        for modo in modos_disponibles:
            if origen in nodos and destino in nodos:
                itinerarios_base = Itinerario.buscador_caminos(nodos, origen, destino, [], [], modo, itinerarios_base)

        return itinerarios_base



    #Funcion que calcula costos y tiempos y los agrega a los itinerarios base.
    @staticmethod
    def calcular_costos_y_tiempos(itinerarios_base, carga_kg, vehiculos_por_modo):
        itinerarios_final = {}
        id_actual = 1

        for modo, caminos in itinerarios_base.items(): #modo es un str, caminos una lista de listas con las conexiones.
            vehiculo = vehiculos_por_modo.get((modo.lower())) #del diccionario vehiculos_por_modo, se el objeto vehiculo correspondiente al modo
            if vehiculo is None:
                continue #osea si no existe ese vehiculo este ni siquiera es analizado, ni aparecera en el dict "itinerarios_final" devuelto

            for camino in caminos: #camino es una lista de objetos conexion
                costo_total_camino = vehiculo.calcular_costo_carga(camino, carga_kg)
                tiempo_total_camino = 0

                for conexion in camino: #cada camino es una forma de ir, osea un itinerario
                    costo_total_camino += vehiculo.calcular_costo_tramo(conexion, carga_kg)
                    tiempo_total_camino += vehiculo.calcular_tiempo(conexion)
                info = Itinerario(modo, camino, costo_total_camino, tiempo_total_camino) #instancio ese itinerario
                itinerarios_final[id_actual] = info
                id_actual += 1

        return itinerarios_final #es un dict: clave: id, valor: objeto itinerario correspondiente


    #Funcion unificada que llamo desde el main:
    @staticmethod
    def itinerario_por_solicitud(nodos_existentes, solicitud_tupla, vehiculos_por_modo):
        itinerario_sin_costos = Itinerario.construir_itinerario(nodos_existentes, solicitud_tupla)
        # Extraemos de la tupla, el diccionario datos
        _, datos = solicitud_tupla #pues se que no usare id_carga
        
        itinerarios_final_por_solicitud = Itinerario.calcular_costos_y_tiempos(itinerario_sin_costos, datos["peso_kg"], vehiculos_por_modo)
        
        return itinerarios_final_por_solicitud



    #Funcion para imprimir tabla itinerarios
    @staticmethod
    def imprimir_itinerario_final(itinerarios_final):

        if not itinerarios_final:
            print(f"\nNo existen itinerarios posibles para la solicitud pedida.")

        else:
            print("")
            print(f"{'ID':<4} | {'Modo':<12} | {'Costo Total':<12} | {'Tiempo Total (min)':<20} | Itinerario")
            print("-" * 125)
            
            for id_, itinerario in itinerarios_final.items():
                camino_limpio = [itinerario.getCamino()[0].getOrigen().getNombre()] #empiezo lista con el primer nodo origen 
                
                camino_limpio += [c.getDestino().getNombre() for c in itinerario.getCamino()] #le agregamos solo los destinos de cada conexion
                camino_str = " → ".join(camino_limpio) #transformamos la lista final en un str
                print(f"{id_:<4} | {itinerario.getModo().capitalize():<12} | ${itinerario.getCosto():<11.2f} | {itinerario.getTiempo():<20.2f} | {camino_str}")



    @staticmethod
    def indicador_por_rend(itinerarios_final, funcion_rendimiento, funcion_impresion, **kwargs):
        if not itinerarios_final:
            funcion_impresion(None)  # Imprime mensaje de "no hay itinerarios"
            return None

        mejor_valor = float('inf') #Parte del inf como mejor valor, y luego recorre para encontrar el menor.
        id_res = None
        res = None

        for id, itinerario in itinerarios_final.items():

            #rendimiento es un valor obtenido con la funcion pasada por parametro
            rendimiento = funcion_rendimiento(itinerario, **kwargs)

            if rendimiento < mejor_valor: #si es menor al que tenia, lo reemplazo
                mejor_valor = rendimiento
                id_res = id
                res = itinerario

        par_res = (id_res, res)
        funcion_impresion(par_res)  # Imprime el resultado del mejor itinerario

        return par_res #Luego de recorrer todo, me queda el itineario con menor valor, osea el mejor optimizado


    # Criterio 1: Tiempo total: Obtenes el tiempo del itinerario recibido por parametro.
    @staticmethod
    def rendimiento_por_tiempo(itinerario, **kwargs):
        return itinerario.getTiempo()


    # Criterio 2: Costo total: Obtenes el costo total del itinerario recibido
    @staticmethod
    def rendimiento_por_costo(itinerario, **kwargs):
        return itinerario.getCosto()


    # Criterio 3: Consumo por kg (usa kwargs: vehiculos_por_modo y tupla_solicitud) Obtenes el consumo por kg.
    @staticmethod
    def rendimiento_por_combustible(itinerario, **kwargs):

        if not ("vehiculos_por_modo" in kwargs and "tupla_solicitud" in kwargs): #chequea que esten en kwargs
            raise KeyError("Faltan parámetros requeridos: 'vehiculos_por_modo' y/o 'tupla_solicitud'.")
        vehiculos_por_modo = kwargs["vehiculos_por_modo"]
        tupla_solicitud = kwargs["tupla_solicitud"]

        carga_kg = tupla_solicitud[1].get("peso_kg") #chequa que carga sea positivo
        if not (carga_kg and carga_kg > 0):
            raise ValueError("La carga debe ser mayor que 0.")

        vehiculo = vehiculos_por_modo[itinerario.getModo().lower()] #identifica el vehiculo del q se trata

        consumo_total = 0

        for conexion in itinerario.getCamino(): #recorro cada conexion dentro del camino de ese itinerario
            consumo_total += vehiculo.calcular_combustible(conexion.getDistancia(), conexion, carga_kg) #en litros de combustible
        
        #Asigno el valor de consumo_por_kg, no hace falta validarlo, ya se validó arriba.
        consumo_por_kg = consumo_total / carga_kg  #queda en litros/kg

        return consumo_por_kg


    #Funciones para imprimir KPIs:
    @staticmethod
    def imprimir_rend_tiempo(par_res):
        if not par_res:
            print("\n\nNo hay itinerarios disponibles para el Indicador por Rendimiento de Tiempo.")
        else:
            id_res = par_res[0]
            res = par_res[1]
            print("\n\nMEJOR ITINERARIO SEGÚN: → | Indicador por Rendimiento: Minimizar el Tiempo Total de Entrega |")
            print("-" * 72)
            print(f"El itinerario {id_res} es el mejor.\n")
            print(res)

    @staticmethod
    def imprimir_rend_costo(par_res):
        if not par_res:
            print("\n\nNo hay itinerarios disponibles para el Indicador por Rendimiento de Costo.")
        else:
            id_res = par_res[0]
            res = par_res[1]
            print("\n\nMEJOR ITINERARIO SEGÚN: → | Indicador por Rendimiento: Minimizar el Costo Total del Transporte |")
            print("-" * 75)
            print(f"El itinerario {id_res} es el mejor.\n")
            print(res)

    @staticmethod
    def imprimir_rend_combustible(par_res): 
        if not par_res: 
            print("\n\nNo hay itinerarios disponibles para el Indicador por Rendimiento de Combustible.")
        else: 
            id_res = par_res[0]
            res = par_res[1]
            print("\n\nMEJOR ITINERARIO SEGÚN: → | Indicador por Rendimiento: Minimizar el consumo de combustible por kg de carga |")
            print("-" * 87)
            print(f"El itinerario {id_res} es el mejor.\n")
            print(res)

