import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Datos de la planificación
tasks = [
    "Investigar documentación sobre la(s) librería(s)",
    "Investigar sobre surprise",
    "Investigar geopy",
    "Investigar y adaptar el dataset a la librería",
    "Crear la arquitectura y codificarla",
    "Continuar codificación",
    "Código y documentación de la arquitectura",
    "Entregar documento de la arquitectura y código",
    "Preparar código para entrega parcial",
    "Entregar prototipo tecnológico y código",
    "Desarrollar y finalizar estructura de la memoria",
    "Entregar estructura de la memoria",
    "Continuar código y memoria",
    "Tener código y memoria terminadas"
]

# Inicio y duración de cada tarea (en semanas)
start_weeks = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 9]
durations = [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1]

# Fecha inicial
start_date = datetime(2024, 10, 1)

# Crear el DataFrame para los datos
gantt_data = pd.DataFrame({
    'Task': tasks,
    'Start': [start_date + timedelta(weeks=w) for w in start_weeks],
    'End': [start_date + timedelta(weeks=w+d) for w, d in zip(start_weeks, durations)]
})

# Generar el gráfico de Gantt
fig, ax = plt.subplots(figsize=(10, 6))

# Dibujar las barras para cada tarea
for i, task in gantt_data.iterrows():
    ax.barh(task['Task'], (task['End'] - task['Start']).days, left=(task['Start'] - start_date).days)

# Definir los marcadores de las semanas (1 a 10)
week_ticks = [start_date + timedelta(weeks=i) for i in range(10)]  # 10 semanas
week_labels = [str(i+1) for i in range(10)]  # Solo los números de las semanas
ax.set_xticks([(date - start_date).days for date in week_ticks])
ax.set_xticklabels(week_labels)

# Etiquetas y título
ax.set_xlabel('Semanas')
ax.set_ylabel('Tareas')
ax.set_title('Gráfico de Gantt - Planificación del Proyecto')
plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)

# Mostrar gráfico
plt.tight_layout()
plt.show()
