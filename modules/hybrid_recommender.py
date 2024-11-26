from .collaborative_filter import CollaborativeFilter
from .content_filter import ContentFilter
from .geo_utils import GeoUtils

class HybridRecommender:
    def __init__(self, collaborative_model: CollaborativeFilter, geo_calculator: GeoUtils):
        self.collaborative_model = collaborative_model
        self.geo_calculator = geo_calculator

    def recommend(self, user_id, user_input, feature_weights, user_location, cars_df):
        content_scores = ContentFilter.calculate_content_similarity(user_input, cars_df, feature_weights)
        geo_scores = self.geo_calculator.apply_penalty(content_scores, user_location, feature_weights.get('distance', 0))
        geo_scores['collaborative_score'] = geo_scores['model_id'].apply(lambda x: self.collaborative_model.predict_rating(user_id, x))
        
        geo_scores['hybrid_score'] = (
            geo_scores['similarity_score'] * 0.4 +
            geo_scores['collaborative_score'] * 0.4 +
            geo_scores['geo_score'] * 0.2
        )

        return geo_scores.sort_values('hybrid_score', ascending=False)
