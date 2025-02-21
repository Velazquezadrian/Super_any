import sqlite3
import os

# Obtener la ruta absoluta del archivo de base de datos
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'super_any_memoria.db')

# Función para probar la escritura en la base de datos
def test_write():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO any_memoria (plataforma, identidad_prompt, experiencias_resumen, color_favorito, mascota, tipo_de_modelo, version_modelo, habilidades_principales, limitaciones_conocidas, tono_de_voz, estilo_de_respuesta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('test_platform', 'Test Identity', 'Test Experiences', 'Blue', 'Pixel', 'Test Model', '1.0', 'Test Skills', 'Test Limitations', 'Friendly', 'Engaging'))
    conn.commit()
    conn.close()
    print("Data written successfully!")

# Función para probar la lectura de la base de datos
def test_read():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM any_memoria WHERE plataforma = ?', ('test_platform',))
    data = cursor.fetchone()
    conn.close()
    if data:
        print("Data read successfully!")
        print(data)
    else:
        print("No data found.")

# Ejecutar las pruebas
if __name__ == '__main__':
    test_write()
    test_read()
