def recomendar_coches(coches, preferencias_usuario):
    presupuesto_max = float(preferencias_usuario["presupuesto_max"])
    combustible_preferido = preferencias_usuario["combustible_preferido"]
    anio_min = int(preferencias_usuario["anio_min"])

    # Filtrar coches según las preferencias
    coches_filtrados = [
        coche for coche in coches
        if float(coche.precio) <= float(presupuesto_max) and
           coche.combustible.lower() == combustible_preferido.lower() and
           float(coche.anio) >= float(anio_min)
    ]

    return coches_filtrados
