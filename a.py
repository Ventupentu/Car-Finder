import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from datetime import datetime, timedelta
# Definir colores para las barras
colors = [
    "#FF5733",  # Rojo
    "#33FF57",  # Verde
    "#3357FF",  # Azul
    "#FF33A1",  # Rosa
    "#FF8C33",  # Naranja
    "#8C33FF",  # Púrpura
    "#33FFF5",  # Cian
    "#F5FF33",  # Amarillo
]
# Definir las tareas del proyecto y sus duraciones
tasks = [
    ("Investigación", 1, "2023-09-23"),
    ("Planificación", 1, "2023-09-30"),
    ("Diseño Arquitectura", 3, "2023-10-07"),
    ("Código", 5, "2023-10-28"),
    ("Estructura de la Memoria", 1, "2023-11-18"),
    ("Memoria", 2, "2023-11-25"),
    ("Preparar la defensa", 1, "2023-12-02"),
]
# Asignar colores a las tareas sin repetir
task_colors = {}
for i, task in enumerate(tasks):
    task_colors[task[0]] = colors[i % len(colors)]
# Configurar fechas y tareas para el diagrama de Gantt
start_dates = [datetime.strptime(task[2], "%Y-%m-%d") for task in tasks]
durations = [timedelta(weeks=task[1]) for task in tasks]
end_dates = [start_dates[i] + durations[i] for i in range(len(tasks))]
# Crear el diagrama de Gantt
fig, ax = plt.subplots(figsize=(15, 8))
# Definir límites del eje X
ax.set_xlim(datetime(2023, 9, 23), max(end_dates) + timedelta(days=7))
ax.set_ylim(-0.5, len(tasks)-0.5)
# Configurar el formato de las fechas en el eje X
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1, byweekday=mdates.SA))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
# Crear las barras del diagrama y etiquetas en el eje Y
for i, task in enumerate(tasks):
    start = date2num(start_dates[i])
    duration = durations[i].days
    ax.barh(task[0], duration, left=start, height=0.2, align='center', color=task_colors[task[0]])
# Etiquetas y títulos
ax.set_xlabel('Fecha')
ax.set_ylabel('Tareas')
ax.set_title('Diagrama de Gantt Sistema de Recomendación de Automóviles')
# Ajustar formato del gráfico
plt.tight_layout()
plt.grid(True, axis='x', linestyle='--', alpha=0.7)
# Mostrar gráfico
plt.savefig("diagrams/gantt.svg")
plt.show()