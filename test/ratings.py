import pandas as pd
import numpy as np

# Cargar el dataset original desde un archivo CSV
file_path = 'data/coches.csv'  # Cambia esto a la ruta de tu archivo CSV
df = pd.read_csv(file_path)

# Paso 1: Definir segmentos de usuarios con preferencias específicas
num_users = 3000  # Puedes ajustar este número según la cantidad de usuarios que quieras simular

# Definir características de preferencia
preferences = {
    'sporty': {'make': ['PORSCHE', 'BMW', 'AUDI'], 'min_power': 300, 'max_price': 150000},
    'economical': {'make': ['TOYOTA', 'HONDA', 'FORD'], 'max_price': 50000, 'max_kms': 100000},
    'luxury': {'make': ['MERCEDES', 'LAMBORGHINI', 'FERRARI'], 'min_price': 200000, 'min_power': 400},
    'family': {'doors': [4], 'max_price': 80000, 'max_kms': 80000},  # Cambiado 'doors': 4 a 'doors': [4]
    # Puedes agregar más segmentos según las necesidades
}

# Asignar un segmento a cada usuario
user_segments = np.random.choice(list(preferences.keys()), size=num_users, p=[0.25, 0.25, 0.25, 0.25])

# Crear un DataFrame para usuarios
users_df = pd.DataFrame({
    'user_id': range(1, num_users + 1),
    'segment': user_segments
})

# Crear un DataFrame de valoraciones
ratings = []

# Parámetros para valoraciones
min_ratings_per_model = 10  # Mínimo de valoraciones por modelo

for model_id in df['model_id'].unique():
    # Filtrar los coches con este model_id
    cars = df[df['model_id'] == model_id]
    
    for _ in range(min_ratings_per_model):
        user = users_df.sample(n=1).iloc[0]
        prefs = preferences[user['segment']]
        car = cars.sample(n=1).iloc[0]
        
        # Verificar si el coche coincide con las preferencias del usuario
        match = True
        for key, value in prefs.items():
            if key in ['make', 'doors']:
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
            # Añade más condiciones según las preferencias
        
        # Asignar una puntuación basada en la coincidencia
        if match:
            rating = np.random.choice([4, 5], p=[0.2, 0.8])  # Mayor probabilidad de puntuaciones altas
        else:
            rating = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])  # Mayor probabilidad de puntuaciones bajas
        
        ratings.append((str(user['user_id']), str(model_id), rating))

# Convertir la lista de valoraciones a un DataFrame
ratings_df = pd.DataFrame(ratings, columns=['user_id', 'model_id', 'rating'])

# Eliminar posibles duplicados (opcional)
ratings_df = ratings_df.drop_duplicates(subset=['user_id', 'model_id'])

# Guardar el DataFrame de valoraciones en un archivo CSV
ratings_df.to_csv('data/car_ratings.csv', index=False)

print("Dataset de valoraciones generado exitosamente.")
