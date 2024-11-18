from surprise import BaselineOnly, SVDpp, Dataset, Reader
from surprise.model_selection import train_test_split
import pandas as pd

# Cargar datos
ratings_path = "data/car_ratings.csv"  # Cambia la ruta según corresponda
df_ratings = pd.read_csv(ratings_path)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df_ratings[['user_id', 'model_id', 'rating']], reader)

# Dividir datos en entrenamiento y prueba
trainset, testset = train_test_split(data, test_size=0.2)

# Entrenar modelos individuales
print("Entrenando BaselineOnly...")
model_baseline = BaselineOnly()
model_baseline.fit(trainset)

print("Entrenando SVD++...")
model_svdpp = SVDpp()
model_svdpp.fit(trainset)

# Generar predicciones híbridas
def hybrid_prediction(testset, model1, model2, weight1=0.7, weight2=0.3):
    """
    Combina las predicciones de dos modelos según los pesos especificados.
    
    :param testset: Conjunto de datos de prueba.
    :param model1: Primer modelo.
    :param model2: Segundo modelo.
    :param weight1: Peso del primer modelo.
    :param weight2: Peso del segundo modelo.
    :return: DataFrame con predicciones híbridas.
    """
    hybrid_results = []
    for user, item, actual_rating in testset:
        # Predicciones individuales
        pred1 = model1.predict(user, item).est
        pred2 = model2.predict(user, item).est
        
        # Predicción híbrida (ponderada)
        hybrid_rating = (weight1 * pred1 + weight2 * pred2) / (weight1 + weight2)
        hybrid_results.append((user, item, actual_rating, hybrid_rating))
    
    return pd.DataFrame(hybrid_results, columns=["user_id", "model_id", "actual_rating", "hybrid_rating"])

# Evaluar predicciones híbridas
print("Generando predicciones híbridas...")
results = hybrid_prediction(testset, model_baseline, model_svdpp)

# Calcular métricas
def calculate_hybrid_metrics(results):
    """
    Calcula RMSE y MAE para las predicciones híbridas.
    
    :param results: DataFrame con columnas actual_rating e hybrid_rating.
    :return: Métricas RMSE y MAE.
    """
    mse = ((results["actual_rating"] - results["hybrid_rating"]) ** 2).mean()
    mae = (results["actual_rating"] - results["hybrid_rating"]).abs().mean()
    rmse = mse ** 0.5
    return rmse, mae

rmse, mae = calculate_hybrid_metrics(results)

# Mostrar resultados
print(f"Híbrido - RMSE: {rmse:.4f}, MAE: {mae:.4f}")
