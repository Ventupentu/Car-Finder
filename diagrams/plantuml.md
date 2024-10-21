
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
```