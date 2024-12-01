import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import os

class GeoUtils:
    def __init__(self, user_agent="geo_calc", cache_file='data/distance_cache.csv'):
        self.geolocator = Nominatim(user_agent=user_agent)
        self.cache_file = cache_file
        self.distance_cache = {}
        self.cache_miss_message_shown = False
        self._load_cache()

    def _load_cache(self):
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
        cache_data = [
            {"origin": origin, "destination": destination, "distance_km": round(distance, 2)}
            for (origin, destination), distance in self.distance_cache.items()
        ]
        cache_df = pd.DataFrame(cache_data)
        cache_df.to_csv(self.cache_file, index=False)

    def calculate_distance(self, origin, destination):
        origin = origin.lower()
        destination = destination.lower()

        if (origin, destination) in self.distance_cache or (destination, origin) in self.distance_cache:
            return self.distance_cache.get((origin, destination)) or self.distance_cache.get((destination, origin))
        if not self.cache_miss_message_shown:
            print("Distancia no encontrada en caché. Esto puede tardar unos segundos...")
            self.cache_miss_message_shown = True
        try:
            coords_origin = self.geolocator.geocode(origin)
            coords_dest = self.geolocator.geocode(destination)
            if coords_origin and coords_dest:
                distance = geodesic(
                    (coords_origin.latitude, coords_origin.longitude),
                    (coords_dest.latitude, coords_dest.longitude)
                ).kilometers
                self.distance_cache[(origin, origin)] = 0.0
                self.distance_cache[(origin, destination)] = distance
                self._save_cache()
                return round(distance,2)
        except Exception as e:
            print(f"Error al calcular la distancia: {e}")

        return None

    def apply_penalty(self, car_data, user_location, distance_weight):
        max_distance = 5000
        car_data['distance'] = round(car_data['province'].apply(
            lambda x: self.calculate_distance(user_location, x) if self.calculate_distance(user_location, x) is not None else max_distance
        ), 2)
        car_data['geo_score'] = car_data['distance'].apply(
            lambda x: -distance_weight * (x / max_distance) if x < max_distance else -distance_weight
        )
        return car_data
