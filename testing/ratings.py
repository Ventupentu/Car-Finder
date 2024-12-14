import pandas as pd
import numpy as np

# Cargar el dataset original desde un archivo CSV
file_path = 'data/coches.csv'
df = pd.read_csv(file_path)

num_users = 15000

# Definir segmentos
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
min_ratings_per_user = 120  # Incrementado para asegurar más valoraciones
min_ratings_per_model = 100  # Incrementado para garantizar más valoraciones por modelo

# Inicializar un contador de valoraciones por modelo
model_ratings_count = {model_id: 0 for model_id in df['model_id'].unique()}

# Asegurar un mínimo de valoraciones por usuario
for user_id in range(1, num_users + 1):
    user = users_df.loc[users_df['user_id'] == user_id]
    prefs = preferences[user['segment'].iloc[0]]

    # Asegurarse de que el usuario valore un número adecuado de modelos
    cars_to_rate = df.sample(min_ratings_per_user, replace=True)

    for _, car in cars_to_rate.iterrows():
        model_id = car['model_id']

        # Verificar si el coche coincide con las preferencias del usuario
        match = True
        for key, value in prefs.items():
            if key in ['make', 'fuel', 'year', 'doors', 'shift', 'color', 'province']:
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
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.3, 0.3, 0.1])  # Mejora en la distribución
        else:
            rating = np.random.choice([2, 3], p=[0.4, 0.6])

        ratings.append((str(user_id), str(model_id), rating))
        model_ratings_count[model_id] += 1

# Asegurarse de que cada usuario tenga al menos 100 valoraciones
ratings_per_user = pd.DataFrame(ratings, columns=['user_id', 'model_id', 'rating'])['user_id'].value_counts()
for user_id, count in ratings_per_user.items():
    if count < 100:
        additional_ratings_needed = 100 - count
        cars_to_rate = df.sample(additional_ratings_needed, replace=True)
        for _, car in cars_to_rate.iterrows():
            model_id = car['model_id']
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.3, 0.3, 0.1])
            ratings.append((str(user_id), str(model_id), rating))

# Asegurarse de que cada modelo tenga al menos min_ratings_per_model valoraciones
for model_id, count in model_ratings_count.items():
    if count < min_ratings_per_model:
        additional_ratings_needed = min_ratings_per_model - count
        additional_users = np.random.choice(users_df['user_id'], size=additional_ratings_needed, replace=True)
        for user_id in additional_users:
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.3, 0.3, 0.1])
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

# Modelo con más valoraciones
model_with_most_ratings = ratings_per_model.idxmax()
most_ratings_count = ratings_per_model.max()
print(f"Modelo con más valoraciones: {model_with_most_ratings} ({most_ratings_count} valoraciones)")