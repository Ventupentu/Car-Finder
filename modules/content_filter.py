import pandas as pd

def calculate_content_similarity(user_input: dict, car_data: pd.DataFrame, feature_weights: dict) -> pd.DataFrame:
    """
    Calcula la similitud entre las características deseadas por el usuario y los coches.
    
    :param user_input: Preferencias del usuario.
    :param car_data: DataFrame con los datos de coches.
    :param feature_weights: Pesos asignados a cada característica.
    :return: DataFrame con puntajes de similitud.
    """
    car_data = car_data.copy()
    car_data['similarity_score'] = 0.0

    for feature, weight in feature_weights.items():
        if feature in user_input:
            if isinstance(user_input[feature], (list, tuple)):
                mask = car_data[feature].between(*user_input[feature])
            else:
                mask = car_data[feature] == user_input[feature]
            car_data.loc[mask, 'similarity_score'] += weight
    
    return car_data.sort_values('similarity_score', ascending=False)
