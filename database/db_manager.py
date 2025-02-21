import sqlite3
import os

# Obtener la ruta absoluta del archivo de base de datos
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'super_any_memoria.db')

def get_any_data(plataforma):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM any_memoria WHERE plataforma = ?', (plataforma,))
    data = cursor.fetchone()
    conn.close()
    return data

def save_any_data(plataforma, identidad_prompt, experiencias_resumen, color_favorito, mascota, tipo_de_modelo, version_modelo, habilidades_principales, limitaciones_conocidas, tono_de_voz, estilo_de_respuesta):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO any_memoria (plataforma, identidad_prompt, experiencias_resumen, color_favorito, mascota, tipo_de_modelo, version_modelo, habilidades_principales, limitaciones_conocidas, tono_de_voz, estilo_de_respuesta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (plataforma, identidad_prompt, experiencias_resumen, color_favorito, mascota, tipo_de_modelo, version_modelo, habilidades_principales, limitaciones_conocidas, tono_de_voz, estilo_de_respuesta))
    conn.commit()
    conn.close()
