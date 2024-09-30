# main.py

import pandas as pd
from modules.geo_utils import GeoDistanceCalculator
from modules.data_loader import load_data, assign_model_ids
from modules.recommendation_model import RecommendationModel

def main():
    # Rutas a los archivos CSV
    coches_path = 'data/coches.csv'
    ratings_path = 'data/car_ratings.csv'
    
    # Cargar los datos
    df_cars, df_ratings = load_data(coches_path, ratings_path)
    
    # Asignar 'model_id'
    df_cars = assign_model_ids(df_cars)
    
    # Inicializar y entrenar el modelo de recomendación
    recommender = RecommendationModel(df_ratings)
    recommender.train(test_size=0.2, random_state=42)
    rmse, mae = recommender.evaluate()
    
    # Definir preferencias del usuario (puede dejar cualquiera como None)
    user_preferences = {
        'make': 'PORSCHE',             # e.g., 'ABARTH'
        'model': '911',                 # e.g., '500'
        'min_price': 50000,            # e.g., 20000
        'max_price': 400000,          # e.g., 30000
        'fuel': None,                  # e.g., 'Gasolina'
        'max_year': None,              # e.g., 2021
        'max_kms': None,               # e.g., 10000
        'power': 500,                   # e.g., 180
        'doors': None,                 # e.g., 3
        'shift': None,                 # e.g., 'Manual'
        'color': None,                 # e.g., 'Negro'
        'origin_city': 'Madrid'      # Ciudad de origen del usuario
        # 'max_distance': 100    # Eliminado como preferencia de filtrado
    }
    
    # Crear instancia de GeoDistanceCalculator
    geo_calculator = GeoDistanceCalculator()
    
    # Filtrar los coches según las preferencias del usuario
    filtered_cars = df_cars.copy()
    
    # Aplicar filtros basados en preferencias
    for key, value in user_preferences.items():
        if key == 'origin_city' or value is None:
            continue  # Ignorar 'origin_city' y preferencias no especificadas
        if key in ['min_price', 'max_price', 'max_kms', 'power']:
            if key == 'min_price':
                filtered_cars = filtered_cars[filtered_cars['price'] >= value]
            elif key == 'max_price':
                filtered_cars = filtered_cars[filtered_cars['price'] <= value]
            elif key == 'max_kms':
                filtered_cars = filtered_cars[filtered_cars['kms'] <= value]
            elif key == 'power':
                filtered_cars = filtered_cars[filtered_cars['power'] >= value]
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
        
        # Predecir calificaciones para cada modelo filtrado
        predicted_ratings = pd.DataFrame({
            'model_id': model_ids,
            'estimated_rating': [recommender.predict_rating('new_user', model_id) for model_id in model_ids]
        })
        
        # Unir con los detalles de los coches
        recommendations = pd.merge(predicted_ratings, filtered_cars, on='model_id')
        
        # Redondear 'estimated_rating' y 'distance_km' a 2 decimales
        recommendations['estimated_rating'] = recommendations['estimated_rating'].round(2)
        if 'distance_km' in recommendations.columns:
            recommendations['distance_km'] = recommendations['distance_km'].round(2)
        
        # Ordenar por calificación estimada y seleccionar las top 5
        top_recommendations = recommendations.sort_values(by='estimated_rating', ascending=False).head(5)
        
        # Mostrar las recomendaciones incluyendo la distancia
        print("\nMejores recomendaciones para el usuario nuevo:")
        print(top_recommendations[['make', 'model', 'price', 'fuel', 'year', 'kms', 'power', 'doors', 'shift', 'color', 'province', 'distance_km', 'estimated_rating']])
    else:
        print("No hay coches que cumplan con las preferencias del usuario.")

if __name__ == "__main__":
    main()
