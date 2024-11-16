import pandas as pd

def load_data(coches_path: str, ratings_path: str) -> tuple:
    """
    Carga los datasets de coches y valoraciones desde archivos CSV.
    
    :param coches_path: Ruta al archivo de coches.
    :param ratings_path: Ruta al archivo de valoraciones.
    :param sep: Separador del CSV.
    :return: Tuple (df_cars, df_ratings)
    """
    try:
        df_cars = pd.read_csv(coches_path)
        df_ratings = pd.read_csv(ratings_path)
        print("Datos cargados exitosamente.")
        return df_cars, df_ratings
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        raise

