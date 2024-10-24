
## Diagrama de Casos de Uso
```


```
## Diagrama de Clases
```
@startuml
class InterfazGrafica {
    - user_preferences: dict
    - user_weights: dict
    + capturarPreferenciasUsuario(): dict
    + capturarImportanciaPesos(): dict
    + guardarPreferenciasYpesos()
    + mostrarTop5Coches(recomendaciones: list)
}

class Recomendador {
    + cargarDatos(coches, ratings)
    + predecirCalificaciones()
    + recomendar()
}



class GeoDistanceCalculator {
    + calcularCoordenadas()
}

folder "data" {

file coches.csv {

}

file ratings.csv {
}
}

InterfazGrafica --> Recomendador : Llamar recomendador con preferencias y pesos
Recomendador --> GeoDistanceCalculator
Recomendador --> InterfazGrafica : Devolver top 5 coches recomendados
GeoDistanceCalculator --> Recomendador

Recomendador -- data #black;line.dashed : Cargar datos de los csv
@enduml
```
## Diagrama de Componentes
```
@startuml
title Sistema de Recomendación de Coches
left to right direction
package "Interfaz Gráfica" {
    [InterfazGrafica]
}

package "Modelo Recomendación" {

    [Recomendador]
    [GeoDistanceCalculator]
}

package "Datos" {
    [coches.csv]
    [ratings.csv]
}



' Relaciones del sistema completo
[Usuario] --> [InterfazGrafica] : Introduce preferencias y pesos
[InterfazGrafica] --> [Recomendador] : Enviar preferencias y pesos
[Recomendador] --> [coches.csv] : Cargar datos de coches
[Recomendador] --> [ratings.csv] : Cargar datos de ratings
[Recomendador] --> [GeoDistanceCalculator] : Calcular coordenadas (si hay ciudad)
[Recomendador] --> [InterfazGrafica] : Enviar top 5 coches recomendados
[GeoDistanceCalculator] --> [Recomendador]

@enduml


```
## Diagrama de Flujo
```
@startuml
start
:Usuario abre la interfaz gráfica;
:Usuario introduce preferencias;
:Usuario introduce pesos;

:Guardar preferencias y pesos;

:Llamar al recomendador con los datos guardados;

if (Los CSV están accesibles?) then (Sí)
    :Leer CSV de coches;
    :Leer CSV de ratings;
    :Leer CSV de ciudades;
else (No)
    :Mostrar error de acceso a datos;
    stop
endif



if (¿Hay ciudad de origen?) then (Sí)
    :Calcular coordenadas con GeoDistanceCalculator;
else (No)
    :Continuar sin calcular distancia;
endif


:Predecir calificaciones para el usuario;
:Generar lista de recomendaciones;

:Mostrar top 5;

stop
@enduml

@startuml
start

:Inicializar el modelo SVD con hiperparámetros óptimos;

:Entrenar el modelo con los datos de ratings;
note right: Realiza división en training y test sets

if (¿Entrenamiento exitoso?) then (Sí)
    :Calcular predicciones para el test set;
    :Evaluar el modelo (RMSE, MAE);
    if (¿Métricas aceptables?) then (Sí)
        :Guardar el modelo entrenado;
    else (No)
        :Ajustar hiperparámetros;
        :Reentrenar el modelo;
    endif
else (No)
    :Mostrar error de entrenamiento;
    stop
endif

:Recibir las preferencias del usuario nuevo;

:Recibir pesos para cada característica;
note right: Los pesos indican la importancia de cada parámetro

if (¿El usuario introdujo algún peso?) then (Sí)
    :Asignar pesos a las características;
else (No)
    :Solicitar al usuario que asigne al menos un peso;
    stop
endif

:Calcular predicción base (mean rating) para el modelo;

if (¿Existen datos del modelo?) then (Sí)
    :Ajustar la predicción según las características del coche;
    :Penalizar/bonificar según la coincidencia de características;
    note right: Si no hay coincidencia o se exceden los límites, penaliza
else (No)
    :Usar la media global como estimación base;
endif

if (¿El usuario especificó una ciudad de origen?) then (Sí)
    :Calcular distancia del coche a la ciudad del usuario;
    if (Distancia alta y peso de distancia alto) then (Sí)
        :Penalizar por distancia lejana;
    endif
else (No)
    :Continuar sin penalización por distancia;
endif

:Generar predicción final para cada modelo de coche;

:Devolver la lista de recomendaciones ordenadas por calificación;

stop
@enduml

```