# modules/recommendation_model.py

import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

class RecommendationModel:
    def __init__(self, df_ratings: pd.DataFrame, rating_scale: tuple = (1, 5)):
        """
        Inicializa el modelo de recomendación.
        
        :param df_ratings: DataFrame de valoraciones.
        :param rating_scale: Tupla que define el rango de las valoraciones.
        """
        self.df_ratings = df_ratings
        self.reader = Reader(rating_scale=rating_scale)
        self.model = SVD()
        self.trainset = None
        self.testset = None
        self.rmse = None
        self.mae = None

    def train(self, test_size: float = 0.2, random_state: int = 42):
        """
        Entrena el modelo de recomendación.
        
        :param test_size: Proporción del dataset para prueba.
        :param random_state: Semilla para reproducibilidad.
        """
        data = Dataset.load_from_df(self.df_ratings[['user_id', 'model_id', 'rating']], self.reader)
        self.trainset, self.testset = train_test_split(data, test_size=test_size, random_state=random_state)
        self.model.fit(self.trainset)
        print("Modelo de recomendación entrenado.")

    def evaluate(self) -> tuple:
        """
        Evalúa el modelo de recomendación.
        
        :return: Tuple (rmse, mae)
        """
        if self.testset is None:
            raise ValueError("El modelo no ha sido entrenado aún.")
        
        predictions = self.model.test(self.testset)
        self.rmse = accuracy.rmse(predictions)
        self.mae = accuracy.mae(predictions)
        return self.rmse, self.mae

    def predict_rating(self, user_id: str, model_id: int) -> float:
        """
        Predice la calificación estimada para un usuario y modelo de coche.
        
        :param user_id: ID del usuario.
        :param model_id: ID del modelo de coche.
        :return: Calificación estimada.
        """
        pred = self.model.predict(uid=user_id, iid=model_id)
        return pred.est
