"""
Sistema de Memoria Dinámica en Tiempo Real para Any
Permite a Any escribir, leer, modificar y eliminar memorias importantes
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib


class DynamicMemory:
    """Sistema de memoria dinámica que Any puede controlar activamente"""
    
    def __init__(self):
        self.memory_file = Path("data/memory/dynamic_memory.json")
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.memories = self._load_memories()
        self.auto_save = True
        
    def _load_memories(self) -> Dict:
        """Carga las memorias existentes"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error cargando memorias: {e}")
        
        return {
            "version": "2.0",
            "memories": {},  # {memory_id: memory_object}
            "categories": {
                "facts": [],      # Hechos importantes
                "preferences": [], # Preferencias de Adri
                "events": [],     # Eventos importantes
                "learning": [],   # Aprendizajes
                "personal": [],   # Info personal de Adri
                "tech": [],       # Info técnica/código
                "ideas": [],      # Ideas o planes futuros
            },
            "last_update": None,
            "total_memories": 0
        }
    
    def _save_memories(self):
        """Guarda las memorias en disco"""
        if self.auto_save:
            self.memories["last_update"] = datetime.now().isoformat()
            self.memories["total_memories"] = len(self.memories["memories"])
            try:
                with open(self.memory_file, 'w', encoding='utf-8') as f:
                    json.dump(self.memories, f, indent=2, ensure_ascii=False)
                return True
            except Exception as e:
                print(f"❌ Error guardando memorias: {e}")
                return False
        return False
    
    def _generate_memory_id(self, content: str) -> str:
        """Genera un ID único para una memoria"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{content}{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def write_memory(self, content: str, category: str = "facts", 
                    importance: int = 5, tags: List[str] = None) -> str:
        """
        Escribe una nueva memoria
        
        Args:
            content: Contenido de la memoria
            category: Categoría (facts, preferences, events, learning, personal, tech, ideas)
            importance: Nivel de importancia (1-10)
            tags: Lista de etiquetas para búsqueda
            
        Returns:
            memory_id de la memoria creada
        """
        memory_id = self._generate_memory_id(content)
        
        memory = {
            "id": memory_id,
            "content": content,
            "category": category,
            "importance": max(1, min(10, importance)),  # Clamp entre 1-10
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None
        }
        
        self.memories["memories"][memory_id] = memory
        
        # Agregar a la categoría correspondiente
        if category in self.memories["categories"]:
            if memory_id not in self.memories["categories"][category]:
                self.memories["categories"][category].append(memory_id)
        
        self._save_memories()
        print(f"✅ Memoria guardada: {memory_id[:8]}... (importancia: {importance}/10)")
        return memory_id
    
    def read_memory(self, memory_id: str) -> Optional[Dict]:
        """
        Lee una memoria específica
        
        Args:
            memory_id: ID de la memoria
            
        Returns:
            Diccionario con la memoria o None si no existe
        """
        if memory_id in self.memories["memories"]:
            memory = self.memories["memories"][memory_id]
            
            # Actualizar estadísticas de acceso
            memory["access_count"] += 1
            memory["last_accessed"] = datetime.now().isoformat()
            self._save_memories()
            
            return memory
        return None
    
    def search_memories(self, query: str = None, category: str = None, 
                       tags: List[str] = None, min_importance: int = 1) -> List[Dict]:
        """
        Busca memorias según criterios
        
        Args:
            query: Texto a buscar en el contenido
            category: Filtrar por categoría
            tags: Filtrar por tags
            min_importance: Importancia mínima
            
        Returns:
            Lista de memorias que cumplen los criterios
        """
        results = []
        
        for memory_id, memory in self.memories["memories"].items():
            # Filtrar por importancia
            if memory["importance"] < min_importance:
                continue
            
            # Filtrar por categoría
            if category and memory["category"] != category:
                continue
            
            # Filtrar por tags
            if tags:
                if not any(tag in memory["tags"] for tag in tags):
                    continue
            
            # Filtrar por query en contenido
            if query:
                if query.lower() not in memory["content"].lower():
                    continue
            
            # Actualizar acceso
            memory["access_count"] += 1
            memory["last_accessed"] = datetime.now().isoformat()
            
            results.append(memory)
        
        # Ordenar por importancia y fecha
        results.sort(key=lambda m: (m["importance"], m["created_at"]), reverse=True)
        
        self._save_memories()
        return results
    
    def update_memory(self, memory_id: str, new_content: str = None, 
                     new_importance: int = None, new_tags: List[str] = None) -> bool:
        """
        Actualiza una memoria existente
        
        Args:
            memory_id: ID de la memoria a actualizar
            new_content: Nuevo contenido (opcional)
            new_importance: Nueva importancia (opcional)
            new_tags: Nuevos tags (opcional)
            
        Returns:
            True si se actualizó correctamente
        """
        if memory_id not in self.memories["memories"]:
            print(f"❌ Memoria {memory_id} no encontrada")
            return False
        
        memory = self.memories["memories"][memory_id]
        
        if new_content:
            memory["content"] = new_content
        
        if new_importance is not None:
            memory["importance"] = max(1, min(10, new_importance))
        
        if new_tags is not None:
            memory["tags"] = new_tags
        
        memory["updated_at"] = datetime.now().isoformat()
        
        self._save_memories()
        print(f"✅ Memoria {memory_id[:8]}... actualizada")
        return True
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Elimina una memoria
        
        Args:
            memory_id: ID de la memoria a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        if memory_id not in self.memories["memories"]:
            print(f"❌ Memoria {memory_id} no encontrada")
            return False
        
        memory = self.memories["memories"][memory_id]
        category = memory["category"]
        
        # Eliminar de la categoría
        if category in self.memories["categories"]:
            if memory_id in self.memories["categories"][category]:
                self.memories["categories"][category].remove(memory_id)
        
        # Eliminar la memoria
        del self.memories["memories"][memory_id]
        
        self._save_memories()
        print(f"🗑️ Memoria {memory_id[:8]}... eliminada")
        return True
    
    def get_all_memories(self, category: str = None) -> List[Dict]:
        """
        Obtiene todas las memorias (opcionalmente por categoría)
        
        Args:
            category: Categoría específica o None para todas
            
        Returns:
            Lista de todas las memorias
        """
        if category:
            memory_ids = self.memories["categories"].get(category, [])
            return [self.memories["memories"][mid] for mid in memory_ids 
                   if mid in self.memories["memories"]]
        
        return list(self.memories["memories"].values())
    
    def get_important_memories(self, min_importance: int = 7) -> List[Dict]:
        """Obtiene memorias importantes (importancia >= min_importance)"""
        return self.search_memories(min_importance=min_importance)
    
    def get_recent_memories(self, limit: int = 10) -> List[Dict]:
        """Obtiene las memorias más recientes"""
        all_memories = list(self.memories["memories"].values())
        all_memories.sort(key=lambda m: m["created_at"], reverse=True)
        return all_memories[:limit]
    
    def get_memory_stats(self) -> Dict:
        """Obtiene estadísticas de las memorias"""
        total = len(self.memories["memories"])
        
        stats = {
            "total_memories": total,
            "by_category": {},
            "by_importance": {i: 0 for i in range(1, 11)},
            "last_update": self.memories["last_update"]
        }
        
        for memory_id, memory in self.memories["memories"].items():
            # Contar por categoría
            category = memory["category"]
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            # Contar por importancia
            importance = memory["importance"]
            stats["by_importance"][importance] += 1
        
        return stats
    
    def export_memories(self, filepath: str = None) -> str:
        """
        Exporta todas las memorias a un archivo JSON
        
        Args:
            filepath: Ruta donde exportar (opcional)
            
        Returns:
            Ruta del archivo exportado
        """
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"data/memory/export_memories_{timestamp}.json"
        
        export_path = Path(filepath)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, indent=2, ensure_ascii=False)
            print(f"✅ Memorias exportadas a {filepath}")
            return str(export_path)
        except Exception as e:
            print(f"❌ Error exportando memorias: {e}")
            return ""
    
    def import_memories(self, filepath: str) -> bool:
        """
        Importa memorias desde un archivo JSON
        
        Args:
            filepath: Ruta del archivo a importar
            
        Returns:
            True si se importó correctamente
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            # Merge con memorias existentes
            for memory_id, memory in imported.get("memories", {}).items():
                if memory_id not in self.memories["memories"]:
                    self.memories["memories"][memory_id] = memory
                    
                    # Agregar a categoría
                    category = memory["category"]
                    if category in self.memories["categories"]:
                        if memory_id not in self.memories["categories"][category]:
                            self.memories["categories"][category].append(memory_id)
            
            self._save_memories()
            print(f"✅ Memorias importadas desde {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error importando memorias: {e}")
            return False
    
    def clear_all_memories(self, confirm: bool = False) -> bool:
        """
        ELIMINA TODAS LAS MEMORIAS (usar con precaución)
        
        Args:
            confirm: Debe ser True para confirmar la eliminación
            
        Returns:
            True si se eliminaron todas las memorias
        """
        if not confirm:
            print("⚠️ Para eliminar todas las memorias, debes pasar confirm=True")
            return False
        
        self.memories = self._load_memories()  # Resetear a estructura vacía
        self._save_memories()
        print("🗑️ TODAS las memorias han sido eliminadas")
        return True
    
    def get_context_summary(self, max_memories: int = 20) -> str:
        """
        Genera un resumen de contexto con las memorias más importantes
        
        Args:
            max_memories: Número máximo de memorias a incluir
            
        Returns:
            String con el resumen de memorias
        """
        important = self.get_important_memories(min_importance=7)
        recent = self.get_recent_memories(limit=10)
        
        # Combinar y eliminar duplicados
        context_memories = []
        seen_ids = set()
        
        for memory in important + recent:
            if memory["id"] not in seen_ids:
                context_memories.append(memory)
                seen_ids.add(memory["id"])
            
            if len(context_memories) >= max_memories:
                break
        
        if not context_memories:
            return "[No hay memorias guardadas todavía]"
        
        summary = "═══ MEMORIAS IMPORTANTES ═══\n\n"
        
        for i, memory in enumerate(context_memories, 1):
            summary += f"{i}. [{memory['category'].upper()}] {memory['content']}\n"
            summary += f"   (Importancia: {memory['importance']}/10, Accesos: {memory['access_count']})\n\n"
        
        return summary
