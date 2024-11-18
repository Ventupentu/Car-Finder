import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import cross_validate
from surprise import SVD, SVDpp, NMF, KNNBasic, KNNWithMeans, KNNBaseline, BaselineOnly, CoClustering

# Cargar el dataset
ratings_path = 'data/car_ratings.csv'  # Cambia esta ruta si es necesario
df_ratings = pd.read_csv(ratings_path)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df_ratings[['user_id', 'model_id', 'rating']], reader)

# Lista de algoritmos a probar
algorithms = {
    "SVD": SVD(),
    "SVD++": SVDpp(),
    "NMF": NMF(),
    "KNNBasic": KNNBasic(),
    "KNNWithMeans": KNNWithMeans(),
    "KNNBaseline": KNNBaseline(),
    "BaselineOnly": BaselineOnly(),
    "CoClustering": CoClustering()
}

# Evaluar cada algoritmo
results = {}
for name, algo in algorithms.items():
    print(f"Entrenando y evaluando {name}...")
    cv_results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=False)
    results[name] = {
        "RMSE": round(cv_results['test_rmse'].mean(), 4),
        "MAE": round(cv_results['test_mae'].mean(), 4)
    }

# Mostrar resultados
print("\nResultados finales:")
for name, metrics in sorted(results.items(), key=lambda x: x[1]['RMSE']):
    print(f"{name}: RMSE={metrics['RMSE']}, MAE={metrics['MAE']}")



"""
Resultados finales:
BaselineOnly: RMSE=0.5169, MAE=0.4954
SVD++: RMSE=0.5198, MAE=0.495
SVD: RMSE=0.5215, MAE=0.495
KNNBasic: RMSE=0.5219, MAE=0.4954
NMF: RMSE=0.522, MAE=0.4946
KNNBaseline: RMSE=0.5222, MAE=0.4968
CoClustering: RMSE=0.5227, MAE=0.4951
KNNWithMeans: RMSE=0.5233, MAE=0.4971
"""
