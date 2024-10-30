# main.py

from modules.data_loader import load_data, assign_model_ids
from modules.geo_utils import GeoDistanceCalculator
from modules.recommendation_model import RecommendationModel
from modules.recommender import recommend

def obtener_preferencias_usuario():
    """Obtiene las preferencias del usuario a través de inputs."""
    print("Introduce tus preferencias para el coche:")
    
    user_preferences = {
        'min_price': float(input("Precio mínimo (deja en blanco si no aplica): ") or 0),
        'max_price': float(input("Precio máximo (deja en blanco si no aplica): ") or 0),
        'fuel': input("Combustible (gasolina, diesel, etc.): ") or None,
        'year': int(input("Año mínimo (deja en blanco si no aplica): ") or 0),
        'max_kms': int(input("Kilómetros máximos (deja en blanco si no aplica): ") or 0),
        'power': int(input("Potencia mínima en CV (deja en blanco si no aplica): ") or 0),
        'doors': int(input("Número de puertas (deja en blanco si no aplica): ") or 0),
        'shift': input("Tipo de cambio (manual, automático): ") or None,
        'color': input("Color (rojo, negro, azul, etc.): ") or None,
        'origin_city': input("Ciudad de origen: ") or None,
    }
    
    return user_preferences

def obtener_pesos_usuario():
    """Obtiene los pesos que el usuario asigna a las características del coche."""
    print("\nAsignar pesos a las características (más alto significa mayor importancia):")
    
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
        'distance': int(input("Peso para la distancia: ") or 1)  # Añadir peso para la distancia
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
    
    # Mostrar las recomendaciones
    if recomendaciones:
        print("\nEstas son las mejores recomendaciones de coches según tus preferencias:")
        for i, rec in enumerate(recomendaciones, 1):
            print(f"\nRecomendación {i}:")
            print(f"Marca: {rec['make']}")
            print(f"Modelo: {rec['model']}")
            print(f"Precio: {rec['price']} €")
            print(f"Combustible: {rec['fuel']}")
            print(f"Año: {rec['year']}")
            print(f"Kilómetros: {rec['kms']}")
            print(f"Potencia: {rec['power']} CV")
            print(f"Número de puertas: {rec['doors']}")
            print(f"Tipo de cambio: {rec['shift']}")
            print(f"Color: {rec['color']}")
            print(f"Provincia: {rec['province']}")
            print(f"Distancia desde tu ciudad: {rec['distance_km']} km")
            print(f"Calificación estimada: {rec['estimated_rating']}")

if __name__ == "__main__":
    main()
