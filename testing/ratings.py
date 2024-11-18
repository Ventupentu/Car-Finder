import pandas as pd
import numpy as np

# Cargar el dataset original desde un archivo CSV
file_path = 'data/coches.csv'
df = pd.read_csv(file_path)

# Paso 1: Definir segmentos de usuarios con preferencias específicas
num_users = 15000

# Definir características de preferencia
preferences = {
    'sporty': {'make': ['PORSCHE', 'BMW', 'AUDI'], 'min_power': 300, 'max_price': 150000},
    'economical': {'make': ['TOYOTA', 'HONDA', 'FORD'], 'max_price': 50000, 'max_kms': 100000},
    'luxury': {'make': ['MERCEDES-BENZ', 'LAMBORGHINI', 'FERRARI'], 'min_price': 200000, 'min_power': 400},
    'family': {'doors': [4, 5], 'max_price': 80000, 'max_kms': 80000},
    'adventurous': {'make': ['JEEP', 'LAND-ROVER', 'TOYOTA'], 'min_power': 150, 'max_kms': 150000},
    'eco_friendly': {'make': ['TESLA', 'TOYOTA', 'NISSAN'], 'fuel': ['electric', 'hybrid'], 'max_price': 60000},
    'classics': {'make': ['JAGUAR', 'BENTLEY', 'ASTON MARTIN'], 'min_price': 50000, 'max_kms': 200000},
    'youth': {'make': ['MINI', 'FIAT', 'SEAT'], 'max_price': 30000, 'max_kms': 100000},
}

# Asignar un segmento a cada usuario con probabilidades ajustadas
segment_probs = [0.15, 0.15, 0.1, 0.1, 0.2, 0.2, 0.05, 0.05]  # Probabilidades ajustadas
user_segments = np.random.choice(list(preferences.keys()), size=num_users, p=segment_probs)

# Crear un DataFrame para usuarios
users_df = pd.DataFrame({
    'user_id': range(1, num_users + 1),
    'segment': user_segments
})

# Crear un DataFrame de valoraciones
ratings = []

# Parámetros para valoraciones
min_ratings_per_user = 100  # Aseguramos que cada usuario valore al menos 100 modelos
min_ratings_per_model = 50  # Mínimo de valoraciones por modelo
max_ratings_per_model = 20000  # Máximo de valoraciones por modelo

# Paso 2: Asignar valoraciones de manera equilibrada

# Para mejorar la densidad, vamos a asignar una cantidad mínima de valoraciones por modelo y por usuario
for user_id in range(1, num_users + 1):
    user = users_df.loc[users_df['user_id'] == user_id]
    prefs = preferences[user['segment'].iloc[0]]

    # Asegurarse de que el usuario valore un número adecuado de modelos (min_ratings_per_user)
    # Seleccionar un subconjunto de modelos aleatorios para el usuario
    cars_to_rate = df.sample(n=min_ratings_per_user, replace=False)

    for _, car in cars_to_rate.iterrows():
        model_id = car['model_id']

        # Verificar si el coche coincide con las preferencias del usuario
        match = True
        for key, value in prefs.items():
            if key in ['make', 'doors', 'fuel']:
                if car[key] not in value:
                    match = False
                    break
            elif key == 'min_price':
                if car['price'] < value:
                    match = False
                    break
            elif key == 'max_price':
                if car['price'] > value:
                    match = False
                    break
            elif key == 'min_power':
                if car['power'] < value:
                    match = False
                    break
            elif key == 'max_kms':
                if car['kms'] > value:
                    match = False
                    break
        
        if match:
            rating = np.random.choice([2, 3, 4], p=[0.4, 0.4, 0.2])  # Ajuste de probabilidades para que las valoraciones intermedias sean más frecuentes
        else:
            rating = np.random.choice([2, 3], p=[0.6, 0.4])  # Aumentar la probabilidad de obtener valoraciones intermedias


        ratings.append((str(user_id), str(model_id), rating))

# Convertir la lista de valoraciones a un DataFrame
ratings_df = pd.DataFrame(ratings, columns=['user_id', 'model_id', 'rating'])

# Eliminar posibles duplicados (opcional)
ratings_df = ratings_df.drop_duplicates(subset=['user_id', 'model_id']).reset_index(drop=True)

# Guardar el DataFrame de valoraciones en un archivo CSV
ratings_df.to_csv('data/car_ratings.csv', index=False)

print("Dataset de valoraciones generado exitosamente.")

# Revisar estadísticas generales
num_users = len(users_df['user_id'].unique())
num_models = len(df['model_id'].unique())
total_possible_interactions = num_users * num_models
actual_interactions = len(ratings_df)

# Densidad del dataset
density = actual_interactions / total_possible_interactions
print(f"Densidad del dataset: {density:.2%}")

ratings_per_model = ratings_df['model_id'].value_counts()
print("Valoraciones mínimas por modelo:", ratings_per_model.min())
print("Valoraciones máximas por modelo:", ratings_per_model.max())

# Distribución de valoraciones por usuario
ratings_per_user = ratings_df['user_id'].value_counts()
print("Valoraciones mínimas por usuario:", ratings_per_user.min())
print("Valoraciones máximas por usuario:", ratings_per_user.max())

# Distribución de las valoraciones (1-5)
rating_dist = ratings_df['rating'].value_counts()
print("Distribución de valoraciones:")
print(rating_dist)

# Ver los usuarios con valoraciones extremas (1 o 5)
extreme_ratings = ratings_df[ratings_df['rating'].isin([1, 5])]
print(f"Número de valoraciones extremas (1 o 5): {len(extreme_ratings)}")
print("Ejemplos de valoraciones extremas:")
print(extreme_ratings.head())

# Revisar modelos populares
popular_models = ratings_df['model_id'].value_counts().head(10)
print("Modelos más valorados:")
print(popular_models)
