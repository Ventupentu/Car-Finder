## Diagrama de Actividad
```
@startuml ActivityDiagram

start

:User registers;
:System validates input;
if (Valid?) then (yes)
    :Create user account;
    -> [yes] :Registration successful;
else (no)
    :Display error message;
endif

:User logs in;
:System authenticates user;
if (Authentication successful?) then (yes)
    :Display user dashboard;
else (no)
    :Display login error;
endif

:User sets preferences;
:System receives preferences;
:Filter cars based on preferences;
:Calculate distances using GeoDistanceCalculator;
:Generate recommendations using RecommendationModel;
:Display recommendations to user;

stop

@enduml
```
## Diagrama de Casos de Uso
```
@startuml UseCaseDiagram

actor User
actor Admin

rectangle "Sistema de Recomendación de Coches" {
    User --> (Register)
    User --> (Login)
    User --> (Set Preferences)
    User --> (View Recommendations)
    
    Admin --> (Manage Users)
    Admin --> (Manage Data)
}

@enduml
```
## Diagrama de Clases
```
@startuml ClassDiagram

class User {
    - user_id: int
    - username: string
    - password: string
    + register()
    + login()
    + set_preferences()
}

class Authenticator {
    + authenticate(username: string, password: string): bool
}

class Preference {
    - make: string
    - model: string
    - min_price: float
    - max_price: float
    - fuel: string
    - max_year: int
    - max_kms: int
    - power: int
    - doors: int
    - shift: string
    - color: string
    - origin_city: string
    + get_preferences()
}

class GeoDistanceCalculator {
    - geolocator
    - cache: dict
    - cache_file: string
    + obtener_coordenadas(ubicacion, pais=None)
    + calcular_distancia(origen, destino, pais_origen=None, pais_destino=None)
    - _load_distance_cache()
    - _save_distance_cache()
}

class RecommendationModel {
    - model
    - trainset
    - testset
    - rmse
    - mae
    + train(test_size, random_state)
    + evaluate(): tuple
    + predict_rating(user_id, model_id): float
}

class DataLoader {
    + load_data(coches_path, ratings_path, sep=';'): tuple
    + assign_model_ids(df_cars): DataFrame
}

class Database {
    + query(sql: string): DataFrame
    + execute(sql: string)
}

class Car {
    - model_id: int
    - make: string
    - model: string
    - price: float
    - fuel: string
    - year: int
    - kms: int
    - power: int
    - doors: int
    - shift: string
    - color: string
    - province: string
}

class Rating {
    - user_id: int
    - model_id: int
    - rating: float
}

User --> Authenticator
User --> Preference
Preference --> RecommendationModel
RecommendationModel --> GeoDistanceCalculator
GeoDistanceCalculator --> Database
DataLoader --> Database
Car --> Rating

@enduml
```
## Diagrama de Componentes
```
@startuml ComponentDiagram

[Web Frontend] --> [Backend]

[Backend] --> [GeoDistanceCalculator]
[Backend] --> [RecommendationModel]
[Backend] --> [DataLoader]

[GeoDistanceCalculator] --> [Database]
[DataLoader] --> [Database]
[RecommendationModel] --> [Database]

[Database] --> [Backend]

@enduml
```
## Diagrama de Despliegue
```
@startuml DeploymentDiagram

node "User's Browser" {
    component "Web Frontend"
}

node "Web Server" {
    component "Web Frontend"
}

node "Application Server" {
    component "Backend"
    component "GeoDistanceCalculator"
    component "RecommendationModel"
    component "DataLoader"
}

node "Database Server" {
    database "Database"
}

[Web Frontend] --> [Application Server]
[Backend] --> [Database Server]
[GeoDistanceCalculator] --> [Database Server]
[RecommendationModel] --> [Database Server]
[DataLoader] --> [Database Server]

@enduml
```
## Diagrama de Estado
```
@startuml StateDiagram

[*] --> LoggedOut

LoggedOut --> Registering : User chooses to register
LoggedOut --> LoggingIn : User chooses to login

Registering --> LoggedIn : Successful registration
Registering --> LoggedOut : Registration failed

LoggingIn --> LoggedIn : Successful login
LoggingIn --> LoggedOut : Login failed

LoggedIn --> SettingPreferences : User sets preferences
LoggedIn --> LoggedOut : User logs out

SettingPreferences --> LoggedIn : Preferences set

@enduml
```
## Diagrama de Objeto
```
@startuml ObjectDiagram

object User1 {
    user_id = 1
    username = "johndoe"
    password = "hashed_pwd"
}

object Auth {
    // Authentication instance
}

object Pref1 {
    make = "PORSCHE"
    model = 911
    min_price = 50000
    max_price = 400000
    fuel = null
    max_year = null
    max_kms = null
    power = 500
    doors = null
    shift = null
    color = null
    origin_city = "Madrid"
}

object GeoCalc {
    // GeoDistanceCalculator instance
}

object Recommender {
    // RecommendationModel instance
}

object DataLoad {
    // DataLoader instance
}

object DB {
    // Database instance
}

object Car1 {
    model_id = 713
    make = "PORSCHE"
    model = "911"
    price = 262000
    fuel = "Gasolina"
    year = 2021
    kms = 70
    power = 650
    doors = 2
    shift = "Automatico"
    color = "Gris"
    province = "Murcia"
}

object Rating1 {
    user_id = 202
    model_id = 713
    rating = 4
}

User1 --> Auth
User1 --> Pref1
Pref1 --> Recommender
Recommender --> GeoCalc
GeoCalc --> DB
DataLoad --> DB
Car1 --> Rating1

@enduml
```
## Diagrama de Secuencia

```
@startuml SequenceDiagram

actor User

participant "Web Frontend" as Frontend
participant "Backend" as Backend
participant "Database" as DB
participant "GeoDistanceCalculator" as Geo
participant "RecommendationModel" as Recommender

User -> Frontend: Register/Login
Frontend -> Backend: Authenticate(user_credentials)
Backend -> DB: Verify credentials
DB --> Backend: Credentials valid
Backend --> Frontend: Authentication success
Frontend --> User: Display dashboard

User -> Frontend: Set Preferences
Frontend -> Backend: Send preferences
Backend -> Recommender: Generate recommendations(preferences)
Recommender -> Geo: Calculate distances(province)
Geo -> DB: Fetch distance from cache
alt Distance not in cache
    Geo -> Backend: Fetch from API
    Backend -> Geo: Distance data
    Geo -> DB: Save distance to cache
end
Geo --> Recommender: Distance data
Recommender --> Backend: Recommendations
Backend --> Frontend: Send recommendations
Frontend --> User: Display recommendations

@enduml
```
## Diagrama de Tiempo
```
@startuml TimingDiagram

robust "Web Frontend" as Frontend
robust "Backend" as Backend
robust "Database" as DB
robust "GeoDistanceCalculator" as Geo
robust "RecommendationModel" as Recommender

Frontend -> Backend: Authenticate
Backend -> DB: Verify credentials
DB --> Backend: Credentials valid
Backend --> Frontend: Authentication success

Frontend -> Backend: Send preferences
Backend -> Recommender: Generate recommendations
Recommender -> Geo: Calculate distances
Geo -> DB: Fetch distance from cache
DB --> Geo: Distance data
Geo --> Recommender: Distance
Recommender --> Backend: Recommendations
Backend --> Frontend: Send recommendations

@enduml
```
