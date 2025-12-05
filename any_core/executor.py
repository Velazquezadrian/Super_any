"""
Módulo Executor de Any
Permite a Any ejecutar comandos y acciones en el sistema
"""

import subprocess
import os
from pathlib import Path
from typing import Tuple


class Executor:
    """Ejecuta comandos y acciones en el sistema"""
    
    def __init__(self, permissions: dict):
        self.can_execute = permissions.get('can_execute_commands', False)
        self.can_modify_files = permissions.get('can_modify_files', False)
        self.can_self_update = permissions.get('can_self_update', False)
    
    def execute_command(self, command: str) -> Tuple[bool, str]:
        """
        Ejecuta un comando en el sistema
        
        Args:
            command: Comando a ejecutar
        
        Returns:
            Tuple[bool, str]: (éxito, resultado/error)
        """
        if not self.can_execute:
            return False, "Permisos insuficientes para ejecutar comandos"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout if result.returncode == 0 else result.stderr
            return result.returncode == 0, output
        except Exception as e:
            return False, f"Error al ejecutar comando: {str(e)}"
    
    def read_file(self, file_path: str) -> Tuple[bool, str]:
        """Lee un archivo del sistema"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False, f"Archivo no encontrado: {file_path}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return True, content
        except Exception as e:
            return False, f"Error al leer archivo: {str(e)}"
    
    def write_file(self, file_path: str, content: str) -> Tuple[bool, str]:
        """Escribe contenido en un archivo"""
        if not self.can_modify_files:
            return False, "Permisos insuficientes para modificar archivos"
        
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"Archivo guardado: {file_path}"
        except Exception as e:
            return False, f"Error al escribir archivo: {str(e)}"
    
    def list_directory(self, directory: str = ".") -> Tuple[bool, str]:
        """Lista el contenido de un directorio"""
        try:
            path = Path(directory)
            if not path.exists():
                return False, f"Directorio no encontrado: {directory}"
            
            items = []
            for item in path.iterdir():
                prefix = "[DIR]" if item.is_dir() else "[FILE]"
                items.append(f"{prefix} {item.name}")
            
            return True, "\n".join(items)
        except Exception as e:
            return False, f"Error al listar directorio: {str(e)}"
