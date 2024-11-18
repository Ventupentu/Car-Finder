import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pickle
import os

MODEL_PATH = 'data/collaborative_model.pkl'

def train_collaborative_model(ratings_path: str) -> tuple:
    """
    Entrena un modelo de filtrado colaborativo con Surprise o carga uno guardado.
    
    :param ratings_path: Ruta al dataset de valoraciones.
    :return: Tuple (modelo entrenado, datos de prueba)
    """
    if os.path.exists(MODEL_PATH):
        print("Cargando modelo colaborativo guardado...")
        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file)
        return model, None  # No se devuelve testset ya que no se puede dividir al cargar

    print("Entrenando un nuevo modelo colaborativo...")
    # Cargar datos
    df_ratings = pd.read_csv(ratings_path)
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_ratings[['user_id', 'model_id', 'rating']], reader)
    
    # Dividir en datos de entrenamiento y prueba
    trainset, testset = train_test_split(data, test_size=0.2)
    
    # Mejores hiperparámetros obtenidos
    best_params = {'n_factors': 20, 'n_epochs': 10, 'lr_all': 0.002, 'reg_all': 0.4}

    # Crear el modelo SVD con los mejores parámetros
    model = SVD(
        n_factors=best_params['n_factors'],
        n_epochs=best_params['n_epochs'],
        lr_all=best_params['lr_all'],
        reg_all=best_params['reg_all']
    )
    model.fit(trainset)

    # Guardar el modelo en un archivo
    with open(MODEL_PATH, 'wb') as model_file:
        pickle.dump(model, model_file)

    return model, testset


def predict_rating(user_id: str, model_id: int, model) -> float:
    """
    Predice la valoración de un usuario para un modelo de coche.
    
    :param user_id: ID del usuario.
    :param model_id: ID del modelo de coche.
    :param model: Modelo entrenado de Surprise.
    :return: Valoración predicha.
    """
    prediction = model.predict(user_id, model_id)
    return prediction.est
