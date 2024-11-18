import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('data/coches.csv')

# Group by 'model_id' and count the occurrences
model_counts = df['province'].unique()

print(model_counts)