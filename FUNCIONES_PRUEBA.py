

@staticmethod
def kpi_generico(itinerarios_final, key_func, vehiculos_por_modo=None, tupla_solicitud=None):
    if not itinerarios_final:
        return None

    mejor_valor = float('inf')
    id_res = None
    res = None

    for id, itinerario in itinerarios_final.items():
        valor = key_func(id, itinerario, vehiculos_por_modo, tupla_solicitud)
        if valor < mejor_valor:
            mejor_valor = valor
            id_res = id
            res = itinerario

    return (id_res, res)


# Tiempo total
def criterio_tiempo(id, itinerario, vehiculos_por_modo=None, tupla_solicitud=None):
    return itinerario.getTiempo()

# Costo total
def criterio_costo(id, itinerario, vehiculos_por_modo=None, tupla_solicitud=None):
    return itinerario.getCosto()

# Consumo por kg
def criterio_consumo(id, itinerario, vehiculos_por_modo, tupla_solicitud):
    carga_kg = tupla_solicitud[1]["peso_kg"]
    vehiculo = vehiculos_por_modo[itinerario.getModo().lower()]
    consumo_total = sum(vehiculo.calcular_combustible(conexion.getDistancia(), conexion, carga_kg)
                        for conexion in itinerario.getCamino())
    return consumo_total / carga_kg


"""
if __name__ == "__main__":
    mejor_kpi1 = Itinerario.kpi_generico(Itinerario.itinerarios_dict, Itinerario.criterio_tiempo)
    mejor_kpi2 = Itinerario.kpi_generico(Itinerario.itinerarios_dict, Itinerario.criterio_costo)
    mejor_kpi3 = Itinerario.kpi_generico(Itinerario.itinerarios_dict, Itinerario.criterio_consumo, vehiculos_por_modo= Itinerario.vehiculos_por_modo, tupla_solicitud= Itinerario.solicitud_tupla)

"""