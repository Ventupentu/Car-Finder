# modules/recommendation_model.py

import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import numpy as np

class RecommendationModel:
    def __init__(self, df_ratings: pd.DataFrame, rating_scale: tuple = (1, 5)):
        self.df_ratings = df_ratings
        self.reader = Reader(rating_scale=rating_scale)
        self.model = SVD()
        self.trainset = None
        self.testset = None
        self.rmse = None
        self.mae = None

    def train(self, test_size: float = 0.2, random_state: int = 0):
        data = Dataset.load_from_df(self.df_ratings[['user_id', 'model_id', 'rating']], self.reader)
        self.trainset, self.testset = train_test_split(data, test_size=test_size, random_state=random_state)
        self.model.fit(self.trainset)
        print("Modelo de recomendación entrenado.")

    def evaluate(self) -> tuple:
        if self.testset is None:
            raise ValueError("El modelo no ha sido entrenado aún.")
        
        predictions = self.model.test(self.testset)
        self.rmse = accuracy.rmse(predictions)
        self.mae = accuracy.mae(predictions)
        return self.rmse, self.mae

    def predict_rating(self, user_id: str, model_id: int) -> float:
        pred = self.model.predict(uid=user_id, iid=model_id)
        return pred.est

    def predict_rating_new_user(self, model_id: int, car_features: dict, preferences: dict, weights: dict) -> float:
        # Obtener la media de las valoraciones para el modelo
        model_ratings = self.df_ratings[self.df_ratings['model_id'] == model_id]['rating']
        mean_rating = model_ratings.mean() if not model_ratings.empty else self.trainset.global_mean

        # Normalizar los pesos
        total_weight = sum(weights.values())
        normalized_weights = {key: value / total_weight if total_weight > 0 else 0 for key, value in weights.items()}

        # Ajustar la puntuación basada en la coincidencia de características
        adjustment = 0

        for key, value in preferences.items():
            if value is None:
                continue
            if key in ['min_price', 'max_price', 'min_power', 'max_kms']:
                # Comparar con rangos
                if key == 'min_price' and car_features.get('price', 0) >= value:
                    adjustment += normalized_weights.get('min_price', 0) * 0.5
                elif key == 'max_price' and car_features.get('price', 0) <= value:
                    adjustment += normalized_weights.get('max_price', 0) * 0.5
                elif key == 'min_power' and car_features.get('power', 0) >= value:
                    adjustment += normalized_weights.get('min_power', 0) * 0.5
                elif key == 'max_kms' and car_features.get('kms', 0) <= value:
                    adjustment += normalized_weights.get('max_kms', 0) * 0.5
            else:
                # Comparar con igualdad
                if car_features.get(key) == value:
                    adjustment += normalized_weights.get(key, 0) * 0.5

        # Penalizar según la distancia
        if 'distance' in normalized_weights and 'distance_km' in car_features:
            adjustment -= normalized_weights['distance'] * (car_features['distance_km'] / 100)

        # Asegurarse de que el ajuste no cause que la calificación sea menor que 1 o mayor que 5
        final_rating = min(max(mean_rating + adjustment, 1), 5)

        return final_rating






