import pandas as pd
import numpy as np

# Cargar el dataset original desde un archivo CSV
file_path = 'coches.csv'  # Cambia esto a la ruta de tu archivo CSV
df = pd.read_csv(file_path, sep=';')

""" Esta parte añade un ID único para cada modelo
# Paso 1: Añadir un ID único para cada modelo
df['model_id'] = df.groupby(['make', 'model']).ngroup() + 1  # +1 para empezar desde 1

# Mostrar el DataFrame con model_id
print("DataFrame con model_id:")
print(df[['make', 'model', 'model_id']].drop_duplicates())
"""

# Paso 2: Crear un dataset de valoraciones
num_users = 50  # Puedes ajustar este número según la cantidad de usuarios que quieras simular
min_ratings_per_model = 5  # Mínimo de valoraciones por modelo
total_models = df['model_id'].nunique()  # Número total de modelos únicos
total_ratings = 100  # Número total de valoraciones que deseas crear

# Crear un DataFrame de valoraciones
ratings = []

# Asegurarse de que cada modelo tenga al menos `min_ratings_per_model` valoraciones
for model_id in df['model_id'].unique():
    for _ in range(min_ratings_per_model):
        user_id = np.random.randint(1, num_users + 1)  # Generar user_id aleatorio
        rating = np.random.randint(1, 6)  # Valoraciones de 1 a 5
        ratings.append((user_id, model_id, rating))

# Calcular cuántas valoraciones quedan por generar
remaining_ratings = total_ratings - len(ratings)

# Completar las valoraciones restantes de manera aleatoria
np.random.seed(42)  # Para reproducibilidad
for _ in range(remaining_ratings):
    user_id = np.random.randint(1, num_users + 1)  # Generar user_id aleatorio
    model_id = np.random.choice(df['model_id'].unique())  # Seleccionar un model_id aleatorio
    rating = np.random.randint(1, 6)  # Valoraciones de 1 a 5
    ratings.append((user_id, model_id, rating))

# Crear un DataFrame de valoraciones
ratings_df = pd.DataFrame(ratings, columns=['user_id', 'model_id', 'rating'])

# Mostrar el dataset de valoraciones
print("\nDataset de valoraciones:")
print(ratings_df.head())

# Guardar ambos DataFrames en archivos CSV
df.to_csv('car_models_with_id.csv', index=False)
ratings_df.to_csv('car_ratings.csv', index=False)

print("\nLos archivos han sido guardados como 'car_models_with_id.csv' y 'car_ratings.csv'.")
