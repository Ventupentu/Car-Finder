import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import os

class GeoUtils:
    """
    GeoUtils es una clase que proporciona utilidades para cálculos geográficos, como la distancia entre ubicaciones.

    Atributos:
        geolocator (Nominatim): Objeto geolocator de geopy para obtener coordenadas de ubicaciones.
        cache_file (str): Ruta al archivo CSV que contiene el caché de distancias.
        distance_cache (dict): Diccionario que almacena las distancias calculadas entre ubicaciones.
        cache_miss_message_shown (bool): Indica si se ha mostrado el mensaje de caché no encontrado
    """
    def __init__(self, user_agent="geo_calc", cache_file='data/distance_cache.csv'):
        """
        Inicializa una instancia de la clase GeoUtils.

        Args:
            user_agent (str): Nombre del agente de usuario para geopy.
            cache_file (str): Ruta al archivo CSV que contiene el caché de distancias.
        """
        self.geolocator = Nominatim(user_agent=user_agent)  # Inicializa el geolocator
        self.cache_file = cache_file  # Archivo de caché
        self.distance_cache = {}  # Diccionario de caché de distancias
        self.cache_miss_message_shown = False  # Indicador de mensaje de caché no encontrado
        self._load_cache()  # Carga el caché

    def _load_cache(self):
        """
        Carga el caché de distancias desde el archivo CSV especificado en el atributo cache_file.

        El archivo CSV debe tener las siguientes columnas:
        - origin: Ubicación de origen.
        - destination: Ubicación de destino.
        - distance_km: Distancia en kilómetros entre origen y destino.
        """
        if os.path.exists(self.cache_file):  # Verifica si el archivo de caché existe
            try:
                cache_df = pd.read_csv(self.cache_file)  # Lee el archivo CSV
                self.distance_cache = {
                    (row['origin'].lower(), row['destination'].lower()): row['distance_km']
                    for _, row in cache_df.iterrows()
                }  # Llena el diccionario de caché
            except Exception as e:
                print(f"Error al cargar el caché: {e}.")  # Manejo de errores

    def _save_cache(self):
        """
        Guarda el caché de distancias en el archivo CSV especificado en el atributo cache_file.

        El archivo CSV tendrá las siguientes columnas:
        - origin: Ubicación de origen.
        - destination: Ubicación de destino.
        - distance_km: Distancia en kilómetros entre origen y destino.
        """
        cache_data = [
            {"origin": origin, "destination": destination, "distance_km": round(distance, 2)}
            for (origin, destination), distance in self.distance_cache.items()
        ]  # Prepara los datos para guardar
        cache_df = pd.DataFrame(cache_data)  # Crea un DataFrame
        cache_df.to_csv(self.cache_file, index=False)  # Guarda el DataFrame en un archivo CSV

    def calculate_distance(self, origin, destination):
        """
        Calcula la distancia en kilómetros entre dos ubicaciones geográficas.

        Args:
            origin (str): Ubicación de origen.
            destination (str): Ubicación de destino.

        Returns:
            float: La distancia en kilómetros entre las dos ubicaciones, o None si no se puede calcular.
        """
        origin = origin.lower()  # Convierte a minúsculas
        destination = destination.lower()  # Convierte a minúsculas

        # Verifica si la distancia ya está en caché
        if (origin, destination) in self.distance_cache or (destination, origin) in self.distance_cache:
            return self.distance_cache.get((origin, destination)) or self.distance_cache.get((destination, origin))
        if not self.cache_miss_message_shown:
            print("Distancia no encontrada en caché. Esto puede tardar unos segundos...")
            self.cache_miss_message_shown = True
        try:
            # Obtiene las coordenadas de las ubicaciones
            coords_origin = self.geolocator.geocode(origin)
            coords_dest = self.geolocator.geocode(destination)
            if coords_origin and coords_dest:
                # Calcula la distancia geodésica
                distance = geodesic(
                    (coords_origin.latitude, coords_origin.longitude),
                    (coords_dest.latitude, coords_dest.longitude)
                ).kilometers
                self.distance_cache[(origin, origin)] = 0.0  # Distancia de origen a sí mismo es 0
                self.distance_cache[(origin, destination)] = distance  # Guarda la distancia en caché
                self._save_cache()  # Guarda el caché actualizado
                return round(distance, 2)  # Retorna la distancia redondeada
        except Exception as e:
            print(f"Error al calcular la distancia: {e}")  # Manejo de errores

        return None

    def apply_penalty(self, car_data, user_location, distance_weight):
        """
        Aplica una penalización a los datos de los autos basada en la distancia a la ubicación del usuario.

        Args:
            car_data (pd.DataFrame): DataFrame que contiene los datos de los autos.
            user_location (str): Ubicación del usuario.
            distance_weight (float): Peso de la penalización por distancia.

        Returns:
            pd.DataFrame: DataFrame con los datos de los autos y una columna adicional 'geo_score' 
                        que indica la penalización por distancia, ordenado de menor a mayor distancia.
        """
        max_distance = 200  # Distancia máxima para penalización
        car_data['distance'] = round(car_data['province'].apply(
            lambda x: self.calculate_distance(user_location, x) if self.calculate_distance(user_location, x) is not None else max_distance
        ), 2)  # Calcula la distancia para cada auto
        car_data['geo_score'] = car_data['distance'].apply(
            lambda x: -distance_weight * (x / max_distance) if x < max_distance else -distance_weight
        )  # Aplica la penalización basada en la distancia
        return car_data  # Retorna el DataFrame modificado
