import tkinter as tk
from tkinter import ttk, messagebox
from modules.hybrid_recommender import HybridRecommender
from modules.collaborative_filter import CollaborativeFilter
from modules.geo_utils import GeoUtils
from modules.data_loader import DataLoader
import os

# Configuración
cars_path = 'data/coches.csv'
ratings_path = 'data/car_ratings.csv'
distance_cache = 'data/distance_cache.csv'
user_id = 'new_user'

# Cargar datos y modelos
cars_df, ratings_df = DataLoader(cars_path, ratings_path).load_data()
collaborative_model = CollaborativeFilter()
collaborative_model.train_model(ratings_path)
geo_calculator = GeoUtils()


class CarRecommenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Coches")
        self.geometry("1400x800")  # Tamaño ajustado
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
        files = [cars_path, ratings_path, distance_cache]
        missing_files = [file for file in files if not os.path.exists(file)]
        if missing_files:
            messagebox.showerror(
                "Error",
                f"Faltan los siguientes archivos necesarios para ejecutar el programa:\n{', '.join(missing_files)}"
            )
            return False
        return True

    def create_header(self):
        header = tk.Frame(self, bg="#2b6cb0", height=60)
        header.pack(fill="x", side="top")

        title = tk.Label(
            header, text="Bienvenido al Recomendador de Coches",
            font=("Helvetica", 20, "bold"), fg="white", bg="#2b6cb0", pady=10
        )
        title.pack()

    def setup_styles(self):
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
        self.notebook.tab(1, state="normal")
        self.notebook.select(1)

    def enable_results_page(self):
        self.notebook.tab(2, state="normal")
        self.notebook.select(2)


class CharacteristicsPage(tk.Frame):
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
            "fuel": "Tipo de combustible (Diesel, Gasolina, Eléctrico, Híbrido)",
            "year": "Año del coche",
            "kms": "Kilometraje del coche",
            "power": "Potencia del coche en caballos",
            "doors": "Número de puertas (2, 3, 4, 5)",
            "shift": "Tipo de transmisión (Automático, Manual)",
            "color": "Color del coche"
        }
        self.inputs = {}

        # Contenedor del formulario
        self.form = ttk.LabelFrame(self, text="Características del Coche", padding=20, style="Custom.TFrame")
        self.form.pack(fill="both", expand=True, padx=20, pady=20)

        for feature in self.features:
            row = ttk.Frame(self.form, style="Custom.TFrame")
            row.pack(fill="x", pady=5)
            label = ttk.Label(row, text=self.feature_labels[feature], width=30, anchor="w", style="Custom.TLabel")
            label.pack(side="left")
            entry = ttk.Entry(row)
            entry.pack(side="right", fill="x", expand=True)
            self.inputs[feature] = entry

        row = ttk.Frame(self.form)
        row.pack(fill="x", pady=5)
        label = ttk.Label(row, text="Ubicación (ciudad)", width=30, anchor="w", style="Custom.TLabel")
        label.pack(side="left")
        self.location_entry = ttk.Entry(row)
        self.location_entry.pack(side="right", fill="x", expand=True)

        next_button = ttk.Button(self, text="Siguiente", command=self.collect_data, style="Custom.TButton")
        next_button.pack(pady=20)

    def collect_data(self):
        self.parent.user_input = {
            k: int(v.get()) if v.get().isdigit() else (None if v.get().strip() == "" else v.get())
            for k, v in self.inputs.items()
        }
        self.parent.user_location = self.location_entry.get().strip()

        if not self.parent.user_location:
            messagebox.showerror("Error", "La ubicación es obligatoria.")
            return

        self.parent.weights_page.update_weights()
        self.parent.enable_weights_page()


class WeightsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.parent = parent
        self.weights = {}
        self.form = ttk.LabelFrame(self, text="Pesos de Características", padding=20, style="Custom.TFrame")
        self.form.pack(fill="both", expand=True, padx=20, pady=20)

        next_button = ttk.Button(self, text="Recomendar", command=self.collect_weights, style="Custom.TButton")
        next_button.pack(pady=20)

    def update_weights(self):
        for widget in self.form.winfo_children():
            widget.destroy()

        self.features_to_weight = [f for f in self.parent.user_input if self.parent.user_input[f] is not None]

        if not self.features_to_weight:
            messagebox.showerror("Error", "Debes seleccionar al menos una característica.")
            return

        for feature in self.features_to_weight:
            row = ttk.Frame(self.form, style="Custom.TFrame")
            row.pack(fill="x", pady=5)
            label = ttk.Label(row, text=f"Peso para {self.parent.characteristics_page.feature_labels[feature]} (0-10)", width=30, anchor="w", style="Custom.TLabel")
            label.pack(side="left")
            spinbox = ttk.Spinbox(row, from_=0, to=10, width=5)
            spinbox.pack(side="right", fill="x", expand=True)
            self.weights[feature] = spinbox

        row = ttk.Frame(self.form, style="Custom.TFrame")
        row.pack(fill="x", pady=5)
        label = ttk.Label(row, text="Peso para Distancia (0-10)", width=30, anchor="w", style="Custom.TLabel")
        label.pack(side="left")
        spinbox = ttk.Spinbox(row, from_=0, to=10, width=5)
        spinbox.pack(side="right", fill="x", expand=True)
        self.weights["distance"] = spinbox

    def collect_weights(self):
        try:
            self.parent.feature_weights = {k: int(v.get()) for k, v in self.weights.items()}
            if all(weight == 0 for weight in self.parent.feature_weights.values()):
                messagebox.showerror("Error", "Debes asignar al menos un peso mayor que 0.")
                return

            self.parent.results_page.generate_recommendations()
            self.parent.enable_results_page()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores válidos.")


class ResultsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.parent = parent
        self.results_area = ttk.LabelFrame(self, text="Recomendaciones", padding=20, style="Custom.TFrame")
        self.results_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(self.results_area, columns=(
            "make", "model", "price", "fuel", "year", "kms",
            "power", "doors", "shift", "color", "province", "distance"),
                                 show="headings", height=15)
        self.tree.pack(fill="both", expand=True)

        # Scrollbars
        self.scroll_y = ttk.Scrollbar(self.results_area, orient="vertical", command=self.tree.yview)
        self.scroll_x = ttk.Scrollbar(self.results_area, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=self.scroll_y.set, xscroll=self.scroll_x.set)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100, anchor="center")

    def generate_recommendations(self):
        try:
            recommender = HybridRecommender(collaborative_model, geo_calculator)
            recommendations = recommender.recommend(
                user_id, self.parent.user_input, self.parent.feature_weights,
                self.parent.user_location, cars_df
            )

            top_recommendations = recommendations[["make", "model", "price", "fuel", "year", "kms", "power",
                                                    "doors", "shift", "color", "province", "distance"]].head(10)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for _, row in top_recommendations.iterrows():
                self.tree.insert("", "end", values=row.tolist())

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar recomendaciones: {e}")


if __name__ == '__main__':
    app = CarRecommenderApp()
    app.mainloop()
