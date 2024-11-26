import pandas as pd

class DataLoader:
    def __init__(self, coches_path: str, ratings_path: str):
        self.coches_path = coches_path
        self.ratings_path = ratings_path

    def load_data(self) -> tuple:
        """
        Carga los datasets de coches y valoraciones desde archivos CSV.
        
        :return: Tuple (df_cars, df_ratings)
        """
        try:
            df_cars = pd.read_csv(self.coches_path)
            df_ratings = pd.read_csv(self.ratings_path)
            print("Datos cargados exitosamente.")
            return df_cars, df_ratings
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            raise
