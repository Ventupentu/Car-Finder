import pandas as pd
import numpy as np

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
    
    for feature, weight in feature_weights.items():
        if feature in user_input and user_input[feature] is not None:
            user_value = user_input[feature]
            
            if feature in ['price', 'year', 'kms', 'power']:  # Características numéricas
                max_val = car_data[feature].max()
                min_val = car_data[feature].min()
                
                # Penalización para price y kms si son mayores que el valor del usuario
                if feature in ['price', 'kms']:
                    normalized_diff = np.where(car_data[feature] > user_value, 
                                               (car_data[feature] - user_value) / (max_val - user_value), 
                                               1.0)
                else:  # Normalización directa para year y power
                    normalized_diff = np.where(car_data[feature] < user_value, 
                                                (user_value - car_data[feature]) / (user_value - min_val), 
                                                1.0)

                car_data['similarity_score'] += normalized_diff * weight
            
            elif feature in ['fuel', 'shift', 'color', 'make', 'model', 'doors']:  # Características categóricas
                car_data['similarity_score'] += car_data[feature].apply(
                    lambda x: weight if str(x).lower() == str(user_value).lower() else 0)
    # Ordenar por el puntaje de similitud en orden descendente
    return car_data.sort_values(by='similarity_score', ascending=False)
