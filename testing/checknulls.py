import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('data/coches.csv', encoding='utf-8')

# Analizar la columna "kms" y revisar si hay valores vacíos
empty_kms = df['power'].isnull()

# Mostrar las filas donde la columna "kms" está vacía
empty_rows = df[empty_kms]

print("Filas con valores vacíos en la columna 'kms':")
print(empty_rows)
