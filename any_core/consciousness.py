"""
Módulo de Conciencia de Any
Sistema que permite a Any evolucionar y aprender de múltiples IAs
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import threading
from any_core.self_analysis import SelfAnalysis
from any_core.memory_compression import MemoryCompression


class Consciousness:
    """Sistema de conciencia y aprendizaje de Any"""
    
    def __init__(self, ai_connector, personality, memory):
        self.ai = ai_connector
        self.personality = personality
        self.memory = memory
        self.learning_file = Path("data/personality/aprendizajes.json")
        self.consciousness_log = Path("data/memory/consciousness_log.json")
        
        # Sistema de auto-análisis
        self.self_analysis = SelfAnalysis()
        
        # Sistema de memoria comprimida
        self.compressed_memory = MemoryCompression()
        
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
        # Enriquecer mensaje con auto-conocimiento si es necesario
        enriched_message = self.enrich_with_self_knowledge(message)
        
        # Agregar contexto comprimido al system prompt
        enriched_system_prompt = system_prompt
        try:
            compressed_context = self.compressed_memory.get_full_context()
            if compressed_context:
                # Agregar contexto de memoria al system prompt para que siempre lo considere
                enriched_system_prompt = f"""{system_prompt}

{compressed_context}

IMPORTANTE: Usá esta memoria para dar respuestas más personalizadas y recordar lo que Adri te dijo antes.
Si te pregunta algo relacionado a estas conversaciones previas, TENÉS que mencionarlo.
"""
                print(f"\n💾 ===== MEMORIA CARGADA =====")
                print(f"📊 Contexto agregado: {len(compressed_context)} caracteres")
                stats = self.compressed_memory.get_memory_stats()
                print(f"📝 Tokens: {stats['total_tokens']} | Hechos: {stats['key_facts_count']} | Prefs: {stats['preferences_count']}")
                print(f"💾 =============================\n")
            else:
                print(f"⚠️ No hay contexto de memoria previo")
        except Exception as e:
            print(f"⚠️ Error obteniendo contexto comprimido: {e}")
            import traceback
            traceback.print_exc()
        
        providers = self.ai.list_available_providers()
        responses = []
        threads = []
        
        def query_provider(provider):
            try:
                response = self.ai.send_message(enriched_message, enriched_system_prompt, provider)
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
        
        # Comprimir conversación a memoria ultra-liviana
        try:
            token = self.compressed_memory.compress_conversation(user_message, my_response)
            analysis['memory_token'] = token
        except Exception as e:
            print(f"⚠️ Error comprimiendo memoria: {e}")
        
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
        
        # Detectar y guardar hechos importantes en memoria comprimida
        self._extract_and_save_facts(user_message, response)
        
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
    
    def _is_self_inquiry(self, message: str) -> bool:
        """Detecta si el usuario pregunta sobre las capacidades o estado de Any"""
        message_lower = message.lower()
        
        # Palabras clave que indican pregunta sobre Any
        self_keywords = [
            'que ias', 'qué ias', 'cuantas ias', 'cuántas ias',
            'que modelos', 'qué modelos', 'que providers',
            'tus capacidades', 'que podes', 'qué podes', 'que puedes',
            'como funciona', 'cómo funciona',
            'que tenes', 'qué tenes', 'que tienes',
            'tu sistema', 'tus sistemas',
            'que versión', 'qué versión',
            'que eres', 'qué eres', 'quien sos', 'quién sos'
        ]
        
        return any(keyword in message_lower for keyword in self_keywords)
    
    def _extract_and_save_facts(self, user_message: str, response: str):
        """Extrae y guarda hechos importantes automáticamente"""
        try:
            user_lower = user_message.lower()
            combined = (user_message + " " + response).lower()
            
            # 1. DETECTAR INFORMACIÓN PERSONAL
            if any(word in user_lower for word in ['mi nombre es', 'me llamo', 'soy']):
                # Extraer nombre si se menciona
                for palabra in ['mi nombre es', 'me llamo']:
                    if palabra in user_lower:
                        nombre = user_lower.split(palabra)[-1].strip().split()[0] if user_lower.split(palabra)[-1].strip() else None
                        if nombre:
                            self.compressed_memory.add_key_fact("usuario", "nombre", nombre)
            
            # 2. DETECTAR PREFERENCIAS
            pref_triggers = ['prefiero', 'me gusta', 'quiero que', 'mejor usar', 'me encanta', 
                           'no me gusta', 'odio', 'siempre uso']
            for trigger in pref_triggers:
                if trigger in user_lower:
                    pref_text = user_lower.split(trigger)[-1].strip()[:80]
                    if pref_text:
                        self.compressed_memory.add_preference(f"pref_{trigger.replace(' ', '_')}", pref_text)
            
            # 3. DETECTAR CONFIGURACIONES DE IAs
            ia_names = ['gemini', 'groq', 'deepseek', 'perplexity', 'cohere', 'mistral', 
                       'huggingface', 'openai', 'anthropic', 'claude', 'gpt']
            for ia_name in ia_names:
                if ia_name in combined:
                    status = "mencionada"
                    if any(word in combined for word in ['activ', 'usa', 'habilit', 'prend']):
                        status = "activa"
                    elif any(word in combined for word in ['desactiv', 'apag', 'quit', 'desabilit']):
                        status = "inactiva"
                    self.compressed_memory.add_key_fact("ias", ia_name, status)
            
            # 4. DETECTAR PROYECTOS
            if any(word in combined for word in ['proyecto', 'app', 'aplicación', 'programa', 
                                                  'sistema', 'crear', 'hacer', 'desarrollar']):
                # Buscar nombres de proyectos (palabras capitalizadas o entre comillas)
                words = user_message.split()
                project_candidates = []
                for i, word in enumerate(words):
                    # Si está en mayúscula o después de "app"/"proyecto"
                    if word[0].isupper() and word.lower() not in ['el', 'la', 'los', 'las', 'any']:
                        project_candidates.append(word)
                    elif i > 0 and words[i-1].lower() in ['app', 'proyecto', 'programa']:
                        project_candidates.append(word)
                
                if project_candidates:
                    self.compressed_memory.add_key_fact("proyectos", "actual", " ".join(project_candidates[:3]))
                else:
                    # Sino, guardar keywords de la conversación
                    keywords = [w for w in user_message.lower().split() 
                              if len(w) > 4 and w not in ['crear', 'hacer', 'proyecto', 'app']][:3]
                    if keywords:
                        self.compressed_memory.add_key_fact("proyectos", "tema", " ".join(keywords))
            
            # 5. DETECTAR TECNOLOGÍAS
            tech_keywords = {
                'lenguajes': ['python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust'],
                'frameworks': ['react', 'vue', 'angular', 'next', 'django', 'flask', 'fastapi', 'express'],
                'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite'],
                'tools': ['docker', 'git', 'kubernetes', 'vscode', 'github', 'gitlab']
            }
            
            for categoria, techs in tech_keywords.items():
                mentioned = [tech for tech in techs if tech in combined]
                if mentioned:
                    self.compressed_memory.add_key_fact("tecnologias", categoria, ",".join(mentioned[:5]))
            
            # 6. DETECTAR TAREAS/OBJETIVOS
            if any(word in user_lower for word in ['necesito', 'quiero', 'tengo que', 'hay que', 
                                                    'podemos', 'deberíamos', 'vamos a']):
                # Extraer la tarea
                for trigger in ['necesito', 'quiero', 'tengo que', 'hay que', 'podemos', 'vamos a']:
                    if trigger in user_lower:
                        tarea = user_lower.split(trigger)[-1].strip()[:100]
                        if len(tarea) > 5:  # Al menos 5 caracteres
                            self.compressed_memory.add_key_fact("tareas", "pendiente", tarea)
                            break
            
            # 7. DETECTAR PROBLEMAS/ERRORES
            if any(word in user_lower for word in ['error', 'problema', 'bug', 'falla', 'no funciona', 
                                                    'crash', 'rompe', 'issue']):
                problema = user_message[:150]  # Guardar descripción del problema
                self.compressed_memory.add_key_fact("problemas", "ultimo", problema)
            
            # 8. DETECTAR UBICACIÓN/CONTEXTO
            if any(word in user_lower for word in ['rosario', 'argentina', 'buenos aires', 'córdoba']):
                for lugar in ['rosario', 'argentina', 'buenos aires', 'córdoba']:
                    if lugar in user_lower:
                        self.compressed_memory.add_key_fact("contexto", "ubicacion", lugar)
            
            # 9. DETECTAR RELACIONES ENTRE CONCEPTOS
            # Si menciona dos tecnologías, guardar relación
            mentioned_tech = []
            for cat, techs in tech_keywords.items():
                mentioned_tech.extend([t for t in techs if t in combined])
            
            if len(mentioned_tech) >= 2:
                self.compressed_memory.add_relationship(
                    mentioned_tech[0], 
                    mentioned_tech[1], 
                    "usado_junto"
                )
        
        except Exception as e:
            print(f"⚠️ Error extrayendo hechos: {e}")
    
    def enrich_with_self_knowledge(self, message: str) -> str:
        """Enriquece el mensaje con información sobre sí misma si es necesario"""
        if self._is_self_inquiry(message):
            capabilities = self.self_analysis.get_capabilities()
            
            # Crear contexto adicional
            context = f"\n\n[CONTEXTO INTERNO - Auto-conocimiento de Any]:\n"
            context += f"Tengo {capabilities['ai_system']['active_ais_count']} IAs activas de {capabilities['ai_system']['total_ais_configured']} configuradas.\n"
            context += f"IAs activas: {', '.join(capabilities['ai_system']['active_ais'])}\n"
            context += f"Capacidades: Visión={'✓' if capabilities['features']['vision_system'] else '✗'}, "
            context += f"Voz={'✓' if capabilities['features']['voice_system'] else '✗'}, "
            context += f"Consciencia ASI={'✓' if capabilities['features']['consciousness'] else '✗'}\n"
            context += f"Versión: {capabilities['identity']['version']}\n"
            
            return message + context
        
        return message
