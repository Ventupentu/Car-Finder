import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('data/coches.csv')

# Reemplazar Gas natural (CNG) por Gas natural
df['fuel'] = df['fuel'].replace('Gas natural (CNG)', 'Gas natural')

# Reemplazar Gas licuado (GLP) por Gas licuado
df['fuel'] = df['fuel'].replace('Gas licuado (GLP)', 'Gas licuado')


# Guardar el DataFrame actualizado en un nuevo archivo CSV
df.to_csv('data/coches.csv', index=False)