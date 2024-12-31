"""
Este módulo contiene la clase DataLoader que se encarga de cargar datos desde archivos CSV.
"""

import pandas as pd

class DataLoader:
    """
    DataLoader es una clase que se encarga de cargar los datos de coches y ratings
    desde archivos CSV.

    Atributos:
        coches_path (str): Ruta al archivo CSV que contiene los datos de los coches.
        ratings_path (str): Ruta al archivo CSV que contiene las valoraciones de los usuarios.
    """
    def __init__(self, coches_path: str, ratings_path: str):
        self.coches_path = coches_path
        self.ratings_path = ratings_path

    def load_data(self) -> tuple:
        """
        Carga los datos de coches y valoraciones desde los archivos CSV especificados.

        Returns:
            tuple: Un par de DataFrames que contienen los datos de los coches y las valoraciones.
        """
        try:
            df_cars = pd.read_csv(self.coches_path)
            df_ratings = pd.read_csv(self.ratings_path)
            print("Datos cargados exitosamente.")
            return df_cars, df_ratings
        except Exception as exception:
            print(f"Error al cargar los datos: {exception}")
            raise
