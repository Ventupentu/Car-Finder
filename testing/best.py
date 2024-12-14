import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import cross_validate
from surprise import SVD, SVDpp, NMF, KNNBasic, KNNWithMeans, KNNBaseline, BaselineOnly, CoClustering
import time

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
    a = time.time()
    print(f"Entrenando y evaluando {name}...")
    cv_results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=False, n_jobs=-1)
    results[name] = {
        "RMSE": round(cv_results['test_rmse'].mean(), 4),
        "MAE": round(cv_results['test_mae'].mean(), 4),
        "Tiempo": round(time.time() - a, 2)
    }


# Mostrar resultados
print("\nResultados finales:")
for name, metrics in sorted(results.items(), key=lambda x: x[1]['RMSE']):
    print(f"{name}: RMSE={metrics['RMSE']}, MAE={metrics['MAE']}, Tiempo={metrics['Tiempo']}s")



"""
Algoritmo         RMSE     MAE     Tiempo (s)
----------------------------------------------
BaselineOnly     0.5169   0.4954   10.63
SVD++            0.5198   0.4950   61.18
SVD              0.5215   0.4950   13.83
KNNBasic         0.5219   0.4954   355.75
NMF              0.5220   0.4946   15.04
KNNBaseline      0.5222   0.4968   365.86
CoClustering     0.5227   0.4951   17.76
KNNWithMeans     0.5233   0.4971   359.92
"""
