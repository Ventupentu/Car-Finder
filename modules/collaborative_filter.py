import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pickle
import os

class CollaborativeFilter:
    """
    CollaborativeFilter es una clase que implementa un modelo de filtrado colaborativo
    para predecir las calificaciones de los usuarios.

    Atributos:
        model_path (str): Ruta al archivo del modelo guardado.
        model (SVD): El modelo de filtrado colaborativo.
        testset (Dataset): El conjunto de datos de prueba utilizado para la evaluación.
    """
    def __init__(self, model_path='data/collaborative_model.pkl'):
        """
        Inicializa una instancia de la clase CollaborativeFilter.

        Args:
            model_path (str): Ruta al archivo del modelo colaborativo. 
                              Por defecto es 'data/collaborative_model.pkl'.
        """
        self.model_path = model_path
        self.model = None
        self.testset = None

    def train_model(self, ratings_path: str) -> None:
        """
        Entrena un modelo de filtrado colaborativo utilizando los datos de calificaciones proporcionados.
        Si un modelo entrenado ya existe en la ruta especificada, lo carga en lugar de entrenar uno nuevo.

        Args:
            ratings_path (str): La ruta al archivo CSV que contiene las calificaciones de los usuarios.

        El archivo CSV debe tener las siguientes columnas:
        - user_id: Identificador del usuario.
        - model_id: Identificador del modelo del coche.
        - rating: Calificación dada por un usuario al ítem.
        El modelo entrenado se guarda en la ruta especificada por self.model_path.
        """
        if os.path.exists(self.model_path):
            print("Cargando modelo colaborativo guardado...")
            with open(self.model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)
            return

        print("Entrenando un nuevo modelo colaborativo...")
        df_ratings = pd.read_csv(ratings_path)
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df_ratings[['user_id', 'model_id', 'rating']], reader)

        trainset, self.testset = train_test_split(data, test_size=0.2)

        best_params = {'n_factors': 20, 'n_epochs': 10, 'lr_all': 0.002, 'reg_all': 0.4} # Estos parámetros han sido encontrados mediante GridSearchCV
        self.model = SVD(
            n_factors=best_params['n_factors'],
            n_epochs=best_params['n_epochs'],
            lr_all=best_params['lr_all'],
            reg_all=best_params['reg_all']
        )
        self.model.fit(trainset)

        with open(self.model_path, 'wb') as model_file:
            pickle.dump(self.model, model_file)

    def predict_rating(self, user_id: str, model_id: int) -> float:
        """
        Predice la calificación de un usuario para un modelo específico.

        Args:
            user_id (str): El ID del usuario para el cual se desea predecir la calificación.
            model_id (int): El ID del modelo para el cual se desea predecir la calificación.

        Returns:
            float: La calificación predicha para el usuario y el modelo especificados.

        Raises:
            ValueError: Si el modelo no está entrenado.
        """
        if self.model is None:
            raise ValueError("El modelo no está entrenado.")
        prediction = self.model.predict(user_id, model_id)
        return prediction.est
