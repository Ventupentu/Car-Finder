# main.py

from modules.data_loader import load_data, assign_model_ids
from modules.geo_utils import GeoDistanceCalculator
from modules.recommendation_model import RecommendationModel
from modules.recommender import recommend
import pandas as pd

def obtener_preferencias_usuario():
    """Obtiene las preferencias del usuario a través de inputs."""
    print("Introduce tus preferencias para el coche:")
    
    """
    user_preferences = {
        'make': input("Marca: ") or None,
        'model': input("Modelo: ") or None,
        'min_price': int(input("Precio mínimo (deja en blanco si no aplica): ") or 0),
        'max_price': int(input("Precio máximo (deja en blanco si no aplica): ") or 0),
        'fuel': input("Combustible (gasolina, diesel, etc.): ") or None,
        'year': int(input("Año mínimo (deja en blanco si no aplica): ") or 0),
        'max_kms': int(input("Kilómetros máximos (deja en blanco si no aplica): ") or 0),
        'power': int(input("Potencia mínima en CV (deja en blanco si no aplica): ") or 0),
        'doors': int(input("Número de puertas (deja en blanco si no aplica): ") or 0),
        'shift': input("Tipo de cambio (manual, automático): ") or None,
        'color': input("Color (rojo, negro, azul, etc.): ") or None,
        'origin_city': input("Ciudad de origen: ") or None,
    }
    """

    # Ejemplo de preferencias para probar
    user_preferences = {
        'min_price': 0,
        'max_price': 50000,
        'fuel': 'Diesel',
        'max_kms': 100000,
        'power': 100,
        'doors': 5,
        'shift': 'Manual',
        'color': 'Gris',
        'origin_city': 'Barcelona',
    }

    return user_preferences

def obtener_pesos_usuario():
    """Obtiene los pesos que el usuario asigna a las características del coche."""
    print("\nAsignar pesos a las características (más alto significa mayor importancia):")
    """
    weights = {
        'make': int(input("Peso para la marca: ") or 1),
        'model': int(input("Peso para el modelo: ") or 1),
        'min_price': int(input("Peso para el precio mínimo: ") or 1),
        'max_price': int(input("Peso para el precio máximo: ") or 1),
        'fuel': int(input("Peso para el tipo de combustible: ") or 1),
        'year': int(input("Peso para el año: ") or 1),
        'max_kms': int(input("Peso para los kilómetros: ") or 1),
        'power': int(input("Peso para la potencia: ") or 1),
        'doors': int(input("Peso para el número de puertas: ") or 1),
        'shift': int(input("Peso para el tipo de cambio: ") or 1),
        'color': int(input("Peso para el color: ") or 1),
        'origin_city': int(input("Peso para la ciudad de origen: ") or 1),
    }
    """
    # Ejemplo de pesos para probar
    weights = {
        'make': 0,
        'model': 1,
        'min_price': 2,
        'max_price': 4,
        'fuel': 10,
        'year': 10,
        'max_kms': 0,
        'power': 7,
        'doors': 4,
        'shift': 3,
        'color': 8,
        'origin_city': 7,
        'distance': 0,
    }
    
    return weights

def main():
    """Función principal para ejecutar la recomendación."""
    # Obtener preferencias del usuario
    user_preferences = obtener_preferencias_usuario()
    
    # Obtener pesos asignados por el usuario
    #weights = obtener_pesos_usuario()
    
    # Ejecutar el sistema de recomendación
    recomendaciones = recommend(user_preferences)
    
    # Mostrar el top 5 de recomendaciones en forma de tabla
    top5_recommendations = recomendaciones
    df = pd.DataFrame(top5_recommendations)
    print("\nTop 5 recomendaciones:")
    print(df)

if __name__ == "__main__":
    main()
