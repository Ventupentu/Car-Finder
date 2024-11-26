from graphviz import Digraph

# Create a new directed graph
flowchart = Digraph(format='png', name="diagrama_flujo_recomendacion")

# Define nodes
flowchart.attr(rankdir='TB', size='8,10')

# Start and end nodes
flowchart.node("Inicio", "Inicio", shape="ellipse", style="filled", fillcolor="lightblue")
flowchart.node("Fin", "Fin", shape="ellipse", style="filled", fillcolor="lightblue")

# Process nodes
flowchart.node("VerificarCSV", "Verificar archivos CSV", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("ErrorCSV", "Error: Archivos CSV faltantes", shape="box", style="filled", fillcolor="pink")
flowchart.node("EntrenarModelo", "Entrenar modelo colaborativo", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("CargarDatos", "Cargar datos de coches y valoraciones", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("EntradaUsuario", "Recibir entrada del usuario\n(preferencias y pesos)", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("SimContenido", "Calcular similitud de contenido", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("PenalizarDist", "Aplicar penalización por distancia", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("PredColab", "Predicción colaborativa", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("CalcularPuntaje", "Calcular puntaje híbrido", shape="box", style="rounded,filled", fillcolor="lightyellow")
flowchart.node("MostrarResultados", "Mostrar recomendaciones", shape="box", style="rounded,filled", fillcolor="lightyellow")

# Redefinir las conexiones para corregir el error
flowchart.edge("Inicio", "VerificarCSV")
flowchart.edge("VerificarCSV", "ErrorCSV", label="no")
flowchart.edge("ErrorCSV", "Fin")
flowchart.edge("VerificarCSV", "EntrenarModelo", label="sí")
flowchart.edge("EntrenarModelo", "CargarDatos")
flowchart.edge("CargarDatos", "EntradaUsuario")
flowchart.edge("EntradaUsuario", "SimContenido")
flowchart.edge("SimContenido", "PenalizarDist")
flowchart.edge("PenalizarDist", "PredColab")
flowchart.edge("PredColab", "CalcularPuntaje")
flowchart.edge("CalcularPuntaje", "MostrarResultados")
flowchart.edge("MostrarResultados", "Fin")

# Renderizar el diagrama
diagram_path = "data/diagrama_flujo_recomendacion_corregido"
flowchart.render(diagram_path, format='png', cleanup=True)
diagram_path + ".png"

