from .collaborative_filter import predict_rating
from .content_filter import calculate_content_similarity
from .geo_utils import apply_geographic_penalty

def hybrid_recommendation(user_id, user_input, feature_weights, user_location, geo_calculator, collaborative_model, cars_df):
    # Filtrado basado en contenido
    content_scores = calculate_content_similarity(user_input, cars_df, feature_weights)

    # Penalización geográfica
    geo_scores = apply_geographic_penalty(content_scores, user_location, geo_calculator, feature_weights.get('distance', 0))
    
    # Filtrado colaborativo
    geo_scores['collaborative_score'] = geo_scores['model_id'].apply(lambda x: predict_rating(user_id, x, collaborative_model))
    
    # Calcular puntaje híbrido
    geo_scores['hybrid_score'] = (
        geo_scores['similarity_score'] * 0.4 +
        geo_scores['collaborative_score'] * 0.4 +
        geo_scores['geo_score'] * 0.2
    )

    # Normalizar el puntaje híbrido a un rango de 0-10
    min_score = geo_scores['hybrid_score'].min()
    max_score = geo_scores['hybrid_score'].max()
    geo_scores['hybrid_score'] = round(geo_scores['hybrid_score'].apply(lambda x: 10 * (x - min_score) / (max_score - min_score) if max_score > min_score else 0), 2)
    
    return geo_scores.sort_values('hybrid_score', ascending=False)

