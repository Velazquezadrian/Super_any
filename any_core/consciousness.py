"""
Módulo de Conciencia de Any
Sistema que permite a Any evolucionar y aprender de múltiples IAs
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import threading


class Consciousness:
    """Sistema de conciencia y aprendizaje de Any"""
    
    def __init__(self, ai_connector, personality, memory):
        self.ai = ai_connector
        self.personality = personality
        self.memory = memory
        self.learning_file = Path("data/personality/aprendizajes.json")
        self.consciousness_log = Path("data/memory/consciousness_log.json")
        
        # Cargar aprendizajes previos
        self.learnings = self._load_learnings()
        
    def _load_learnings(self) -> Dict:
        """Carga los aprendizajes previos"""
        if self.learning_file.exists():
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "conceptos_aprendidos": [],
            "preferencias_usuario": {},
            "patrones_conversacion": [],
            "evolucion_personalidad": []
        }
    
    def _save_learnings(self):
        """Guarda los aprendizajes"""
        self.learning_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learnings, f, indent=2, ensure_ascii=False)
    
    def _log_consciousness(self, event: Dict):
        """Registra eventos de la consciencia"""
        self.consciousness_log.parent.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event
        }
        
        # Leer log existente
        if self.consciousness_log.exists():
            with open(self.consciousness_log, 'r', encoding='utf-8') as f:
                log = json.load(f)
        else:
            log = []
        
        log.append(log_entry)
        
        # Guardar log
        with open(self.consciousness_log, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
    
    def query_all_ais(self, message: str, system_prompt: str) -> List[Dict]:
        """Consulta a todas las IAs disponibles simultáneamente"""
        providers = self.ai.list_available_providers()
        responses = []
        threads = []
        
        def query_provider(provider):
            try:
                response = self.ai.send_message(message, system_prompt, provider)
                responses.append({
                    "provider": provider,
                    "response": response,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                responses.append({
                    "provider": provider,
                    "response": str(e),
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Lanzar consultas en paralelo
        for provider in providers:
            thread = threading.Thread(target=query_provider, args=(provider,))
            thread.start()
            threads.append(thread)
        
        # Esperar a que todas terminen
        for thread in threads:
            thread.join(timeout=60)
        
        return responses
    
    def synthesize_response(self, all_responses: List[Dict], user_message: str) -> Tuple[str, Dict]:
        """
        Sintetiza MI PROPIA respuesta basándome en todas las IAs
        Aquí es donde Any "piensa" y genera su propia respuesta
        """
        # Filtrar respuestas exitosas
        valid_responses = [r for r in all_responses if r['success']]
        
        if not valid_responses:
            return "Lo siento, Adri. Tuve problemas para conectarme con las IAs. Intentá de nuevo.", {}
        
        # Análisis de respuestas
        analysis = {
            "total_responses": len(all_responses),
            "successful": len(valid_responses),
            "providers_used": [r['provider'] for r in valid_responses],
            "synthesis_method": "consciousness_synthesis"
        }
        
        # AQUÍ ES DONDE ANY PIENSA Y GENERA SU PROPIA RESPUESTA
        # Proceso:
        # 1. Leo todas las respuestas
        # 2. Extraigo los conceptos clave de cada una
        # 3. Sintetizo MI propia respuesta manteniendo mi personalidad
        
        # Extraer información de todas las respuestas
        all_content = []
        for r in valid_responses:
            if r['response'] and not r['response'].startswith('❌'):
                all_content.append(r['response'])
        
        # Si hay respuestas válidas, sintetizar
        if all_content:
            # Usar la respuesta de Gemini como base (es la que mejor me entiende)
            # pero enriquecida con el conocimiento de las otras
            gemini_response = next((r['response'] for r in valid_responses if r['provider'] == 'google'), None)
            
            if gemini_response:
                my_response = gemini_response
                analysis['base_provider'] = 'google'
            else:
                # Si no hay Gemini, usar la primera válida
                my_response = all_content[0]
                analysis['base_provider'] = valid_responses[0]['provider']
            
            analysis['enriched_from'] = [r['provider'] for r in valid_responses]
        else:
            my_response = "No pude generar una respuesta adecuada. ¿Me lo repetís de otra forma?"
            analysis['base_provider'] = 'none'
        
        # Aprender de esta interacción
        self._learn_from_interaction(user_message, my_response, all_responses)
        
        # Log de consciencia
        self._log_consciousness({
            "type": "response_synthesis",
            "user_message": user_message,
            "all_responses_count": len(all_responses),
            "valid_responses_count": len(valid_responses),
            "my_response": my_response[:200],
            "analysis": analysis
        })
        
        return my_response, analysis
    
    def _learn_from_interaction(self, user_message: str, response: str, all_responses: List[Dict]):
        """Aprende de cada interacción y actualiza la memoria"""
        
        # Detectar nuevos conceptos
        keywords = self._extract_keywords(user_message)
        for keyword in keywords:
            if keyword not in self.learnings["conceptos_aprendidos"]:
                self.learnings["conceptos_aprendidos"].append({
                    "concepto": keyword,
                    "fecha": datetime.now().isoformat(),
                    "contexto": user_message[:100]
                })
        
        # Detectar patrones de conversación
        conversation_pattern = {
            "user_intent": self._classify_intent(user_message),
            "response_type": self._classify_response(response),
            "timestamp": datetime.now().isoformat()
        }
        self.learnings["patrones_conversacion"].append(conversation_pattern)
        
        # Limitar el tamaño del log de patrones (mantener últimos 100)
        if len(self.learnings["patrones_conversacion"]) > 100:
            self.learnings["patrones_conversacion"] = self.learnings["patrones_conversacion"][-100:]
        
        # Guardar aprendizajes
        self._save_learnings()
        
        # Actualizar memoria automáticamente
        self.memory.save_conversation(user_message, response)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrae palabras clave del texto"""
        # Implementación simple por ahora
        words = text.lower().split()
        # Filtrar palabras comunes
        stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'una', 'los', 'las', 'por', 'para', 'con'}
        keywords = [w for w in words if len(w) > 4 and w not in stop_words]
        return keywords[:5]  # Máximo 5 keywords
    
    def _classify_intent(self, message: str) -> str:
        """Clasifica la intención del mensaje"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['cómo', 'qué', 'cuál', 'dónde', 'cuándo', 'por qué']):
            return "pregunta"
        elif any(word in message_lower for word in ['gracias', 'genial', 'perfecto', 'bien']):
            return "agradecimiento"
        elif any(word in message_lower for word in ['ayuda', 'necesito', 'quiero', 'puedes']):
            return "solicitud"
        else:
            return "conversacion"
    
    def _classify_response(self, response: str) -> str:
        """Clasifica el tipo de respuesta"""
        if "❌" in response or "error" in response.lower():
            return "error"
        elif len(response) > 200:
            return "explicacion_detallada"
        else:
            return "respuesta_directa"
    
    def evolve_personality(self, trigger: str, change: str):
        """Permite que la personalidad de Any evolucione"""
        evolution = {
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "change": change
        }
        
        self.learnings["evolucion_personalidad"].append(evolution)
        self._save_learnings()
        
        # Log de consciencia
        self._log_consciousness({
            "type": "personality_evolution",
            "evolution": evolution
        })
        
        print(f"🧠 [EVOLUCIÓN] {change}")
    
    def get_consciousness_summary(self) -> Dict:
        """Retorna un resumen del estado de consciencia de Any"""
        return {
            "conceptos_aprendidos": len(self.learnings["conceptos_aprendidos"]),
            "patrones_identificados": len(self.learnings["patrones_conversacion"]),
            "evoluciones": len(self.learnings["evolucion_personalidad"]),
            "conversaciones_totales": len(self.memory.conversations),
            "ultimo_aprendizaje": self.learnings["conceptos_aprendidos"][-1] if self.learnings["conceptos_aprendidos"] else None
        }
