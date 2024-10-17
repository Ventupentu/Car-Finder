
def calculate_rating_for_opposite_car(recommender, user_preferences):
    """
    Calcula la puntuación que recibiría un coche completamente opuesto a las preferencias del usuario.
    
    :param recommender: Instancia del modelo de recomendación entrenado.
    :param user_preferences: Diccionario con las preferencias del usuario.
    :return: Puntuación estimada para el coche opuesto.
    """
    # Crear un coche con características completamente distintas a las preferencias del usuario
    opposite_car = {
        'make': 'FIAT',               # Marca distinta
        'model': 'Punto',             # Modelo distinto
        'price': 10000,               # Mucho más barato
        'fuel': 'Diesel',             # Combustible distinto
        'year': 2005,                 # Mucho más viejo
        'kms': 250000,                # Muchos más kilómetros
        'power': 60,                  # Mucha menos potencia
        'doors': 3,                   # Menos puertas
        'shift': 'Manual',            # Cambio distinto
        'color': 'Blanco',            # Color distinto
        'province': 'Barcelona'       # Provincia distinta
    }

    # Obtener la puntuación estimada para este coche distinto
    opposite_rating = recommender.predict_rating_new_user(
        model_id='99999',  # ID ficticio para el coche opuesto
        car_features=opposite_car,
        preferences=user_preferences
    )

    print("\nCoche completamente distinto a las preferencias del usuario:")
    print(f"Marca: {opposite_car['make']}, Modelo: {opposite_car['model']}, Precio: {opposite_car['price']}")
    print(f"Año: {opposite_car['year']}, Kilómetros: {opposite_car['kms']}, Potencia: {opposite_car['power']}")
    print(f"Puertas: {opposite_car['doors']}, Combustible: {opposite_car['fuel']}, Color: {opposite_car['color']}")
    print(f"Provincia: {opposite_car['province']}")
    print(f"\nPuntuación estimada para el coche distinto: {opposite_rating:.2f}")
    
    return opposite_rating


