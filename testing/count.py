import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('data/coches.csv')

makes = df['make'].unique()

fuels = df['fuel'].unique()

shifts = df['shift'].unique()

print(f"Marcas: {makes}")
print(f"Combustibles: {fuels}")
print(f"Cambios: {shifts}")

