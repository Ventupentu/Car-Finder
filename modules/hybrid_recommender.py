from .collaborative_filter import CollaborativeFilter
from .content_filter import ContentFilter
from .geo_utils import GeoUtils

class HybridRecommender:
    """
    HybridRecommender es una clase que implementa un sistema de recomendación híbrido
    que combina filtrado colaborativo, filtrado basado en contenido y penalización geográfica.

    Atributos:
        collaborative_model (CollaborativeFilter): El modelo de filtrado colaborativo utilizado.
        geo_calculator (GeoUtils): La instancia de GeoUtils utilizada para cálculos geográficos 
    """
    def __init__(self, collaborative_model: CollaborativeFilter, geo_calculator: GeoUtils):
        """
        Inicializa una instancia de la clase HybridRecommender.

        Args:
            collaborative_model (CollaborativeFilter): El modelo de filtrado colaborativo a utilizar.
            geo_calculator (GeoUtils): La instancia de GeoUtils a utilizar para cálculos geográficos.
        """
        self.collaborative_model = collaborative_model
        self.geo_calculator = geo_calculator

    def recommend(self, user_id, user_input, feature_weights, user_location, cars_df):
        """
        Recomienda coches al usuario basándose en sus preferencias, ubicación y valoraciones previas.
        
        Args:
            user_id (int): Identificador del usuario para el que se generan las recomendaciones.
            user_input (dict): Diccionario con las características y valores proporcionados por el usuario.
            feature_weights (dict): Diccionario con los pesos asignados a cada característica.
            user_location (str): Ubicación del usuario en formato de texto.
            cars_df (pd.DataFrame): DataFrame que contiene los datos de los coches.

        Returns:
            pd.DataFrame: DataFrame con los datos de los coches recomendados y sus puntuaciones de similitud.
        """
        # Calcula la similitud de contenido entre las preferencias del usuario y los coches
        content_scores = ContentFilter.calculate_content_similarity(user_input, cars_df, feature_weights)
        
        # Aplica una penalización geográfica a las puntuaciones de similitud de contenido
        geo_scores = self.geo_calculator.apply_penalty(content_scores, user_location, feature_weights.get('distance', 0))
        
        # Calcula la puntuación colaborativa para cada coche
        geo_scores['collaborative_score'] = geo_scores['model_id'].apply(lambda x: self.collaborative_model.predict_rating(user_id, x))
        
        # Calcula la puntuación híbrida combinando las puntuaciones de similitud, colaborativas y geográficas
        geo_scores['hybrid_score'] = (
            geo_scores['similarity_score'] * 0.4 +
            geo_scores['collaborative_score'] * 0.3 +
            geo_scores['geo_score'] * 0.3
        )

        # Ordena los coches por la puntuación híbrida en orden descendente y devuelve el DataFrame resultante
        return geo_scores.sort_values('hybrid_score', ascending=False)
