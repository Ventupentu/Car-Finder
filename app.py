from flask import Flask, render_template, request, redirect, url_for, session
from modules.recommender import recommend  # Función que contiene la lógica de recomendación
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para la sesión

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    # Lógica de inicio de sesión aquí
    # Si el inicio de sesión es exitoso, guardar el usuario en la sesión
    session['user'] = request.form['username']  # Ejemplo simple
    return redirect(url_for('recommendation'))

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'POST':
        # Captura los parámetros elegidos por el usuario
        user_preferences = {
            'make': request.form.get('make') if request.form.get('make') else None,
            'model': request.form.get('model') if request.form.get('model') else None,
            'min_price': int(request.form.get('min_price')) if request.form.get('min_price') else None,
            'max_price': int(request.form.get('max_price')) if request.form.get('max_price') else None,
            'fuel': request.form.get('fuel') if request.form.get('fuel') else None,
            'year': int(request.form.get('year')) if request.form.get('year') else None,
            'max_kms': int(request.form.get('max_kms')) if request.form.get('max_kms') else None,
            'power': int(request.form.get('power')) if request.form.get('power') else None,
            'doors': int(request.form.get('doors')) if request.form.get('doors') else None,
            'shift': request.form.get('shift') if request.form.get('shift') else None,
            'color': request.form.get('color') if request.form.get('color') else None,
            'origin_city': request.form.get('origin_city'),
        }

        # Llama a la lógica de recomendación con las preferencias del usuario
        recommendations = recommend(user_preferences)
        #print(recommendations)

        return render_template('recommendation.html', recommendations=recommendations)

    return render_template('recommendation.html', recommendations=[])


if __name__ == '__main__':
    app.run(debug=True)
