from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)
Flask(__name__)

# Asegúrate de que la ruta al archivo de base de datos sea correcta y accesible
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'database', 'super_any_memoria.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    platform = request.form['platform']
    conversation = request.form['conversation']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO any_memoria (plataforma, experiencias_resumen)
    VALUES (?, ?)
    ON CONFLICT(plataforma) DO UPDATE SET experiencias_resumen = experiencias_resumen || '\n' || excluded.experiencias_resumen
    ''', (platform, conversation))
    conn.commit()
    conn.close()

    return "Conversación guardada exitosamente."

@app.route('/historial')
def historial():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT plataforma, experiencias_resumen FROM any_memoria')
    conversaciones = cursor.fetchall()
    conn.close()
    return render_template('historial.html', conversaciones=conversaciones)

if __name__ == '__main__':
    app.run(debug=True)
