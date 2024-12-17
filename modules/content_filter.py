import pandas as pd
import numpy as np

class ContentFilter:
    @staticmethod
    def calculate_content_similarity(user_input: dict, car_data: pd.DataFrame, feature_weights: dict) -> pd.DataFrame:
        """
        Calcula la similitud entre las características deseadas por el usuario y los coches.

        :param user_input: Diccionario con las preferencias del usuario.
        :param car_data: DataFrame con los datos de los coches.
        :param feature_weights: Diccionario con los pesos asignados a cada característica.
        :return: DataFrame con un puntaje de similitud para cada coche.
        """
        # Crear una copia del DataFrame original para evitar modificarlo directamente
        car_data = car_data.copy()
        
        # Inicializar una nueva columna para almacenar el puntaje de similitud
        car_data['similarity_score'] = 0.0

        # Normalizar los pesos de las características para que sumen 1
        total_weight = sum(feature_weights.values())
        if total_weight > 0:
            for feature in feature_weights:
                feature_weights[feature] /= total_weight
            

        # Calcular la similitud para cada característica
        for feature, weight in feature_weights.items():
            if feature in user_input and user_input[feature] is not None:
                user_value = user_input[feature]

                # Características numéricas
                if feature in ['price', 'year', 'kms', 'power']:
                    max_val = car_data[feature].max()
                    min_val = car_data[feature].min()

                    if feature in ['price', 'kms']:
                        # (menor es mejor)
                        normalized_diff = np.where(
                            car_data[feature] < user_value,
                            1,
                            1 - (car_data[feature] - user_value) / (max_val - user_value)
                        )
                    else:
                        # (mayor es mejor)
                        normalized_diff = np.where(
                            car_data[feature] > user_value,
                            1,
                            1 - (car_data[feature] - user_value) / (max_val - user_value)
                        )

                    # Ajustar el puntaje de similitud según el peso de la característica
                    car_data['similarity_score'] += normalized_diff * weight

                # Características categóricas
                elif feature in ['fuel', 'shift', 'color', 'make', 'model', 'doors']:
                    # Asignar un puntaje según si hay coincidencia exacta o no
                    def category_score(value):
                        if str(value).lower() == str(user_value).lower():
                            return weight  # Coincidencia exacta
                        else:
                            return weight * 0.5 if weight < 5 else 0  # Penalización según peso

                    car_data['similarity_score'] += car_data[feature].apply(category_score)

        # Bonus adicional por coincidencias exactas en ciertas características
        for feature in user_input:
            if feature in car_data.columns and user_input[feature] is not None:
                exact_match_bonus = 0.2 * feature_weights.get(feature, 0)
                car_data['similarity_score'] += car_data[feature].apply(
                    lambda x: exact_match_bonus if str(x).lower() == str(user_input[feature]).lower() else 0
                )

        # Normalizar el puntaje final entre 0 y 1 para que sea comparable
        max_score = car_data['similarity_score'].max()
        if max_score > 0:
            car_data['similarity_score'] /= max_score

        # Ordenar los coches según el puntaje de similitud de mayor a menor
        return car_data.sort_values(by='similarity_score', ascending=False)
