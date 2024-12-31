"""
Aplicación de Recomendación de Coches (Intergaz Grágica)

Este módulo proporciona una interfaz gráfica para recomendar coches a los usuarios
basándose en sus preferencias y ubicación.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from modules.hybrid_recommender import HybridRecommender
from modules.collaborative_filter import CollaborativeFilter
from modules.geo_utils import GeoUtils
from modules.data_loader import DataLoader


# Rutas
CARS_PATH = 'data/coches.csv'
RATINGS_PATH = 'data/car_ratings.csv'
DISTANCE_CACHE = 'data/distance_cache.csv'
USER_ID = 'new_user'

# Cargar clases para el modelo y los datos
cars_df, ratings_df = DataLoader(CARS_PATH, RATINGS_PATH).load_data()
collaborative_model = CollaborativeFilter()
collaborative_model.train_model(RATINGS_PATH)
geo_calculator = GeoUtils()


class CarRecommenderApp(tk.Tk):
    """
    CarRecommenderApp es una aplicación con interfaz gráfica que recomienda coches
    a los usuarios basándose en sus preferencias y ubicación.

    Atributos:
        user_input (dict): Diccionario con las características y valores
        proporcionados por el usuario.
        feature_weights (dict): Diccionario con los pesos asignados a cada característica.
        user_location (str): Ubicación del usuario en formato de texto
    """
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Coches")
        self.geometry("1400x700")  # Tamaño ajustado
        self.configure(bg="#edf2f7")  # Fondo claro y moderno

        self.user_input = {}
        self.feature_weights = {}
        self.user_location = ""

        # Verificar archivos necesarios
        if not self.check_csv_files():
            self.destroy()
            return

        # Crear encabezado
        self.create_header()

        # Crear estilos personalizados
        self.setup_styles()

        # Crear pestañas
        self.notebook = ttk.Notebook(self, style="CustomNotebook.TNotebook")
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        self.characteristics_page = CharacteristicsPage(self)
        self.weights_page = WeightsPage(self)
        self.results_page = ResultsPage(self)

        self.notebook.add(self.characteristics_page, text="Paso 1: Características")
        self.notebook.add(self.weights_page, text="Paso 2: Pesos")
        self.notebook.add(self.results_page, text="Paso 3: Resultados")

        self.notebook.tab(1, state="disabled")
        self.notebook.tab(2, state="disabled")

    def check_csv_files(self):
        """
        Verifica si los archivos CSV necesarios para la aplicación
        existen en las rutas especificadas.

        Returns:
            bool: True si los archivos existen, False en caso contrario.
        """
        files = [CARS_PATH, RATINGS_PATH, DISTANCE_CACHE]
        missing_files = [file for file in files if not os.path.exists(file)]
        if missing_files:
            messagebox.showerror(
                "Error",
                "Faltan los siguientes archivos necesarios para ejecutar el programa:\n"
                f"{', '.join(missing_files)}"
            )
            return False
        return True

    def create_header(self):
        """Crea el encabezado de la aplicación."""
        header = tk.Frame(self, bg="#2b6cb0", height=60)
        header.pack(fill="x", side="top")

        title = tk.Label(
            header, text="Bienvenido al Recomendador de Coches",
            font=("Helvetica", 20, "bold"), fg="white", bg="#2b6cb0", pady=10
        )
        title.pack()

    def setup_styles(self):
        """Configura los estilos personalizados para la interfaz."""
        style = ttk.Style()
        style.theme_use("default")

        # Estilo para pestañas
        style.configure(
            "CustomNotebook.TNotebook",
            background="#edf2f7",
            tabmargins=[2, 5, 2, 0],
        )
        style.configure(
            "CustomNotebook.TNotebook.Tab",
            font=("Helvetica", 12, "bold"),
            padding=[10, 5],
            background="#d9e3f0",
            foreground="#2b6cb0",
        )
        style.map(
            "CustomNotebook.TNotebook.Tab",
            background=[("selected", "#2b6cb0")],
            foreground=[("selected", "#ffffff")],
        )

        # Estilo para botones
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 12, "bold"),
            foreground="white",
            background="#2b6cb0",
            padding=10,
            relief="flat",
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#1a436a")],
            foreground=[("active", "white")],
        )

        # Estilo para etiquetas
        style.configure(
            "Custom.TLabel",
            font=("Helvetica", 12),
            padding=5,
        )

        # Estilo para contenedores
        style.configure(
            "Custom.TFrame",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
        )

    def enable_weights_page(self):
        """Habilita la pestaña de pesos y la selecciona."""
        self.notebook.tab(1, state="normal")
        self.notebook.select(1)

    def enable_results_page(self):
        """Habilita la pestaña de resultados y la selecciona."""
        self.notebook.tab(2, state="normal")
        self.notebook.select(2)


class CharacteristicsPage(tk.Frame):
    """
    CharacteristicsPage permite al usuario ingresar las características del coche
    que desea recomendar.

    Atributos:
        parent (tk.Tk): La ventana principal de la aplicación.
        features (list): Lista de características del coche.
        feature_labels (dict): Diccionario de etiquetas para las características.
        feature_tooltips (dict): Diccionario de descripciones para las características.
        inputs (dict): Diccionario para almacenar las entradas de características.
        form (ttk.LabelFrame): Contenedor para los campos de entrada de características.
        location_entry (ttk.Entry): Campo de entrada para la ubicación del usuario.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.parent = parent
        self.features = [
            "make", "price", "fuel", "year", "kms",
            "power", "doors", "shift", "color"
        ]
        self.feature_labels = {
            "make": "Marca del coche",
            "price": "Precio del coche",
            "fuel": "Tipo de combustible",
            "year": "Año del coche",
            "kms": "Kilometraje del coche",
            "power": "Potencia del coche en cv",
            "doors": "Número de puertas",
            "shift": "Tipo de transmisión",
            "color": "Color del coche"
        }
        self.feature_tooltips = {
            "make": "ABARTH, ALFA ROMEO, ALPINE, ARO, ASTON MARTIN, AUDI, AUSTIN, "\
                    "BENTLEY, BMW, CADILLAC, CHEVROLET, CHRYSLER, CITROEN, CORVETTE, "\
                    "CUPRA, DACIA, DAEWOO, DAIHATSU, DFSK, DODGE, DR AUTOMOBILES, DS, "\
                    "FERRARI, FIAT, FORD, GALLOPER, HONDA, HUMMER, HYUNDAI, INFINITI, "\
                    "ISUZU, IVECO, IVECO-PEGASO, JAGUAR, JEEP, KIA, LADA, LAMBORGHINI, "\
                    "LANCIA, LAND-ROVER, LDV, LEXUS, LOTUS, MAHINDRA, MASERATI, MAXUS, "\
                    "MAZDA, MERCEDES-BENZ, MG, MINI, MITSUBISHI, MORGAN, NISSAN, OPEL, "\
                    "PEUGEOT, PIAGGIO, PONTIAC, PORSCHE, RENAULT, ROVER, SAAB, "\
                    "SANTANA, SEAT, SKODA, SMART, SSANGYONG, SUBARU, SUZUKI, TATA, "\
                    "TESLA, TOYOTA, UMM, VAZ, VOLKSWAGEN, VOLVO",
            "fuel": "Gasolina, Diesel, Hibrido enchufable, Gas natural, Electrico, " \
                    "Hibrido, Gas licuado",
            "shift": "Manual, Automatico"
        }
        self.inputs = {}

        # Contenedor del formulario
        self.form = ttk.LabelFrame(
            self, text="Características del Coche", padding=20, style="Custom.TFrame"
        )
        self.form.pack(fill="both", expand=True, padx=20, pady=20)

        for feature in self.features:
            row = ttk.Frame(self.form)
            row.pack(fill="x", pady=5)
            label = ttk.Label(
                row, text=self.feature_labels[feature], width=30, anchor="w", style="Custom.TLabel"
            )
            label.pack(side="left")
            entry = ttk.Entry(row)
            entry.pack(side="left", fill="x", expand=False)
            self.inputs[feature] = entry

            # Agregar tooltip si la característica tiene descripción
            if feature in self.feature_tooltips:
                tooltip_icon = ttk.Label(
                    row, text="🛈", cursor="question_arrow",
                    font=("Helvetica", 12), style="Custom.TLabel"
                )
                tooltip_icon.pack(side="left")
                self.create_tooltip(tooltip_icon, self.feature_tooltips[feature])

        row = ttk.Frame(self.form)
        row.pack(fill="x", pady=5)
        label = ttk.Label(row, text="Ubicación", width=30, anchor="w", style="Custom.TLabel")
        label.pack(side="left")
        self.location_entry = ttk.Entry(row)
        self.location_entry.pack(side="left", fill="x", expand=False)

        next_button = ttk.Button(
            self, text="Siguiente", command=self.collect_data, style="Custom.TButton"
        )
        next_button.pack(pady=20)

    def create_tooltip(self, widget, text):
        """Crea un tooltip."""
        tooltip = tk.Toplevel(self)
        tooltip.withdraw()  # Oculta el tooltip inicialmente
        tooltip.overrideredirect(True)  # Elimina la barra de título y los bordes
        tooltip.configure(bg="#edf2f7", padx=5, pady=5, relief="solid", borderwidth=1)

        label = tk.Label(
            tooltip,
            text=text,
            justify="left",
            wraplength=300,
            bg="#edf2f7",
            font=("Helvetica", 10)
        )
        label.pack()

        def show_tooltip(event):
            # Posiciona el tooltip cerca del cursor del ratón
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.deiconify()  # Muestra el tooltip

        def hide_tooltip():
            tooltip.withdraw()  # Oculta el tooltip

        # Asocia los eventos del ratón al widget
        widget.bind("<Enter>", show_tooltip)  # Al entrar el ratón
        widget.bind("<Leave>", hide_tooltip)  # Al salir el ratón

    def collect_data(self):
        """Recoge los datos ingresados por el usuario y los valida."""
        try:
            self.parent.user_input = {
                k: int(v.get()) if v.get().isdigit() else (
                    None if v.get().strip() == "" else v.get()
                )
                for k, v in self.inputs.items()
            }
            self.parent.user_location = self.location_entry.get().strip()

            if not self.parent.user_location:
                messagebox.showerror("Error", "La ubicación es obligatoria.")
                return

            for feature, value in self.parent.user_input.items():
                if value is None:
                    continue
                if feature in ["price", "year", "kms", "power", "doors"] and \
                   not isinstance(value, int):
                    messagebox.showerror(
                        "Error",
                        f"El valor para {self.feature_labels[feature]} debe ser un número."
                    )
                    return
                if feature in ["make", "fuel", "shift", "color"] and not isinstance(value, str):
                    messagebox.showerror(
                        "Error",
                        f"El valor para {self.feature_labels[feature]} debe ser un texto."
                    )
                    return

            self.parent.weights_page.update_weights()
            self.parent.enable_weights_page()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores válidos.")


class WeightsPage(tk.Frame):
    """
    WeightsPage permite al usuario asignar pesos a las características seleccionadas
    para la recomendación de coches.

    Atributos:
        parent (tk.Tk): La ventana principal de la aplicación.
        weights (dict): Diccionario para almacenar los pesos de las características.
        form (ttk.LabelFrame): Contenedor para los campos de entrada de pesos.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.parent = parent
        self.weights = {}
        self.features_to_weight = []
        self.form = ttk.LabelFrame(self, text="Pesos de Características", padding=20,
                                   style="Custom.TFrame")
        self.form.pack(fill="both", expand=False, padx=20, pady=20)

        next_button = ttk.Button(self, text="Recomendar",command=self.collect_weights,
                                 style="Custom.TButton")
        next_button.pack(pady=20)

    def update_weights(self):
        """Actualiza los campos de pesos basados en las características seleccionadas."""
        for widget in self.form.winfo_children():
            widget.destroy()

        self.features_to_weight = [f for f in self.parent.user_input
                                   if self.parent.user_input[f] is not None]

        if not self.features_to_weight:
            messagebox.showerror("Error", "Debes seleccionar al menos una característica.")
            return

        for feature in self.features_to_weight:
            row = ttk.Frame(self.form)
            row.pack(fill="x", pady=5)
            label_text = f"Peso para {self.parent.characteristics_page.feature_labels[feature]}"
            label = ttk.Label(row, text=label_text, width=30, anchor="w", style="Custom.TLabel")
            label.pack(side="left")
            entry = ttk.Entry(row)
            entry.pack(side="left", fill="x", expand=False)
            self.weights[feature] = entry

        row = ttk.Frame(self.form)
        row.pack(fill="x", pady=5)
        label = ttk.Label(row, text="Peso para Distancia", width=30, anchor="w",
                          style="Custom.TLabel")
        label.pack(side="left")
        distance_entry = ttk.Entry(row)
        distance_entry.pack(side="left", fill="x", expand=False)
        self.weights["distance"] = distance_entry

    def collect_weights(self):
        """Recoge los pesos ingresados por el usuario y los valida."""
        try:
            self.parent.feature_weights = {k: int(v.get()) for k, v in self.weights.items()}
            for weight in self.parent.feature_weights.values():
                if weight < 1 or weight > 10:
                    messagebox.showerror("Error", "Los pesos deben estar entre 1 y 10.")
                    return
                if all(weight == 0 for weight in self.parent.feature_weights.values()):
                    messagebox.showerror("Error", "Debes asignar al menos un peso mayor que 0.")
                    return

            self.parent.results_page.generate_recommendations()
            self.parent.enable_results_page()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores válidos.")


class ResultsPage(tk.Frame):
    """
    ResultsPage muestra las recomendaciones de coches basadas en las preferencias
    y ubicación del usuario.

    Atributos:
        parent (tk.Tk): La ventana principal de la aplicación.
        results_area (ttk.LabelFrame): Contenedor para mostrar las recomendaciones.
        tree (ttk.Treeview): Tabla para mostrar las recomendaciones de coches.
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.parent = parent
        self.results_area = ttk.LabelFrame(self, text="Recomendaciones",
                                           padding=20, style="Custom.TFrame")
        self.results_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(self.results_area, columns=(
            "make", "model", "price", "fuel", "year", "kms",
            "power", "doors", "shift", "color", "province", "distance"),
                                 show="headings", height=15)
        self.tree.pack(fill="both", expand=True)

        # Scrollbars
        self.scroll_y = ttk.Scrollbar(self.results_area, orient="vertical",
                                      command=self.tree.yview)
        self.scroll_x = ttk.Scrollbar(self.results_area, orient="horizontal",
                                      command=self.tree.xview)
        self.tree.configure(yscroll=self.scroll_y.set, xscroll=self.scroll_x.set)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100, anchor="center")

    def generate_recommendations(self):
        """Genera recomendaciones basadas en los datos y pesos proporcionados por el usuario."""
        try:
            recommender = HybridRecommender(collaborative_model, geo_calculator)
            recommendations = recommender.recommend(
                USER_ID, self.parent.user_input, self.parent.feature_weights,
                self.parent.user_location, cars_df
            )

            top_recommendations = recommendations[["make", "model", "price", "fuel",
                                                   "year", "kms", "power", "doors",
                                                   "shift", "color", "province",
                                                   "distance"]].head(10)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for _, row in top_recommendations.iterrows():
                self.tree.insert("", "end", values=row.tolist())

        except (ValueError, KeyError, TypeError) as exception:
            messagebox.showerror("Error", f"Error al generar recomendaciones: {exception}")

        exit_button = ttk.Button(self, text="Salir", command=self.parent.destroy,
                                 style="Custom.TButton")
        exit_button.pack(pady=20)


if __name__ == '__main__':
    app = CarRecommenderApp()
    app.mainloop()
