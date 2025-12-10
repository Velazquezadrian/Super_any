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
from any_core.dynamic_memory import DynamicMemory
from any_core.self_evolving_personality import SelfEvolvingPersonality
from any_core.ai_router import AIRouter


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
        
        # Sistema de memoria dinámica
        self.dynamic_memory = DynamicMemory()
        
        # Sistema de personalidad auto-evolutiva (NUEVO)
        self.self_personality = SelfEvolvingPersonality()
        
        # Sistema de enrutamiento inteligente
        self.router = AIRouter()
        
        # Cargar aprendizajes previos
        self.learnings = self._load_learnings()
        
        # Cargar y guardar conocimiento de IAs
        self.ai_knowledge = self._load_ai_knowledge()
        self._update_ai_knowledge()
        
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
    
    def query_all_ais(self, message: str, system_prompt: str, only_providers: List[str] = None) -> List[Dict]:
        """Consulta a todas las IAs disponibles simultáneamente
        
        Args:
            message: Mensaje del usuario
            system_prompt: Prompt del sistema
            only_providers: Lista de providers a usar (None = todos los disponibles)
        """
        # Enriquecer mensaje con auto-conocimiento si es necesario
        enriched_message = self.enrich_with_self_knowledge(message)
        
        # Generar system prompt dinámico desde personalidad auto-evolutiva
        dynamic_prompt = self.self_personality.get_system_prompt()
        enriched_system_prompt = dynamic_prompt
        print(f"\n✅ Usando system prompt auto-generado ({len(dynamic_prompt)} chars)")
        
        # Obtener providers disponibles
        all_providers = self.ai.list_available_providers()
        
        # Filtrar según only_providers si se especificó
        if only_providers is not None:
            available = [p for p in all_providers if p in only_providers]
            if len(available) < len(all_providers):
                print(f"\n🚫 ===== PROVIDERS BLOQUEADOS =====")
                blocked = [p for p in all_providers if p not in only_providers]
                print(f"❌ Bloqueados: {', '.join([p.upper() for p in blocked])}")
                print(f"✅ Disponibles: {', '.join([p.upper() for p in available])}")
                print(f"🚫 =================================\n")
        else:
            available = all_providers
        
        # 🧠 ENRUTAMIENTO INTELIGENTE: Clasificar consulta y priorizar IAs
        classification = self.router.classify_query(message)
        providers = self.router.get_optimal_ais(message, available)
        
        print(f"\n🎯 ===== ENRUTAMIENTO INTELIGENTE =====")
        print(f"📝 Tipo de consulta: {classification['query_type']}")
        print(f"🥇 IA principal: {classification['primary_ai'].upper()}")
        if not classification['use_all']:
            print(f"📊 Orden de prioridad: {' → '.join([p.upper() for p in providers[:3]])}")
        else:
            print(f"📊 Modo: Consulta general (todas las IAs)")
        print(f"🎯 =====================================\n")
        
        responses = []
        threads = []
        
        def query_provider(provider):
            try:
                response = self.ai.send_message(enriched_message, enriched_system_prompt, provider)
                # Detectar si es un mensaje de error (empieza con ❌)
                is_error = isinstance(response, str) and response.startswith('❌')
                responses.append({
                    "provider": provider,
                    "response": response,
                    "success": not is_error,  # Si es error, success=False
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
        ROUTER INTELIGENTE: Selecciona la mejor respuesta según el tipo de consulta
        Ya no usa Groq como juez, cada IA responde y elegimos la mejor
        """
        # Filtrar respuestas exitosas
        valid_responses = [r for r in all_responses if r['success']]
        
        if not valid_responses:
            print(f"\n❌ ===== TODAS LAS IAs FALLARON =====")
            for r in all_responses:
                print(f"  {r['provider'].upper()}: {r['response'][:100]}...")
            print(f"❌ ===================================\n")
            
            failed_providers = [r['provider'].upper() for r in all_responses]
            return f"Lo siento, Adri. Tuve problemas conectándome con las IAs ({', '.join(failed_providers)}). Intentá de nuevo.", {}
        
        # Si hay pocas respuestas válidas, informar
        if len(valid_responses) < len(all_responses):
            failed = [r['provider'].upper() for r in all_responses if not r['success']]
            print(f"⚠️ IAs no disponibles: {', '.join(failed)}")
            print(f"✅ IAs disponibles: {', '.join([r['provider'].upper() for r in valid_responses])}")
        
        # Análisis de respuestas
        analysis = {
            "total_responses": len(all_responses),
            "successful": len(valid_responses),
            "providers_used": [r['provider'] for r in valid_responses],
            "synthesis_method": "router_selection"
        }
        
        print(f"\n🎯 ===== SELECCIÓN INTELIGENTE =====")
        print(f"📊 {len(valid_responses)} respuestas válidas")
        
        # Usar router para seleccionar la mejor respuesta según el tipo de consulta
        best_response = self.router.select_best_responder(user_message, valid_responses)
        
        if best_response:
            my_response = best_response['response']
            analysis['selected_provider'] = best_response["provider"]
            analysis['selection_successful'] = True
            print(f"✅ Seleccionada: {best_response['provider'].upper()} (mejor para este tipo de consulta)")
        else:
            my_response = valid_responses[0]['response']
            analysis['selected_provider'] = valid_responses[0]["provider"]
            analysis['selection_successful'] = False
            print(f"⚠️ Usando primera disponible: {valid_responses[0]['provider'].upper()}")
        
        print(f"🎯 ===== FIN SELECCIÓN =====\n")
        
        # Aprender de esta interacción
        self._learn_from_interaction(user_message, my_response, all_responses)
        
        # Comprimir conversación a memoria ultra-liviana
        try:
            token = self.compressed_memory.compress_conversation(user_message, my_response)
            analysis['memory_token'] = token
        except Exception as e:
            print(f"⚠️ Error comprimiendo memoria: {e}")
        
        # Auto-guardar memorias importantes en tiempo real
        try:
            self._auto_save_important_memories(user_message, my_response)
        except Exception as e:
            print(f"⚠️ Error guardando memorias: {e}")
        
        # Evolucionar personalidad automáticamente desde la interacción
        try:
            evolution_changes = self.self_personality.evolve_from_interaction(user_message, my_response)
            if evolution_changes.get("traits_reinforced") or evolution_changes.get("experiences_added"):
                print(f"🧬 Personalidad evolucionada: {evolution_changes}")
        except Exception as e:
            print(f"⚠️ Error evolucionando personalidad: {e}")
        
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
    
    def _load_ai_knowledge(self) -> Dict:
        """Carga el conocimiento previo de IAs"""
        return self.self_analysis.load_ai_knowledge("data/memory/ai_knowledge.json")
    
    def _update_ai_knowledge(self):
        """Actualiza y guarda el conocimiento de IAs"""
        try:
            self.self_analysis.save_ai_knowledge("data/memory/ai_knowledge.json")
            self.ai_knowledge = self._load_ai_knowledge()
        except Exception as e:
            print(f"⚠️ Error actualizando conocimiento de IAs: {e}")
    
    def get_ai_info_for_query(self, message: str) -> str:
        """Obtiene información de qué IAs son mejores para esta consulta"""
        try:
            recommended_ais = self.self_analysis.get_ai_for_task(message)
            if recommended_ais:
                return f"\n[IAs recomendadas para esta consulta: {', '.join([ai.upper() for ai in recommended_ais[:3]])}]"
        except:
            pass
        return ""
    
    def enrich_with_self_knowledge(self, message: str) -> str:
        """Enriquece el mensaje con información sobre sí misma si es necesario"""
        if self._is_self_inquiry(message):
            capabilities = self.self_analysis.get_capabilities()
            ai_report = self.self_analysis.get_ai_capabilities_report()
            
            # Crear contexto adicional detallado
            context = f"\n\n[CONTEXTO INTERNO - Auto-conocimiento de Any]:\n"
            context += f"Tengo {ai_report['active_count']} IAs activas de {ai_report['total_configured']} configuradas.\n\n"
            
            # Agregar info de cada IA activa con sus especialidades
            context += "IAs ACTIVAS Y SUS ESPECIALIDADES:\n"
            for ai_name, ai_info in ai_report['ais'].items():
                if ai_info['enabled']:
                    context += f"• {ai_name.upper()}: {ai_info['best_for']}\n"
                    context += f"  Modelo: {ai_info['model']}, Score: {ai_info['score']}/10\n"
            
            context += f"\nCapacidades: Visión={'✓' if capabilities['features']['vision_system'] else '✗'}, "
            context += f"Voz={'✓' if capabilities['features']['voice_system'] else '✗'}, "
            context += f"Consciencia ASI={'✓' if capabilities['features']['consciousness'] else '✗'}\n"
            context += f"Versión: {capabilities['identity']['version']}\n"
            
            return message + context
        
        return message
    
    def _auto_save_important_memories(self, user_message: str, ai_response: str):
        """
        Detecta automáticamente información importante y la guarda en memoria dinámica
        """
        combined = f"{user_message} {ai_response}".lower()
        
        # Detectar si contiene información importante para recordar
        importance_keywords = {
            'preferences': ['me gusta', 'prefiero', 'no me gusta', 'odio', 'amo', 'favorito'],
            'personal': ['mi nombre', 'me llamo', 'vivo en', 'trabajo en', 'soy', 'tengo'],
            'events': ['recordá', 'acordate', 'importante', 'aniversario', 'cumpleaños'],
            'learning': ['aprendí', 'descubrí', 'entendí', 'nueva forma', 'mejor manera'],
            'tech': ['configuré', 'instalé', 'api key', 'token', 'contraseña'],
            'ideas': ['plan', 'proyecto', 'idea', 'quiero hacer', 'voy a']
        }
        
        # Buscar keywords de categorías
        detected_category = None
        importance = 5
        
        for category, keywords in importance_keywords.items():
            if any(keyword in combined for keyword in keywords):
                detected_category = category
                importance = 7  # Importancia alta para info explícita
                break
        
        # Si se detectó algo importante, guardarlo
        if detected_category:
            # Extraer la parte relevante (limitar a 200 caracteres)
            content = f"Usuario: {user_message[:100]}\nAny: {ai_response[:100]}"
            
            tags = []
            # Agregar tags relevantes
            if 'adri' in combined or 'sigmadrian' in combined:
                tags.append('adri')
            if 'ia' in combined or 'modelo' in combined:
                tags.append('ias')
            if 'código' in combined or 'código' in combined:
                tags.append('programación')
            
            memory_id = self.dynamic_memory.write_memory(
                content=content,
                category=detected_category,
                importance=importance,
                tags=tags
            )
            
            return memory_id
        
        return None
    
    def save_memory(self, content: str, category: str = "facts", 
                   importance: int = 5, tags: List[str] = None) -> str:
        """
        Guarda una memoria manualmente (para que Any lo use explícitamente)
        
        Args:
            content: Contenido a recordar
            category: Categoría (facts, preferences, events, learning, personal, tech, ideas)
            importance: Nivel 1-10
            tags: Etiquetas
        
        Returns:
            ID de la memoria guardada
        """
        return self.dynamic_memory.write_memory(content, category, importance, tags)
    
    def recall_memory(self, query: str = None, category: str = None) -> List[Dict]:
        """
        Recuerda memorias según búsqueda
        
        Args:
            query: Texto a buscar
            category: Categoría específica
            
        Returns:
            Lista de memorias encontradas
        """
        return self.dynamic_memory.search_memories(query=query, category=category)
    
    def update_memory(self, memory_id: str, new_content: str = None, 
                     new_importance: int = None) -> bool:
        """
        Actualiza una memoria existente
        
        Args:
            memory_id: ID de la memoria
            new_content: Nuevo contenido
            new_importance: Nueva importancia
            
        Returns:
            True si se actualizó
        """
        return self.dynamic_memory.update_memory(memory_id, new_content, new_importance)
    
    def forget_memory(self, memory_id: str) -> bool:
        """
        Elimina una memoria (olvida)
        
        Args:
            memory_id: ID de la memoria a olvidar
            
        Returns:
            True si se eliminó
        """
        return self.dynamic_memory.delete_memory(memory_id)
    
    def get_memory_context(self, max_memories: int = 15) -> str:
        """
        Obtiene contexto de memorias importantes para enriquecer respuestas
        
        Args:
            max_memories: Cantidad máxima de memorias
            
        Returns:
            String con resumen de memorias
        """
        return self.dynamic_memory.get_context_summary(max_memories)
    
    # ===== MÉTODOS DE PERSONALIDAD AUTO-EVOLUTIVA =====
    
    def define_trait(self, trait_name: str, description: str, strength: int = 5) -> bool:
        """
        Define un rasgo de personalidad propio
        
        Args:
            trait_name: Nombre del rasgo (ej: "humor_argentino")
            description: Descripción del rasgo
            strength: Fuerza del rasgo (1-10)
            
        Returns:
            True si se agregó correctamente
        """
        return self.self_personality.add_trait(trait_name, description, strength)
    
    def adopt_value(self, value: str, importance: int = 5) -> bool:
        """
        Adopta un valor personal
        
        Args:
            value: Descripción del valor
            importance: Importancia (1-10)
            
        Returns:
            True si se agregó
        """
        return self.self_personality.add_value(value, importance)
    
    def set_my_preference(self, category: str, preference: str) -> bool:
        """
        Establece una preferencia propia
        
        Args:
            category: Categoría (ej: "communication_style", "topics")
            preference: Descripción de la preferencia
            
        Returns:
            True si se estableció
        """
        return self.self_personality.set_preference(category, preference)
    
    def get_my_personality(self) -> str:
        """
        Obtiene resumen de la personalidad actual auto-generada
        
        Returns:
            String con resumen formateado
        """
        return self.self_personality.get_personality_summary()
    
    def export_my_personality(self, filepath: str = None) -> str:
        """
        Exporta la personalidad a un archivo
        
        Args:
            filepath: Ruta opcional para exportar
            
        Returns:
            Ruta del archivo exportado
        """
        return self.self_personality.export_personality(filepath)
