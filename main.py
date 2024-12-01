from modules.hybrid_recommender import HybridRecommender
from modules.collaborative_filter import CollaborativeFilter
from modules.geo_utils import GeoUtils
from modules.data_loader import DataLoader
import os

class CarRecommenderApp:
    def __init__(self):
        self.cars_path = 'data/coches.csv'
        self.ratings_path = 'data/car_ratings.csv'
        self.distance_cache = 'data/distance_cache.csv'
        self.user_id = 'new_user'

    def check_csv_files(self):
        files = [self.cars_path, self.ratings_path, self.distance_cache]
        missing_files = [file for file in files if not os.path.exists(file)]
        if missing_files:
            print(f"Faltan los siguientes archivos: {missing_files}")
            return False
        return True
    
    def get_user_input(self):
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

        # Convertir valores numéricos a enteros y vacíos a None
        for key, value in user_input.items():
            if value.isdigit():
                user_input[key] = int(value)
            elif value == "":
                user_input[key] = None

        # Solicitar ubicación obligatoria
        while True:
            user_location = input("Introduce tu ubicación (ciudad): ").strip().capitalize()
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




    def run(self):
        if not self.check_csv_files():
            exit()

        cars_df, ratings_df = DataLoader(self.cars_path, self.ratings_path).load_data()

        collaborative_model = CollaborativeFilter()
        collaborative_model.train_model(self.ratings_path)

        geo_calculator = GeoUtils()

        user_input, feature_weights, user_location = self.get_user_input()
        

        recommender = HybridRecommender(collaborative_model, geo_calculator)
        recommendations = recommender.recommend(self.user_id, user_input, feature_weights, user_location, cars_df)
        
        top_5 = recommendations[['make', 'model', 'price', 'fuel', 'year', 'kms', 
                                  'power', 'doors', 'shift', 'color', 'province', 
                                  'distance']].head(10)
        
        print("Hemos encontrado estos coches para ti:")
        print(top_5.to_string(index=False))


if __name__ == "__main__":
    app = CarRecommenderApp()
    app.run()

