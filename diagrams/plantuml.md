
## Diagrama de Casos de Uso
```


```
## Diagrama de Clases
```

@startuml
class CollaborativeFilter {
    - model_path: str
    - model: any
    - testset: any
    + train_model(): None
    + predict_rating(): float
}

class ContentFilter {
    + calculate_content_similarity(): pd.DataFrame
}

class GeoUtils {
    - geolocator: Nominatim
    - cache_file: str
    - distance_cache: dict
    + calculate_distance(): float
    + apply_penalty(): pd.DataFrame
}

class HybridRecommender {
    - collaborative_model: CollaborativeFilter
    - geo_calculator: GeoUtils
    + recommend(): pd.DataFrame
}

class CarRecommenderApp {
    - cars_path: str
    - ratings_path: str
    - distance_cache: str
    - user_id: str
    + check_csv_files(): bool
    + get_user_input(): tuple
    + run(): None
}

class DataLoader {
    + load_data() : tuple
}

CarRecommenderApp --> HybridRecommender
HybridRecommender --* CollaborativeFilter
HybridRecommender --* GeoUtils
HybridRecommender --* ContentFilter
CarRecommenderApp -> DataLoader
@enduml

```
## Diagrama de Componentes
```
@startuml
left to right direction
[CarRecommenderApp]

package "modules" {

    
    [HybridRecommender]
[CollaborativeFilter]
[ContentFilter]
[GeoUtils]
[DataLoader]
}

package "data" {
    [coches.csv]
    [car_ratings.csv]
[distance_cache.csv]
}

[CarRecommenderApp] --> [HybridRecommender]
[CarRecommenderApp] --> [DataLoader]
[HybridRecommender] --> [CollaborativeFilter]
[HybridRecommender] --> [GeoUtils]
[HybridRecommender] --> [ContentFilter]

[DataLoader] ---> [coches.csv]
[DataLoader] ---> [car_ratings.csv]
[DataLoader] ---> [distance_cache.csv]

@enduml


```
## Diagrama de Flujo
```
@startuml
start

:Inicio;

:Verificar Archivos CSV;
if (¿Archivos disponibles?) then (sí)
    :Cargar coches.csv;
    :Cargar car_ratings.csv;
    :Cargar distance_cache.csv;
else (no)
    :Mostrar mensaje de error;
    stop
endif

:Entrenar Modelo Colaborativo;
if (¿Modelo existente?) then (sí)
    :Cargar modelo entrenado;
else (no)
    :Entrenar nuevo modelo;
endif

:Entrada del Usuario;
:Solicitar preferencias y pesos;

:Comprobar Localización;
if (¿Ciudad en cache?) then (sí)
    :Cargar distancias del cache;
else (no)
    :Calcular nuevas distancias;
endif

:Generación de Recomendaciones;
:Mostrar Top 10;

stop
@enduml

@startuml
start

:Inicio del entrenamiento;

if (¿Existe el modelo guardado?) then (sí)
    :Cargar modelo desde archivo;
    :Fin del entrenamiento;
    stop
else (no)
    :Cargar datos de valoraciones (CSV);
    :Configurar lector de datos (Surprise);
    :Crear dataset desde el DataFrame;
    :Dividir datos en conjunto de entrenamiento y prueba (train_test_split);

    :Definir parámetros del modelo (SVD);
    :Entrenar el modelo con el conjunto de entrenamiento;

    :Guardar el modelo entrenadoen un archivo;
endif

:Fin del entrenamiento;
stop
@enduml


```