"""
Sistema de Compresión de Memoria de Any
Genera resúmenes ultra-compactos que solo la IA entiende
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class MemoryCompression:
    """Sistema de memoria comprimida para Any"""
    
    def __init__(self):
        self.compressed_file = Path("data/memory/memory_compressed.json")
        self.compressed_file.parent.mkdir(parents=True, exist_ok=True)
        self.memory = self._load_compressed_memory()
        
    def _load_compressed_memory(self) -> Dict:
        """Carga la memoria comprimida"""
        if self.compressed_file.exists():
            try:
                with open(self.compressed_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "version": "1.0",
            "context_tokens": [],  # Lista de tokens de contexto ultra-compactos
            "key_facts": {},       # Hechos clave por categoría
            "preferences": {},     # Preferencias del usuario
            "relationships": {},   # Relaciones entre conceptos
            "last_update": None
        }
    
    def _save_compressed_memory(self):
        """Guarda la memoria comprimida"""
        self.memory["last_update"] = datetime.now().isoformat()
        with open(self.compressed_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def compress_conversation(self, user_message: str, assistant_response: str) -> str:
        """
        Comprime una conversación a un token ultra-compacto
        Formato: categoria|concepto_clave|detalles_minimos|timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d")
        
        # Detectar categoría
        category = self._detect_category(user_message, assistant_response)
        
        # Extraer conceptos clave (máximo 5 palabras)
        key_concepts = self._extract_key_concepts(user_message, assistant_response)
        
        # Extraer detalles mínimos (máximo 10 palabras)
        details = self._extract_minimal_details(user_message, assistant_response)
        
        # Crear token comprimido
        token = f"{category}|{key_concepts}|{details}|{timestamp}"
        
        # Agregar a memoria
        self.memory["context_tokens"].append(token)
        
        # Mantener solo últimos 100 tokens para mantenerlo liviano
        if len(self.memory["context_tokens"]) > 100:
            self.memory["context_tokens"] = self.memory["context_tokens"][-100:]
        
        self._save_compressed_memory()
        return token
    
    def _detect_category(self, user_msg: str, ai_msg: str) -> str:
        """Detecta la categoría de la conversación"""
        combined = (user_msg + " " + ai_msg).lower()
        
        # Categorías ultra-compactas (2-3 letras)
        if any(word in combined for word in ['código', 'code', 'programa', 'función', 'class', 'bug']):
            return "cod"  # coding
        elif any(word in combined for word in ['ia', 'modelo', 'provider', 'gemini', 'gpt']):
            return "ais"  # ai systems
        elif any(word in combined for word in ['memoria', 'recordar', 'guardar', 'aprendizaje']):
            return "mem"  # memory
        elif any(word in combined for word in ['voz', 'hablar', 'escuchar', 'tts', 'stt']):
            return "voc"  # voice
        elif any(word in combined for word in ['visión', 'pantalla', 'captura', 'ver', 'screenshot']):
            return "vis"  # vision
        elif any(word in combined for word in ['preferencia', 'gustar', 'quiero', 'prefiero']):
            return "prf"  # preference
        elif any(word in combined for word in ['proyecto', 'app', 'crear', 'hacer']):
            return "prj"  # project
        else:
            return "gen"  # general
    
    def _extract_key_concepts(self, user_msg: str, ai_msg: str) -> str:
        """Extrae conceptos clave (máximo 5 palabras)"""
        combined = user_msg + " " + ai_msg
        
        # Palabras clave importantes (nombres propios, tecnologías, acciones)
        important_words = []
        
        words = combined.lower().split()
        keywords = [
            'any', 'gemini', 'groq', 'deepseek', 'python', 'gui', 'vision', 
            'voice', 'memoria', 'asi', 'consciencia', 'análisis', 'auto',
            'perplexity', 'cohere', 'huggingface', 'rosario', 'argentina'
        ]
        
        for word in words:
            # Limpiar puntuación
            clean_word = ''.join(c for c in word if c.isalnum() or c == '-')
            if clean_word in keywords:
                important_words.append(clean_word)
                if len(important_words) >= 5:
                    break
        
        # Si no hay keywords específicas, tomar primeras palabras relevantes
        if not important_words:
            relevant = [w for w in words if len(w) > 4 and w.isalpha()][:3]
            important_words = relevant
        
        return " ".join(important_words[:5])
    
    def _extract_minimal_details(self, user_msg: str, ai_msg: str) -> str:
        """Extrae detalles mínimos (máximo 10 palabras)"""
        # Intentar extraer lo más importante del mensaje del usuario
        words = user_msg.lower().split()
        
        # Filtrar palabras comunes
        stop_words = {'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'que', 'en', 
                     'y', 'a', 'para', 'con', 'por', 'es', 'esta', 'este', 'como',
                     'qué', 'cómo', 'cuál', 'cuándo', 'dónde'}
        
        relevant_words = [w for w in words if w not in stop_words and len(w) > 2][:10]
        
        return " ".join(relevant_words)
    
    def add_key_fact(self, category: str, key: str, value: str):
        """Agrega un hecho clave a la memoria"""
        if category not in self.memory["key_facts"]:
            self.memory["key_facts"][category] = {}
        
        self.memory["key_facts"][category][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_compressed_memory()
    
    def add_preference(self, preference_key: str, value: str):
        """Agrega una preferencia del usuario"""
        self.memory["preferences"][preference_key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_compressed_memory()
    
    def add_relationship(self, concept_a: str, concept_b: str, relation_type: str):
        """Registra relación entre conceptos"""
        rel_key = f"{concept_a}-{concept_b}"
        self.memory["relationships"][rel_key] = {
            "type": relation_type,
            "timestamp": datetime.now().isoformat()
        }
        self._save_compressed_memory()
    
    def get_context_summary(self, max_tokens: int = 20) -> str:
        """
        Genera un resumen ultra-compacto del contexto reciente
        Para insertar en prompts sin ocupar muchos tokens
        """
        if not self.memory["context_tokens"]:
            return ""
        
        # Tomar últimos N tokens
        recent_tokens = self.memory["context_tokens"][-max_tokens:]
        
        # Agrupar por categoría
        by_category = {}
        for token in recent_tokens:
            parts = token.split("|")
            if len(parts) >= 3:
                cat, concepts, details, _ = parts[0], parts[1], parts[2], parts[3] if len(parts) > 3 else ""
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(f"{concepts}")
        
        # Construir resumen
        summary_parts = []
        for cat, items in by_category.items():
            unique_items = list(set(items))[:3]  # Max 3 por categoría
            summary_parts.append(f"{cat}:{','.join(unique_items)}")
        
        return " | ".join(summary_parts)
    
    def get_full_context(self) -> str:
        """Genera contexto completo para el prompt de la IA"""
        if not any([self.memory["context_tokens"], self.memory["key_facts"], self.memory["preferences"]]):
            return ""
        
        context_parts = []
        context_parts.append("=== MEMORIA DE CONVERSACIONES ANTERIORES ===")
        
        # Hechos clave por categoría (MÁS IMPORTANTE PRIMERO)
        if self.memory["key_facts"]:
            context_parts.append("\n📌 HECHOS IMPORTANTES:")
            for cat, facts in self.memory["key_facts"].items():
                cat_name = {
                    "usuario": "Usuario",
                    "ias": "IAs configuradas",
                    "proyectos": "Proyectos",
                    "tecnologias": "Tecnologías",
                    "tareas": "Tareas pendientes",
                    "problemas": "Problemas recientes",
                    "contexto": "Contexto"
                }.get(cat, cat)
                
                for key, data in list(facts.items())[:5]:  # Max 5 por categoría
                    context_parts.append(f"  • {cat_name} - {key}: {data['value']}")
        
        # Preferencias del usuario
        if self.memory["preferences"]:
            context_parts.append("\n❤️ PREFERENCIAS DEL USUARIO:")
            for key, data in list(self.memory["preferences"].items())[:8]:
                # Limpiar el key
                clean_key = key.replace("pref_", "").replace("_", " ")
                context_parts.append(f"  • {clean_key}: {data['value'][:100]}")
        
        # Resumen de conversaciones recientes
        if self.memory["context_tokens"]:
            recent_tokens = self.memory["context_tokens"][-10:]  # Últimos 10
            if recent_tokens:
                context_parts.append("\n💭 TEMAS RECIENTES:")
                for token in recent_tokens[-5:]:  # Mostrar últimos 5
                    parts = token.split("|")
                    if len(parts) >= 3:
                        cat, concepts, details = parts[0], parts[1], parts[2]
                        cat_name = {
                            "cod": "Programación",
                            "ais": "IAs",
                            "mem": "Memoria",
                            "voc": "Voz",
                            "vis": "Visión",
                            "prf": "Preferencias",
                            "prj": "Proyecto",
                            "gen": "General"
                        }.get(cat, cat)
                        context_parts.append(f"  • {cat_name}: {concepts} - {details[:50]}")
        
        context_parts.append("\n" + "="*45)
        
        return "\n".join(context_parts)
    
    def get_memory_stats(self) -> Dict:
        """Obtiene estadísticas de la memoria comprimida"""
        import sys
        
        # Calcular tamaño del archivo
        file_size = 0
        if self.compressed_file.exists():
            file_size = self.compressed_file.stat().st_size
        
        return {
            "total_tokens": len(self.memory["context_tokens"]),
            "key_facts_count": sum(len(facts) for facts in self.memory["key_facts"].values()),
            "preferences_count": len(self.memory["preferences"]),
            "relationships_count": len(self.memory["relationships"]),
            "file_size_bytes": file_size,
            "file_size_kb": round(file_size / 1024, 2),
            "last_update": self.memory.get("last_update", "Never")
        }
    
    def search_context(self, query: str) -> List[str]:
        """Busca en el contexto comprimido"""
        query_lower = query.lower()
        results = []
        
        for token in self.memory["context_tokens"]:
            if query_lower in token.lower():
                results.append(token)
        
        return results[-10:]  # Últimos 10 matches
    
    def clear_old_context(self, days: int = 30):
        """Limpia contexto más antiguo de N días"""
        from datetime import timedelta
        
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        
        # Filtrar tokens por fecha
        self.memory["context_tokens"] = [
            token for token in self.memory["context_tokens"]
            if len(token.split("|")) >= 4 and token.split("|")[3] >= cutoff_date
        ]
        
        self._save_compressed_memory()
        return len(self.memory["context_tokens"])
