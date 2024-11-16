import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('data/coches.csv')

# Group by 'model_id' and count the occurrences
model_counts = df['model_id'].value_counts()

# Get the top 5 most frequent cars by 'model_id'
top5_models = model_counts.head(10)

print(top5_models)