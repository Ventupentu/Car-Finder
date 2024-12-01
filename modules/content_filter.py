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
        car_data = car_data.copy()
        car_data['similarity_score'] = 0.0

        # Normalizar pesos
        total_weight = sum(feature_weights.values())
        if total_weight > 0:
            for feature in feature_weights:
                feature_weights[feature] /= total_weight

        for feature, weight in feature_weights.items():
            if feature in user_input and user_input[feature] is not None:
                user_value = user_input[feature]

                if feature in ['price', 'year', 'kms', 'power']:  # Características numéricas
                    max_val = car_data[feature].max()
                    min_val = car_data[feature].min()

                    if feature in ['price', 'kms']:
                        normalized_diff = np.where(
                            car_data[feature] > user_value,
                            1 - ((car_data[feature] - user_value) / (max_val - user_value + 1e-6)),
                            1.0
                        )
                    else:
                        normalized_diff = 1 - abs(car_data[feature] - user_value) / (max_val - min_val + 1e-6)

                    car_data['similarity_score'] += normalized_diff * weight

                elif feature in ['fuel', 'shift', 'color', 'make', 'model', 'doors']:
                    car_data['similarity_score'] += car_data[feature].apply(
                        lambda x: weight if str(x).lower() == str(user_value).lower() else weight * 0.5
                        if feature == 'fuel' and str(x).lower() in str(user_value).lower()
                        else 0
                    )

        # Bonus por coincidencias exactas
        for feature in user_input:
            if feature in car_data.columns and user_input[feature] is not None:
                exact_match_bonus = 0.2  # Peso del bonus
                car_data['similarity_score'] += car_data[feature].apply(
                    lambda x: exact_match_bonus if str(x).lower() == str(user_input[feature]).lower() else 0
                )

        # Normalizar el puntaje final entre 0 y 1
        max_score = car_data['similarity_score'].max()
        if max_score > 0:
            car_data['similarity_score'] /= max_score

        return car_data.sort_values(by='similarity_score', ascending=False)
