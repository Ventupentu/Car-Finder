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
        if feature in user_input:
            user_value = user_input[feature]
            
            if feature in ['price', 'year', 'kms', 'power']:  # Características numéricas
                max_val = car_data[feature].max()
                min_val = car_data[feature].min()
                
                # Normalización y cálculo de similitud inversa para price y kms
                if feature in ['price', 'kms']:
                    normalized_diff = 1 - (np.abs(car_data[feature] - user_value) / (max_val - min_val))
                else:  # Normalización directa para year y power
                    normalized_diff = (car_data[feature] - min_val) / (max_val - min_val)
                
                car_data['similarity_score'] += normalized_diff * weight
            
            elif feature in ['fuel', 'shift', 'color', 'province', 'make', 'model','doors']:  # Características categóricas
                car_data['similarity_score'] += car_data[feature].apply(
                    lambda x: weight if x == user_value else 0)
    
    # Ordenar por el puntaje de similitud en orden descendente
    return car_data.sort_values(by='similarity_score', ascending=False)
