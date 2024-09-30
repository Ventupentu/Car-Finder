def capturar_preferencias_usuario():
    presupuesto_max = float(input("¿Cuál es tu presupuesto máximo en dólares?: "))
    combustible_preferido = input("¿Qué tipo de combustible prefieres? (gasolina, diésel, eléctrico, híbrido): ").lower()
    anio_min = float(input("¿Cuál es el año mínimo del coche que estás buscando?: "))
    
    # Opcional: puedes añadir preguntas con respuestas difusas como "¿Cuán importante es el consumo de combustible?"
    consumo_importancia = input("¿Qué tan importante es el consumo de combustible para ti? (1-10): ")

    return {
        "presupuesto_max": presupuesto_max,
        "combustible_preferido": combustible_preferido,
        "anio_min": anio_min,
        "consumo_importancia": consumo_importancia
    }
