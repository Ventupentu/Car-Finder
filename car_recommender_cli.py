from modules.hybrid_recommender import HybridRecommender
from modules.collaborative_filter import CollaborativeFilter
from modules.geo_utils import GeoUtils
from modules.data_loader import DataLoader
import os

class CarRecommenderApp:
    """
    CarRecommenderApp es una aplicación de consola que recomienda coches a los usuarios
    basándose en sus preferencias y ubicación.

    Atributos:
        cars_path (str): Ruta al archivo CSV que contiene los datos de los coches.
        ratings_path (str): Ruta al archivo CSV que contiene las valoraciones de los usuarios.
        distance_cache (str): Ruta al archivo CSV que contiene el caché de distancias.
        user_id (str): Identificador del usuario para el que se generan las recomendaciones.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase CarRecommenderApp.
        """
        self.cars_path = 'data/coches.csv'
        self.ratings_path = 'data/car_ratings.csv'
        self.distance_cache = 'data/distance_cache.csv'
        self.user_id = 'new_user'

    def check_csv_files(self):
        """
        Verifica si los archivos CSV necesarios para la aplicación existen en las rutas especificadas.

        Returns:
            bool: True si los archivos existen, False en caso contrario.
        """
        files = [self.cars_path, self.ratings_path, self.distance_cache]
        missing_files = [file for file in files if not os.path.exists(file)]
        if missing_files:
            print(f"Faltan los siguientes archivos: {missing_files}")
            return False
        return True
    
    def get_user_input(self):
        """
        Solicita al usuario las preferencias para un coche ideal y los pesos para cada característica.

        Returns:
            tuple: Una tupla que contiene el diccionario de preferencias del usuario, los pesos de las características y la ubicación del usuario.
        """
        print("Introduce tus preferencias para un coche ideal:")
        
        # Características del coche
        user_input = {}
        feature_weights = {}

        # Funciones para comprobar los tipos correctos de entrada
        def get_string_input(prompt):
            while True:
                value = input(prompt).strip()
                if value == "":
                    return None
                elif type(value) == str:
                    return value
                else:
                    print("Se requiere un texto. Intenta de nuevo.")

        def get_numeric_input(prompt):
            while True:
                value = input(prompt).strip()
                if value.isdigit():
                    return int(value)
                elif value == "":
                    return None
                else:
                    print("Se requiere un número. Intenta de nuevo.")

        # Solicitar las preferencias del usuario
        user_input['make'] = get_string_input("Marca del coche: ")
        user_input['price'] = get_numeric_input("Precio del coche: ")
        user_input['fuel'] = get_string_input("Tipo de combustible: ")
        user_input['year'] = get_numeric_input("Año del coche: ")
        user_input['kms'] = get_numeric_input("Kilometraje del coche: ")
        user_input['power'] = get_numeric_input("Potencia del coche en caballos: ")
        user_input['doors'] = get_numeric_input("Número de puertas: ")
        user_input['shift'] = get_string_input("Tipo de transmisión: ")
        user_input['color'] = get_string_input("Color del coche: ")

        # Solicitar ubicación obligatoria
        while True:
            user_location = input("Introduce tu ubicación (ciudad): ").strip().capitalize()
            if user_location and not user_location.isdigit():
                break
            print("La ubicación es obligatoria y debe ser un texto. Por favor, ingresa tu ciudad.")

        # Solicitar pesos para todas las características
        print("\nAhora, por favor, asigna un peso del 1 al 10 a cada característica que hayas seleccionado.")
        print("Si no has seleccionado una característica, pon un peso de 0 para esa opción.")
        
        # Pedir el peso para todas las características
        for key in user_input:
            if user_input[key] is not None:
                while True:
                    try:
                        weight = int(input(f"Peso para {key} (debe ser entre 1 y 10): "))
                        if 1 <= weight <= 10:
                            break
                        else:
                            print("El peso debe estar entre 1 y 10. Intenta de nuevo.")
                    except ValueError:
                        print("Por favor, ingresa un número válido entre 1 y 10.")
                feature_weights[key] = weight
            else:
                feature_weights[key] = 0

        # Solicitar importancia de la distancia (obligatoria)
        while True:
            try:
                distance_weight = int(input("¿Qué importancia le das a la distancia? (debe ser entre 1 y 10): "))
                if 1 <= distance_weight <= 10:
                    break
                else:
                    print("El peso debe estar entre 1 y 10. Intenta de nuevo.")
            except ValueError:
                print("Por favor, ingresa un número válido entre 1 y 10.")
        feature_weights['distance'] = distance_weight

        # Validar que se haya seleccionado al menos una característica
        if all(value == 0 for value in feature_weights.values()):
            print("Debes asignar al menos un peso mayor que 0 para realizar la recomendación.")
            return None, None, None

        return user_input, feature_weights, user_location

    def run(self):
        """
        Ejecuta la aplicación de recomendación de coches.
        """
        # Verificar si los archivos CSV necesarios existen
        if not self.check_csv_files():
            exit()

        # Cargar datos de coches y valoraciones
        cars_df, _ = DataLoader(self.cars_path, self.ratings_path).load_data()

        # Entrenar el modelo de filtrado colaborativo
        collaborative_model = CollaborativeFilter()
        collaborative_model.train_model(self.ratings_path)

        # Inicializar el calculador de distancias geográficas
        geo_calculator = GeoUtils()

        # Obtener las preferencias del usuario
        user_input, feature_weights, user_location = self.get_user_input()
        
        # Inicializar el recomendador híbrido
        recommender = HybridRecommender(collaborative_model, geo_calculator)
        # Obtener recomendaciones
        recommendations = recommender.recommend(self.user_id, user_input, feature_weights, user_location, cars_df)
        
        # Mostrar las 10 mejores recomendaciones
        top_5 = recommendations[['make', 'model', 'price', 'fuel', 'year', 'kms', 
                                  'power', 'doors', 'shift', 'color', 'province', 
                                  'distance']].head(10)
        
        print("Hemos encontrado estos coches para ti:")
        print(top_5.to_string(index=False))


if __name__ == "__main__":
    # Crear una instancia de la aplicación y ejecutarla
    app = CarRecommenderApp()
    app.run()
