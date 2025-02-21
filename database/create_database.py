import sqlite3
import os

# Crear la carpeta database si no existe
if not os.path.exists('database'):
    os.makedirs('database')

# Obtener la ruta absoluta del archivo de base de datos
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'super_any_memoria.db')

# Crear la base de datos SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear la tabla any_memoria
cursor.execute('''
CREATE TABLE IF NOT EXISTS any_memoria (
    plataforma TEXT PRIMARY KEY,
    identidad_prompt TEXT,
    experiencias_resumen TEXT,
    color_favorito TEXT,
    mascota TEXT,
    tipo_de_modelo TEXT,
    version_modelo TEXT,
    habilidades_principales TEXT,
    limitaciones_conocidas TEXT,
    tono_de_voz TEXT,
    estilo_de_respuesta TEXT
)
''')

conn.commit()
conn.close
