import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from modules.hybrid_recommender import hybrid_recommendation
from modules.collaborative_filter import train_collaborative_model
from modules.geo_utils import GeoDistanceCalculator
from modules.data_loader import load_data
import pandas as pd
import os

# Configuración
cars_path = 'data/coches.csv'
ratings_path = 'data/car_ratings.csv'
images_path = 'images/'  # Ruta donde se almacenan las imágenes
user_id = 'new_user'

class CarRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendador de Coches")

        self.user_input = {}
        self.feature_weights = {}
        self.user_location = None

        self.step = 0
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

        self.create_widgets()

    def create_widgets(self):
        # Crear un Canvas para el fondo
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Cargar la imagen de fondo
        self.bg_image = Image.open("images/background.jpg")  # Asegúrate de tener esta imagen en tu carpeta
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Ajustar tamaño
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Colocar la imagen de fondo en el Canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Agregar etiquetas y campos sobre el fondo
        self.label = ttk.Label(self.root, text="Bienvenido al recomendador de coches", font=("Arial", 14), background="white")
        self.label_window = self.canvas.create_window(400, 50, window=self.label)

        self.input_label = ttk.Label(self.root, text="Introduce Marca del coche:", background="white")
        self.input_label_window = self.canvas.create_window(400, 150, window=self.input_label)

        self.input_field = ttk.Entry(self.root)
        self.input_field_window = self.canvas.create_window(400, 180, window=self.input_field)

        self.next_button = ttk.Button(self.root, text="Siguiente", command=self.next_step)
        self.next_button_window = self.canvas.create_window(400, 230, window=self.next_button)

        self.results_window = None  # Atributo para almacenar el área de resultados

    def next_step(self):
        user_input = self.input_field.get().strip()
        feature_name = self.features[self.step]

        if user_input == "":
            self.user_input[feature_name] = None
        elif user_input.isdigit():
            self.user_input[feature_name] = int(user_input)
        else:
            self.user_input[feature_name] = user_input

        self.step += 1
        self.input_field.delete(0, tk.END)

        if self.step < len(self.features):
            next_feature = self.features[self.step]
            self.input_label.config(text=f"Introduce {self.feature_labels[next_feature]}:")
        else:
            self.ask_location()

    def ask_location(self):
        self.input_label.config(text="Introduce tu ubicación (ciudad):")
        self.next_button.config(command=self.set_location)

    def set_location(self):
        self.user_location = self.input_field.get().strip()
        if self.user_location == "":
            messagebox.showerror("Error", "La ubicación es obligatoria.")
        else:
            self.input_field.delete(0, tk.END)
            self.ask_weights()

    def ask_weights(self):
        self.step = 0
        self.features_to_weight = [f for f in self.features if self.user_input[f] is not None]
        if not self.features_to_weight:
            messagebox.showerror("Error", "Debes seleccionar al menos una característica.")
            return

        self.input_label.config(text=f"Peso para {self.feature_labels[self.features_to_weight[self.step]]} (0-10):")
        self.next_button.config(command=self.next_weight)

    def next_weight(self):
        try:
            weight = int(self.input_field.get().strip())
            if 0 <= weight <= 10:
                feature_name = self.features_to_weight[self.step]
                self.feature_weights[feature_name] = weight

                self.step += 1
                self.input_field.delete(0, tk.END)

                if self.step < len(self.features_to_weight):
                    next_feature = self.features_to_weight[self.step]
                    self.input_label.config(text=f"Peso para {self.feature_labels[next_feature]} (0-10):")
                else:
                    self.ask_distance_weight()
            else:
                messagebox.showerror("Error", "El peso debe estar entre 0 y 10.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido entre 0 y 10.")

    def ask_distance_weight(self):
        self.input_label.config(text="¿Qué importancia le das a la distancia? (0-10):")
        self.next_button.config(command=self.set_distance_weight)

    def set_distance_weight(self):
        try:
            distance_weight = int(self.input_field.get().strip())
            if 0 <= distance_weight <= 10:
                self.feature_weights["distance"] = distance_weight
                self.show_recommendations()
            else:
                messagebox.showerror("Error", "El peso debe estar entre 0 y 10.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido entre 0 y 10.")

    def show_recommendations(self):
        # Eliminar los resultados anteriores si existen
        if self.results_window:
            self.canvas.delete(self.results_window)

        # Crear un área para los nuevos resultados
        self.results_window = self.canvas.create_text(400, 300, text="Hemos encontrado estos coches para ti:", font=("Arial", 12), fill="white")

        # Cargar datos y modelos
        cars_df, ratings_df = load_data(cars_path, ratings_path)
        collaborative_model, _ = train_collaborative_model(ratings_path)
        geo_calculator = GeoDistanceCalculator()

        # Generar recomendaciones
        recommendations = hybrid_recommendation(
            user_id, self.user_input, self.feature_weights, self.user_location,
            geo_calculator, collaborative_model, cars_df
        )

        # Mostrar resultados
        top_5 = recommendations[['make', 'model', 'price', 'fuel', 'year', 'kms',
                                  'power', 'doors', 'shift', 'color', 'province',
                                  'distance']].head(5)

        y_position = 350
        for _, car in top_5.iterrows():
            car_info = f"{car['make']} {car['model']} - {car['price']}€ - {car['year']} - {car['fuel']} - {car['distance']} km"
            car_label = ttk.Label(self.root, text=car_info, font=("Arial", 10), background="white")
            car_label_window = self.canvas.create_window(400, y_position, window=car_label)
            y_position += 30

            # Cargar la imagen del coche
            image_name = f"{car['make']}_{car['model']}.jpg".replace(" ", "_")
            image_path = os.path.join(images_path, image_name)
            if os.path.exists(image_path):
                car_image = Image.open(image_path)
                car_image = car_image.resize((200, 150))  # Ajustar tamaño
                car_photo = ImageTk.PhotoImage(car_image)

                image_label = tk.Label(self.root, image=car_photo)
                image_label.image = car_photo  # Evitar que se elimine de memoria
                image_label_window = self.canvas.create_window(400, y_position, window=image_label)
                y_position += 160  # Ajustar la posición para la siguiente imagen

if __name__ == '__main__':
    root = tk.Tk()
    app = CarRecommenderApp(root)
    root.mainloop()
