import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Cargar el dataset
data = pd.read_csv('data/coches.csv')

# Imputar valores faltantes en la columna de potencia (power)
# Primero, asegurémonos de que la columna 'power' sea de tipo numérico
data['power'] = pd.to_numeric(data['power'], errors='coerce')

# Codificar las columnas categóricas usando get_dummies
data_encoded = pd.get_dummies(data, columns=['fuel', 'shift', 'province'])

# Separar las filas con valores conocidos y faltantes en 'power'
known_power = data_encoded[data_encoded['power'].notna()]
unknown_power = data_encoded[data_encoded['power'].isna()]

# Definir las características (X) y la variable objetivo (y)
# Seleccionar las columnas que se usarán para predecir la potencia
features = [col for col in data_encoded.columns if col.startswith(('kms', 'year', 'doors', 'fuel_', 'shift_', 'province_'))]

# Dividir los datos conocidos en conjuntos de entrenamiento y prueba
X = known_power[features]
y = known_power['power']

# Entrenar un modelo de regresión
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predecir los valores faltantes en la columna 'power'
X_unknown = unknown_power[features]
predicted_power = model.predict(X_unknown)

# Aplicar ceiling para redondear hacia arriba y convertir a enteros
unknown_power['power'] = np.ceil(predicted_power).astype(int)

# Rellenar el dataset original con las predicciones
data.loc[data['power'].isna(), 'power'] = unknown_power['power']

# Opcional: Guardar el dataset con los valores imputados
data.to_csv('dataset_imputado.csv', index=False)
