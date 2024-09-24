""" Ejemplo de cálculo de distancia geodésica entre dos ubicaciones geográficas """

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def obtener_coordenadas(ubicacion, pais=None):
    # Inicializa el geocodificador con Nominatim (basado en OpenStreetMap)
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    # Si se proporciona un país, lo añadimos a la búsqueda para mayor precisión
    if pais:
        location = geolocator.geocode(f"{ubicacion}, {pais}")
    else:
        location = geolocator.geocode(ubicacion)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"No se pudo encontrar la ubicación para: {ubicacion}")

def calcular_distancia(loc1, loc2, pais1=None, pais2=None):
    # Obtener coordenadas de ambas ubicaciones
    coords_1 = obtener_coordenadas(loc1, pais1)
    coords_2 = obtener_coordenadas(loc2, pais2)
    
    # Calcular la distancia geodésica (en kilómetros) entre las coordenadas
    distancia = geodesic(coords_1, coords_2).kilometers
    
    return distancia

# Ejemplo de uso con códigos postales, asegurando el país
ubicacion_1 = "28001"  # Madrid (código postal)
ubicacion_2 = "08001"  # Barcelona (código postal)
pais1 = "España"
pais2 = "España"

distancia = calcular_distancia(ubicacion_1, ubicacion_2, pais1, pais2)
print(f"La distancia entre {ubicacion_1} y {ubicacion_2} es de {distancia:.2f} km")

# Ejemplo de uso con nombres de ciudades
ciudad_1 = "Madrid"
ciudad_2 = "Barcelona"

distancia_ciudades = calcular_distancia(ciudad_1, ciudad_2, "España", "España")
print(f"La distancia entre {ciudad_1} y {ciudad_2} es de {distancia_ciudades:.2f} km")
