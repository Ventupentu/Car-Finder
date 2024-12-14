import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('data/coches.csv', encoding='utf-8')

# Analizar la columna cada columna en busca de valores nulos
for col in df.columns:
    num_nulls = df[col].isnull().sum()
    print(f"Columna '{col}' tiene {num_nulls} valores nulos")