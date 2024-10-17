# main.py

import pandas as pd
from modules.geo_utils import GeoDistanceCalculator
from modules.data_loader import load_data, assign_model_ids
from modules.recommendation_model import RecommendationModel
from surprise import SVD, Dataset, Reader
from surprise.model_selection import GridSearchCV, train_test_split
import numpy as np

def tune_hyperparameters(df_ratings):
    """
    Ajusta los hiperparámetros del modelo SVD utilizando GridSearchCV.
    
    :param df_ratings: DataFrame con las valoraciones de los usuarios.
    :return: Diccionario con los mejores parámetros encontrados.
    """
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_ratings[['user_id', 'model_id', 'rating']], reader)
    
    param_grid = {
        'n_factors': [50, 100, 150],
        'lr_all': [0.002, 0.005, 0.01],
        'reg_all': [0.02, 0.05, 0.1]
    }
    
    gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3, n_jobs=-1)
    gs.fit(data)
    
    #print(f"Mejor RMSE: {gs.best_score['rmse']}")
    #print(f"Mejores parámetros para RMSE: {gs.best_params['rmse']}")
    
    return gs.best_params['rmse']


def recommend(user_preferences):
    """Función principal para ejecutar el programa de recomendación de coches."""
    # Rutas a los archivos CSV
    coches_path = 'data/coches.csv'
    ratings_path = 'data/car_ratings.csv'
    
    # Cargar los datos
    df_cars, df_ratings = load_data(coches_path, ratings_path)
    
    # Asignar 'model_id'
    df_cars = assign_model_ids(df_cars)
    
    # Asegurarse de que 'model_id' en df_ratings es de tipo string (como lo espera Surprise)
    df_ratings['model_id'] = df_ratings['model_id'].astype(str)
    df_ratings['user_id'] = df_ratings['user_id'].astype(str)
    
    # Ajustar hiperparámetros
    #print("Iniciando ajuste de hiperparámetros...")
    best_params = tune_hyperparameters(df_ratings)
    
    # Inicializar el modelo de recomendación con los mejores parámetros
    recommender = RecommendationModel(df_ratings)
    recommender.model = SVD(**best_params)
    
    # Entrenar el modelo
    recommender.train(test_size=0.2, random_state=42)
    
    # Evaluar el modelo
    #rmse, mae = recommender.evaluate()
    #print(f"Evaluación del Modelo - RMSE: {rmse}, MAE: {mae}")
    
    # Definir preferencias del usuario

    
    # Crear instancia de GeoDistanceCalculator
    geo_calculator = GeoDistanceCalculator()
    
    # Filtrar los coches según las preferencias del usuario
    filtered_cars = df_cars.copy()
    
    # Aplicar filtros basados en preferencias
    for key, value in user_preferences.items():
        if key == 'origin_city' or value is None:
            continue  # Ignorar 'origin_city' y preferencias no especificadas
        filtered_cars['power'] = pd.to_numeric(filtered_cars['power'], errors='coerce')

        if key in ['min_price', 'max_price', 'max_kms', 'power']:
            if key == 'min_price':
                filtered_cars = filtered_cars[filtered_cars['price'] >= value]
            elif key == 'max_price':
                filtered_cars = filtered_cars[filtered_cars['price'] <= value]
            elif key == 'max_kms':
                filtered_cars = filtered_cars[filtered_cars['kms'] <= value]
            elif key == 'power':
                filtered_cars = filtered_cars[filtered_cars['power'] >= value]
                print(type(filtered_cars['power']))
        else:
            filtered_cars = filtered_cars[filtered_cars[key] == value]
    
    # Calcular la distancia desde la ciudad de origen del usuario a la provincia de cada coche
    if user_preferences.get('origin_city'):
        user_origin = user_preferences['origin_city']
        user_coords = geo_calculator.obtener_coordenadas(user_origin, 'España')
        if user_coords is None:
            print(f"No se pudo obtener las coordenadas para la ciudad de origen: {user_origin}")
            filtered_cars = pd.DataFrame()  # Vaciar el DataFrame si no se puede calcular la distancia
        else:
            # Calcular la distancia para cada coche
            distances = filtered_cars['province'].apply(
                lambda prov: geo_calculator.calcular_distancia(user_origin, prov, 'España', 'España')
            )
            # Añadir la columna de distancia
            filtered_cars = filtered_cars.copy()
            filtered_cars['distance_km'] = distances
    
    # Generar recomendaciones
    if not filtered_cars.empty:
        # Obtener IDs de los modelos filtrados
        model_ids = filtered_cars['model_id'].unique()
        
        # Obtener los detalles de los coches filtrados
        filtered_cars_details = df_cars[df_cars['model_id'].isin(model_ids)].to_dict('records')
        
        # Predecir calificaciones para cada modelo filtrado usando el método para usuarios nuevos
        predicted_ratings = []
        for car in filtered_cars_details:
            estimated_rating = recommender.predict_rating_new_user(
                model_id=car['model_id'],
                car_features=car,
                preferences=user_preferences
            )
            predicted_ratings.append({
                'model_id': car['model_id'],
                'estimated_rating': estimated_rating
            })
        
        # Convertir las predicciones a DataFrame
        predicted_ratings_df = pd.DataFrame(predicted_ratings)
        
        # Unir con los detalles de los coches
        recommendations = pd.merge(predicted_ratings_df, filtered_cars, on='model_id')
        
        # Redondear 'estimated_rating' y 'distance_km' a 2 decimales
        recommendations['estimated_rating'] = recommendations['estimated_rating'].round(2)
        if 'distance_km' in recommendations.columns:
            recommendations['distance_km'] = recommendations['distance_km'].round(2)
        
        # Ordenar por calificación estimada y seleccionar las top 5
        top_recommendations = recommendations.sort_values(by='estimated_rating', ascending=False).head(5)
        
        # Mostrar las recomendaciones incluyendo la distancia
        print("\nMejores recomendaciones para el usuario nuevo:")
        top = top_recommendations[['make', 'model', 'price', 'fuel', 'year', 'kms', 'power', 'doors', 'shift', 'color', 'province', 'distance_km', 'estimated_rating']]
        # Convertir a diccionario para mostrar en la interfaz
        return top.to_dict('records')


    else:
        print("No hay coches que cumplan con las preferencias del usuario.")

    

"""
if __name__ == "__main__":
    user_preferences = {
        'make': 'PORSCHE',             # Marca preferida
        'model': '911',                # Modelo preferido
        'min_price': 50000,            # Precio mínimo
        'max_price': 400000,           # Precio máximo
        'fuel': 'Gasolina',            # Tipo de combustible
        'year': 2020,              # Año máximo
        'max_kms': 50000,              # Kilometraje máximo
        'power': 500,                  # Potencia mínima
        'doors': 2,                    # Número de puertas
        'shift': 'Automatico',         # Tipo de cambio
        'color': 'Negro',              # Color
        'origin_city': 'Madrid'        # Ciudad de origen del usuario
        # 'max_distance': 100    # Eliminado como preferencia de filtrado
    }

"""