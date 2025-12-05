"""
Launcher de Any sin ventana de consola
Ejecuta: pythonw launch_any.pyw
"""

import subprocess
import sys
import os

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Ejecutar gui.py sin mostrar consola
if sys.platform == 'win32':
    # En Windows, usar pythonw para no mostrar consola
    subprocess.Popen(['pythonw', 'gui.py'])
else:
    # En otros sistemas
    subprocess.Popen(['python3', 'gui.py'])
