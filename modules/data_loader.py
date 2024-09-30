# modules/data_loader.py

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

def assign_model_ids(df_cars: pd.DataFrame) -> pd.DataFrame:
    """
    Asigna un ID único a cada modelo de coche.
    
    :param df_cars: DataFrame de coches.
    :return: DataFrame de coches con 'model_id' añadido.
    """
    df_cars = df_cars.copy()
    df_cars['model_id'] = df_cars.groupby(['make', 'model']).ngroup() + 1
    return df_cars
