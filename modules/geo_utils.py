# modules/geo_utils.py

import pandas as pd
import os
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class GeoDistanceCalculator:
    def __init__(self, user_agent="calc_distance", cache_file='data/distance_cache.csv'):
        self.geolocator = Nominatim(user_agent=user_agent)
        self.cache = {}  # Cache para almacenar coordenadas y evitar repetidas consultas
        self.cache_file = cache_file
        self.distance_cache = {}  # Cache para almacenar distancias
        self._load_distance_cache()

    def _load_distance_cache(self):
        """
        Carga el caché de distancias desde el archivo CSV.
        """
        if os.path.exists(self.cache_file):
            try:
                df_cache = pd.read_csv(self.cache_file)
                for _, row in df_cache.iterrows():
                    origin = row['origin'].strip().lower()
                    destination = row['destination'].strip().lower()
                    distance = row['distance_km']
                    self.distance_cache[(origin, destination)] = distance
                    self.distance_cache[(destination, origin)] = distance  # Distancia simétrica
                print(f"Caché de distancias cargado desde {self.cache_file}.")
            except Exception as e:
                print(f"Error al cargar el caché de distancias: {e}")
        else:
            print(f"No se encontró el archivo de caché {self.cache_file}. Se creará uno nuevo.")

    def _save_distance_cache(self):
        """
        Guarda el caché de distancias en el archivo CSV.
        """
        try:
            # Solo guardar una dirección para evitar duplicados
            unique_pairs = {(min(k), max(k)): v for k, v in self.distance_cache.items() if k[0] <= k[1]}
            df_cache = pd.DataFrame([
                {'origin': origin, 'destination': destination, 'distance_km': distance}
                for (origin, destination), distance in unique_pairs.items()
            ])
            df_cache.to_csv(self.cache_file, index=False)
        except Exception as e:
            print(f"Error al guardar el caché de distancias: {e}")

    def obtener_coordenadas(self, ubicacion, pais=None):
        """
        Obtiene las coordenadas (latitud, longitud) de una ubicación.
        Utiliza una caché para evitar múltiples consultas a la API.
        
        :param ubicacion: Nombre de la ciudad.
        :param pais: Nombre del país.
        :return: Tuple (latitud, longitud) o None si no se encuentra.
        """
        key = f"{ubicacion},{pais}" if pais else ubicacion
        key = key.strip().lower()
        if key in self.cache:
            return self.cache[key]
        
        query = f"{ubicacion}, {pais}" if pais else ubicacion
        try:
            location = self.geolocator.geocode(query, timeout=10)
            if location:
                coords = (location.latitude, location.longitude)
                self.cache[key] = coords
                time.sleep(1)  # Pausa para respetar las políticas de uso de Nominatim
                return coords
            else:
                print(f"No se pudo encontrar la ubicación para: {ubicacion}")
                return None
        except Exception as e:
            print(f"Error al obtener coordenadas para {ubicacion}: {e}")
            return None

    def calcular_distancia(self, origen, destino, pais_origen=None, pais_destino=None):
        """
        Calcula la distancia en kilómetros entre dos ubicaciones.
        Utiliza el caché si la distancia ya ha sido calculada.
        
        :param origen: Ciudad de origen.
        :param destino: Ciudad de destino.
        :param pais_origen: País de origen.
        :param pais_destino: País de destino.
        :return: Distancia en kilómetros o None si no se puede calcular.
        """
        origen_key = origen.strip().lower()
        destino_key = destino.strip().lower()
        
        if (origen_key, destino_key) in self.distance_cache:
            return self.distance_cache[(origen_key, destino_key)]
        
        distancia = None
        coords_origen = self.obtener_coordenadas(origen, pais_origen)
        coords_destino = self.obtener_coordenadas(destino, pais_destino)
        
        if coords_origen and coords_destino:
            distancia = geodesic(coords_origen, coords_destino).kilometers
            # Guardar en el caché
            self.distance_cache[(origen_key, destino_key)] = distancia
            self.distance_cache[(destino_key, origen_key)] = distancia  # Distancia simétrica
            self._save_distance_cache()
        else:
            print(f"No se pudo calcular la distancia entre {origen} y {destino}.")
        
        return distancia
