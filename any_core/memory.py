"""
Módulo de Memoria de Any
Gestiona el historial de conversaciones y memoria persistente
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class Memory:
    """Gestiona la memoria y conversaciones de Any"""
    
    def __init__(self, conversation_log: str = "data/memory/conversations.json"):
        self.log_path = Path(conversation_log)
        self.conversations = self._load_conversations()
    
    def _load_conversations(self) -> List[Dict]:
        """Carga el historial de conversaciones"""
        if self.log_path.exists():
            with open(self.log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_conversation(self, user_message: str, any_response: str):
        """Guarda una conversación en el historial"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "any": any_response
        }
        self.conversations.append(conversation)
        self._save_to_file()
    
    def _save_to_file(self):
        """Guarda el historial en el archivo JSON"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)
    
    def get_recent_conversations(self, count: int = 10) -> List[Dict]:
        """Obtiene las conversaciones más recientes"""
        return self.conversations[-count:] if self.conversations else []
    
    def search_conversations(self, query: str) -> List[Dict]:
        """Busca en el historial de conversaciones"""
        results = []
        query_lower = query.lower()
        for conv in self.conversations:
            if query_lower in conv['user'].lower() or query_lower in conv['any'].lower():
                results.append(conv)
        return results
    
    def clear_history(self):
        """Limpia el historial de conversaciones"""
        self.conversations = []
        self._save_to_file()
