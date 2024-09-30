import pandas as pd
from coche import Coche
#make;model;version;price;fuel;year;kms;power;doors;shift;color;province;country
def cargar_coches(csv_path):
    df = pd.read_csv(csv_path, sep=";", header=None, names=[
        "Marca", "Modelo", "Versión", "Precio", "Combustible", "Anio", 
        "Kilometraje", "Potencia", "Puertas", "Transmision", "Color", "Provincia", "Pais"
    ], encoding='latin1', skiprows=1)  # Aquí cambiamos la codificación y saltamos la primera fila    
    coches = []
    for _, row in df.iterrows():
        coche = Coche(
            marca=row['Marca'],
            modelo=row['Modelo'],
            descripcion=row['Versión'],
            precio=row['Precio'],
            combustible=row['Combustible'],
            anio=row['Anio'],
            kilometraje=row['Kilometraje'],
            potencia=row['Potencia'],
            puertas=row['Puertas'],
            transmision=row['Transmision'],
            color=row['Color'],
            provincia=row['Provincia'],
            pais=row['Pais']
        )
        coches.append(coche)
    
    return coches
