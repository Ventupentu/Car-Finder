import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import os

class GeoDistanceCalculator:
    def __init__(self, user_agent="geo_calc", cache_file='data/distance_cache.csv'):
        """
        Inicializa el calculador de distancias, incluyendo el cargado de caché.
        """
        self.geolocator = Nominatim(user_agent=user_agent)
        self.cache_file = cache_file
        self.distance_cache = {}
        self._load_cache()

    def _load_cache(self):
        """
        Carga el caché de distancias desde el archivo CSV.
        """
        if os.path.exists(self.cache_file):
            try:
                cache_df = pd.read_csv(self.cache_file)
                self.distance_cache = {
                    (row['origin'].lower(), row['destination'].lower()): row['distance_km']
                    for _, row in cache_df.iterrows()
                }
            except Exception as e:
                print(f"Error al cargar el caché: {e}. Se iniciará vacío.")

    def _save_cache(self):
        """
        Guarda el caché de distancias actualizado en el archivo CSV.
        """
        cache_data = [
            {"origin": origin, "destination": destination, "distance_km": round(distance, 2)}
            for (origin, destination), distance in self.distance_cache.items()
        ]
        cache_df = pd.DataFrame(cache_data)
        cache_df.to_csv(self.cache_file, index=False)

    def calculate_distance(self, origin, destination):
        """
        Calcula la distancia entre dos ubicaciones.
        Si está en el caché, la devuelve directamente; si no, la calcula y la guarda.
        """
        origin = origin.lower()
        destination = destination.lower()

        if (origin, destination) in self.distance_cache:
            return self.distance_cache[(origin, destination)]

        try:
            coords_origin = self.geolocator.geocode(origin)
            coords_dest = self.geolocator.geocode(destination)
            if coords_origin and coords_dest:
                distance = geodesic(
                    (coords_origin.latitude, coords_origin.longitude),
                    (coords_dest.latitude, coords_dest.longitude)
                ).kilometers
                self.distance_cache[(origin, destination)] = distance
                self._save_cache()
                return distance
        except Exception as e:
            print(f"Error al calcular la distancia: {e}")

        # Si no se puede calcular, devolver un valor predeterminado alto
        return None

    def is_city_in_cache(self, city):
        """
        Verifica si una ciudad ya está en el caché como origen.
        """
        city = city.lower()
        return any(origin == city for origin, _ in self.distance_cache.keys())


def apply_geographic_penalty(car_data, user_location, geo_calculator, distance_weight):
    """
    Aplica penalizaciones geográficas basadas en distancias y peso de la distancia.
    """
    max_distance = 500  # Distancia máxima de referencia para escalar
    car_data['distance'] = car_data['province'].apply(lambda x: geo_calculator.calculate_distance(user_location, x) or max_distance)
    car_data['geo_score'] = car_data['distance'].apply(lambda x: -distance_weight * (x / max_distance) if x < max_distance else -distance_weight)
    return car_data

