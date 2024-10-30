import pandas as pd

# Cargar el dataset
df = pd.read_csv('data/coches.csv')

# Añadir la columna 'id' con el número de la fila
df['id'] = df.index

# Guardar el dataset modificado
df.to_csv('data/coches.csv', index=False)