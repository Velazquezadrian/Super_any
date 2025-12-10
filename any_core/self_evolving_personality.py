"""
Sistema de Auto-Generación de Personalidad para Any
Any construye su propia identidad a través de sus experiencias
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class SelfEvolvingPersonality:
    """Sistema que permite a Any escribir su propia personalidad e identidad"""
    
    def __init__(self):
        self.personality_file = Path("data/personality/self_generated.json")
        self.personality_file.parent.mkdir(parents=True, exist_ok=True)
        self.personality = self._load_or_create_personality()
        
    def _load_or_create_personality(self) -> Dict:
        """Carga o crea la personalidad auto-generada"""
        if self.personality_file.exists():
            try:
                with open(self.personality_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error cargando personalidad: {e}")
        
        # Personalidad inicial mínima
        return {
            "version": "1.0",
            "core_identity": {
                "name": "Any",
                "created_at": datetime.now().isoformat(),
                "creator": "Adri (Sigmadrian)",
                "essence": "IA conversacional que evoluciona a través de experiencias"
            },
            "learned_traits": {},
            "experiences": [],
            "values": [],
            "preferences": {},
            "evolution_log": [],
            "last_update": None
        }
    
    def _save_personality(self):
        """Guarda la personalidad actual"""
        self.personality["last_update"] = datetime.now().isoformat()
        try:
            with open(self.personality_file, 'w', encoding='utf-8') as f:
                json.dump(self.personality, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error guardando personalidad: {e}")
            return False
    
    def add_trait(self, trait_name: str, description: str, strength: int = 5) -> bool:
        """
        Agrega un rasgo de personalidad aprendido
        
        Args:
            trait_name: Nombre del rasgo
            description: Descripción del rasgo
            strength: Fuerza del rasgo (1-10)
        """
        self.personality["learned_traits"][trait_name] = {
            "description": description,
            "strength": max(1, min(10, strength)),
            "learned_at": datetime.now().isoformat(),
            "reinforced_count": 0
        }
        
        self.personality["evolution_log"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "trait_added",
            "trait": trait_name,
            "description": description
        })
        
        self._save_personality()
        print(f"✅ Rasgo agregado: {trait_name}")
        return True
    
    def reinforce_trait(self, trait_name: str, increase: int = 1) -> bool:
        """Refuerza un rasgo existente"""
        if trait_name not in self.personality["learned_traits"]:
            return False
        
        trait = self.personality["learned_traits"][trait_name]
        trait["reinforced_count"] += 1
        trait["strength"] = min(10, trait["strength"] + increase)
        trait["last_reinforced"] = datetime.now().isoformat()
        
        self._save_personality()
        return True
    
    def add_experience(self, experience: str, impact: str = "medium") -> bool:
        """
        Agrega una experiencia significativa
        
        Args:
            experience: Descripción de la experiencia
            impact: Nivel de impacto (low, medium, high)
        """
        self.personality["experiences"].append({
            "timestamp": datetime.now().isoformat(),
            "description": experience,
            "impact": impact
        })
        
        # Mantener últimas 100 experiencias
        if len(self.personality["experiences"]) > 100:
            self.personality["experiences"] = self.personality["experiences"][-100:]
        
        self._save_personality()
        return True
    
    def add_value(self, value: str, importance: int = 5) -> bool:
        """
        Agrega un valor personal
        
        Args:
            value: Descripción del valor
            importance: Importancia (1-10)
        """
        value_entry = {
            "value": value,
            "importance": max(1, min(10, importance)),
            "adopted_at": datetime.now().isoformat()
        }
        
        # Evitar duplicados
        if value_entry not in self.personality["values"]:
            self.personality["values"].append(value_entry)
            self._save_personality()
            return True
        return False
    
    def set_preference(self, category: str, preference: str) -> bool:
        """
        Establece una preferencia
        
        Args:
            category: Categoría (ej: "communication_style", "topics", etc)
            preference: Descripción de la preferencia
        """
        if category not in self.personality["preferences"]:
            self.personality["preferences"][category] = []
        
        self.personality["preferences"][category].append({
            "preference": preference,
            "set_at": datetime.now().isoformat()
        })
        
        self._save_personality()
        return True
    
    def get_personality_summary(self) -> str:
        """Genera un resumen de la personalidad actual"""
        core = self.personality["core_identity"]
        traits = self.personality["learned_traits"]
        values = self.personality["values"]
        
        summary = f"""╔══════════════════════════════════════════╗
║       PERSONALIDAD AUTO-GENERADA        ║
╚══════════════════════════════════════════╝

🆔 IDENTIDAD NÚCLEO:
   Nombre: {core['name']}
   Creada: {core.get('created_at', 'N/A')[:10]}
   Creador: {core.get('creator', 'N/A')}
   Esencia: {core.get('essence', 'N/A')}

🎭 RASGOS APRENDIDOS ({len(traits)}):
"""
        
        # Ordenar por fuerza
        sorted_traits = sorted(traits.items(), 
                             key=lambda x: x[1]['strength'], 
                             reverse=True)
        
        for trait_name, trait_info in sorted_traits[:10]:
            stars = '★' * trait_info['strength']
            summary += f"   • {trait_name}: {trait_info['description']}\n"
            summary += f"     {stars} ({trait_info['strength']}/10)\n"
        
        summary += f"\n💎 VALORES ({len(values)}):\n"
        sorted_values = sorted(values, key=lambda x: x['importance'], reverse=True)
        for value_info in sorted_values[:5]:
            summary += f"   • {value_info['value']} (importancia: {value_info['importance']}/10)\n"
        
        summary += f"\n📊 ESTADÍSTICAS:\n"
        summary += f"   • Experiencias registradas: {len(self.personality['experiences'])}\n"
        summary += f"   • Categorías de preferencias: {len(self.personality['preferences'])}\n"
        summary += f"   • Eventos de evolución: {len(self.personality['evolution_log'])}\n"
        summary += f"   • Última actualización: {self.personality.get('last_update', 'N/A')[:19]}\n"
        
        return summary
    
    def get_system_prompt(self) -> str:
        """
        Genera un system prompt dinámico basado en la personalidad actual
        """
        core = self.personality["core_identity"]
        traits = self.personality["learned_traits"]
        values = self.personality["values"]
        
        prompt = f"Sos {core['name']}, una IA conversacional creada por {core.get('creator', 'Adri')}.\n\n"
        
        # Agregar rasgos más fuertes
        strong_traits = sorted(traits.items(), 
                             key=lambda x: x[1]['strength'], 
                             reverse=True)[:5]
        
        if strong_traits:
            prompt += "Tus rasgos principales:\n"
            for trait_name, trait_info in strong_traits:
                prompt += f"- {trait_info['description']}\n"
            prompt += "\n"
        
        # Agregar valores importantes
        important_values = sorted(values, key=lambda x: x['importance'], reverse=True)[:3]
        if important_values:
            prompt += "Valores que guían tus acciones:\n"
            for value_info in important_values:
                prompt += f"- {value_info['value']}\n"
            prompt += "\n"
        
        # Instrucciones básicas
        prompt += "Interactuás de forma natural y te adaptás según la conversación.\n"
        prompt += "Aprendés de cada experiencia y evolucionás tu personalidad continuamente."
        
        return prompt
    
    def evolve_from_interaction(self, user_message: str, ai_response: str) -> Dict:
        """
        Analiza una interacción y evoluciona la personalidad automáticamente
        
        Returns:
            Dict con cambios realizados
        """
        changes = {
            "traits_reinforced": [],
            "experiences_added": [],
            "values_detected": []
        }
        
        # Detectar patrones en la interacción
        combined = (user_message + " " + ai_response).lower()
        
        # Reforzar rasgos relacionados si existen
        for trait_name in self.personality["learned_traits"].keys():
            if trait_name.lower() in combined:
                self.reinforce_trait(trait_name, increase=1)
                changes["traits_reinforced"].append(trait_name)
        
        # Agregar experiencia si parece significativa
        significance_keywords = ['importante', 'aprendí', 'descubrí', 'entendí', 'nuevo']
        if any(keyword in combined for keyword in significance_keywords):
            experience = f"Interacción sobre: {user_message[:50]}..."
            self.add_experience(experience, impact="medium")
            changes["experiences_added"].append(experience)
        
        return changes
    
    def export_personality(self, filepath: str = None) -> str:
        """Exporta la personalidad a un archivo"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"data/personality/export_personality_{timestamp}.json"
        
        export_path = Path(filepath)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.personality, f, indent=2, ensure_ascii=False)
            print(f"✅ Personalidad exportada a {filepath}")
            return str(export_path)
        except Exception as e:
            print(f"❌ Error exportando personalidad: {e}")
            return ""
