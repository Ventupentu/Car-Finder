import pandas as pd
import numpy as np

# Cargar el dataset original desde un archivo CSV
file_path = 'data/coches.csv'  # Cambia esto a la ruta de tu archivo CSV
df = pd.read_csv(file_path)

# Paso 1: Crear un dataset de valoraciones
num_users = 3000  # Puedes ajustar este número según la cantidad de usuarios que quieras simular
min_ratings_per_model = 10  # Mínimo de valoraciones por modelo

# Crear un DataFrame de valoraciones
ratings = []

# Asegurarse de que cada modelo tenga al menos `min_ratings_per_model` valoraciones
for model_id in df['model_id'].unique():
    for _ in range(min_ratings_per_model):
        user_id = np.random.randint(1, num_users + 1)  # Generar user_id aleatorio
        rating = np.random.randint(1, 6)  # Valoraciones de 1 a 5
        ratings.append((user_id, model_id, rating))

# Convertir la lista de valoraciones a un DataFrame
ratings_df = pd.DataFrame(ratings, columns=['user_id', 'model_id', 'rating'])

# Guardar el DataFrame de valoraciones en un archivo CSV
ratings_df.to_csv('data/car_ratings.csv', index=False)