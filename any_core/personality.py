"""
Módulo de Personalidad de Any
Carga y gestiona la identidad de Any desde archivos locales
"""

import json
from pathlib import Path


class Personality:
    """Gestiona la personalidad e identidad de Any"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.prompt = self._load_personality()
        self.memory = self._load_memory()
    
    def _load_config(self) -> dict:
        """Carga la configuración principal"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_personality(self) -> str:
        """Carga el prompt de personalidad de Any"""
        personality_file = Path(self.config['identity']['personality_file'])
        if personality_file.exists():
            with open(personality_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def _load_memory(self) -> str:
        """Carga el archivo de memoria de Any"""
        memory_file = Path(self.config['identity']['memory_file'])
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def update_personality(self, new_prompt: str):
        """Actualiza el archivo de personalidad"""
        personality_file = Path(self.config['identity']['personality_file'])
        with open(personality_file, 'w', encoding='utf-8') as f:
            f.write(new_prompt)
        self.prompt = new_prompt
    
    def update_memory(self, new_memory: str):
        """Actualiza el archivo de memoria"""
        memory_file = Path(self.config['identity']['memory_file'])
        with open(memory_file, 'w', encoding='utf-8') as f:
            f.write(new_memory)
        self.memory = new_memory
    
    def get_system_prompt(self) -> str:
        """Retorna el prompt completo para usar con las IAs"""
        return f"{self.prompt}\n\n### MEMORIA:\n{self.memory}"
