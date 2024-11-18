from modules.hybrid_recommender import hybrid_recommendation
from modules.collaborative_filter import train_collaborative_model
from modules.geo_utils import GeoDistanceCalculator
from modules.data_loader import load_data
import time

# Configuración
cars_path = 'data/coches.csv'
ratings_path = 'data/car_ratings.csv'
user_id = 'new_user'


def get_user_input():
    """
    Solicita al usuario que ingrese sus preferencias para un coche y los pesos correspondientes.
    Incluye la ciudad obligatoria y la importancia de la distancia.
    
    :return: Diccionario con las características del coche, los pesos y la ubicación del usuario.
    """
    print("Introduce tus preferencias para un coche ideal:")
    
    # Características del coche
    user_input = {}
    feature_weights = {}

    # Solicitar características
    user_input['make'] = input("Marca del coche: ").strip()
    user_input['price'] = input("Precio del coche: ").strip()
    user_input['fuel'] = input("Tipo de combustible (Diesel, Gasolina, Eléctrico, Híbrido): ").strip()
    user_input['year'] = input("Año del coche: ").strip()
    user_input['kms'] = input("Kilometraje del coche: ").strip()
    user_input['power'] = input("Potencia del coche en caballos: ").strip()
    user_input['doors'] = input("Número de puertas (2, 3, 4, 5): ").strip()
    user_input['shift'] = input("Tipo de transmisión (Automático, Manual): ").strip()
    user_input['color'] = input("Color del coche: ").strip()

    # Convertir inputs numéricos a tuplas de (min, max) para los rangos
    for key, value in user_input.items():
        if '-' in value:
            try:
                min_value, max_value = map(int, value.split('-'))
                user_input[key] = (min_value, max_value)
            except ValueError:
                user_input[key] = value
        elif value.isdigit():
            user_input[key] = int(value)
        elif value == "":
            user_input[key] = None

    # Solicitar ubicación obligatoria
    while True:
        user_location = input("Introduce tu ubicación (ciudad): ").strip()
        if user_location:
            break
        print("La ubicación es obligatoria. Por favor, ingresa tu ciudad.")

    # Solicitar pesos para todas las características
    print("\nAhora, por favor, asigna un peso del 1 al 10 a cada característica que hayas seleccionado.")
    print("Si no has seleccionado una característica, pon un peso de 0 para esa opción.")
    
    # Pedir el peso para todas las características
    for key in user_input:
        if user_input[key] is not None:
            while True:
                try:
                    weight = int(input(f"Peso para {key} (debe ser entre 0 y 10): "))
                    if 0 <= weight <= 10:
                        break
                    else:
                        print("El peso debe estar entre 0 y 10. Intenta de nuevo.")
                except ValueError:
                    print("Por favor, ingresa un número válido entre 0 y 10.")
            feature_weights[key] = weight
        else:
            feature_weights[key] = 0

    # Solicitar importancia de la distancia (obligatoria)
    while True:
        try:
            distance_weight = int(input("¿Qué importancia le das a la distancia? (debe ser entre 0 y 10): "))
            if 0 <= distance_weight <= 10:
                break
            else:
                print("El peso debe estar entre 0 y 10. Intenta de nuevo.")
        except ValueError:
            print("Por favor, ingresa un número válido entre 0 y 10.")
    feature_weights['distance'] = distance_weight

    # Validar que se haya seleccionado al menos una característica
    if all(value == 0 for value in feature_weights.values()):
        print("Debes asignar al menos un peso mayor que 0 para realizar la recomendación.")
        return None, None, None

    return user_input, feature_weights, user_location


if __name__ == '__main__':
    
    # Configuración
    user_input, feature_weights, user_location = get_user_input()
    a = time.time()
    if user_input is None or feature_weights is None or user_location is None:
        print("No se puede realizar la recomendación sin entradas válidas.")
    else:
        # Cargar datos
        cars_df, ratings_df = load_data(cars_path, ratings_path)

        # Entrenar modelo colaborativo con GridSearch habilitado
        use_gridsearch = True  # Cambiar a False si no deseas ajustar hiperparámetros
        collaborative_model, _ = train_collaborative_model(ratings_path)

        # Instanciar calculadora geográfica
        geo_calculator = GeoDistanceCalculator()

        # Generar recomendaciones
        recommendations = hybrid_recommendation(
            user_id, user_input, feature_weights, user_location,
            geo_calculator, collaborative_model, cars_df
        )

        # Mostrar resultados
        top_5 = recommendations[['make', 'model', 'price', 'fuel', 'year', 'kms', 
                                  'power', 'doors', 'shift', 'color', 'province', 
                                  'distance', 'hybrid_score']].head(5)
        print("Hemos encontrado estos coches para ti:")
        print(top_5.to_string(index=False))

    b = time.time()

    print(f"Tiempo de ejecución: {b - a:.2f} segundos.")

