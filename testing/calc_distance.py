""" Ejemplo de cálculo de distancia geodésica entre dos ubicaciones geográficas """

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class GeoDistanceCalculator:
    def __init__(self, user_agent="calc_distance"):
        self.geolocator = Nominatim(user_agent=user_agent)

    def obtener_coordenadas(self, ubicacion, pais=None):
        query = f"{ubicacion}, {pais}" if pais else ubicacion
        location = self.geolocator.geocode(query)
        
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError(f"No se pudo encontrar la ubicación para: {ubicacion}")

    def calcular_distancia(self, loc1, loc2, pais1=None, pais2=None):
        coords_1 = self.obtener_coordenadas(loc1, pais1)
        coords_2 = self.obtener_coordenadas(loc2, pais2)
        
        distancia = geodesic(coords_1, coords_2).kilometers
        return distancia

if __name__ == "__main__":
    calculator = GeoDistanceCalculator()

    # Ejemplo de uso con códigos postales, asegurando el país
    #ubicacion_1 = "28001"  # Madrid (código postal)
    #ubicacion_2 = "08001"  # Barcelona (código postal)
    pais1 = "España"
    pais2 = "España"

    #distancia = calculator.calcular_distancia(ubicacion_1, ubicacion_2, pais1, pais2)
    #print(f"La distancia entre {ubicacion_1} y {ubicacion_2} es de {distancia:.2f} km")

    # Ejemplo de uso con nombres de ciudades
    ciudad_1 = "Cataluña"
    ciudad_2 = "Galicia"

    distancia_ciudades = calculator.calcular_distancia(ciudad_1, ciudad_2, "España", "España")
    print(f"La distancia entre {ciudad_1} y {ciudad_2} es de {distancia_ciudades:.2f} km")
