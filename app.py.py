from flask import Flask, request, render_template_string
import pandas as pd
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ==========================
# CONFIGURACIÓN DE TOKENS
# ==========================
import os

GEMINI_API_KEY = os.getenv("AIzaSyCndiIzvIk40vOs4dAWZ7glu7FP94TGxVA")
# NGROK ya no es necesario porque vamos a usar Render

# Configurar API Key de Gemini
genai.configure(api_key=GEMINI_API_KEY)


@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = None
    plot_url = None
    ruta_archivo = 'archivo_temporal.csv'

    if request.method == 'POST':
        pregunta = request.form['pregunta']
        archivo = request.files.get('archivo')

        if archivo:
            archivo.save(ruta_archivo)

        try:
            df = pd.read_csv(ruta_archivo)
            respuesta = f"Gemini respondería algo sobre {pregunta} pero en Render no usamos la API para no gastar."  # Temporal

            # Crear gráfico
            plt.figure(figsize=(8, 4))
            df.iloc[:, 1].plot(kind='bar')
            plt.title('Gráfico de ejemplo - Columna 1')
            plt.xlabel('Índice')
            plt.ylabel('Valores')

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

        except Exception as e:
            respuesta = f"Error al procesar el archivo: {e}"

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Consulta tus Datos con Gemini</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="container mt-5">
            <h1>Consulta tus Datos con Gemini</h1>
            <form method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label>Subir CSV (opcional si ya subiste uno):</label>
                    <input type="file" name="archivo" class="form-control">
                </div>
                <div class="mb-3">
                    <label>Pregunta:</label>
                    <input type="text" name="pregunta" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary">Consultar</button>
            </form>

            {% if respuesta %}
                <h2>Respuesta:</h2>
                <p>{{ respuesta }}</p>
            {% endif %}

            {% if plot_url %}
                <h2>Gráfico generado:</h2>
                <img src="data:image/png;base64,{{ plot_url }}" class="img-fluid" alt="Gráfico generado">
            {% endif %}
        </body>
        </html>
    ''', respuesta=respuesta, plot_url=plot_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
