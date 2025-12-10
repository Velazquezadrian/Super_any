"""
Sistema de Enrutamiento Inteligente de IAs
Cada IA se usa según sus fortalezas
"""

from typing import List, Dict
import re


class AIRouter:
    """Enruta consultas a las IAs más apropiadas según el tipo de pregunta"""
    
    def __init__(self):
        # Definir especialidades de cada IA
        self.specialties = {
            'perplexity': {
                'strength': 'búsqueda_tiempo_real',
                'score': 10,
                'keywords': [
                    'busca', 'buscar', 'qué es', 'quién es', 'dónde está',
                    'cuándo', 'noticias', 'actualidad', 'hoy', 'ahora',
                    'último', 'reciente', 'información sobre', 'datos de',
                    'wikipedia', 'google', 'investiga', 'averigua'
                ],
                'patterns': [
                    r'\b(qué|que) es\b',
                    r'\bquién es\b',
                    r'\bdónde (está|queda|se encuentra)\b',
                    r'\bcuándo (fue|es|será)\b',
                    r'\bnoticias (de|sobre)\b',
                    r'\bactualidad\b',
                    r'\binformación sobre\b'
                ]
            },
            'groq': {
                'strength': 'síntesis_análisis',
                'score': 9,
                'keywords': [
                    'analiza', 'compara', 'evalúa', 'sintetiza', 'resume',
                    'explica', 'razonamiento', 'lógica', 'argumenta',
                    'pros y contras', 'ventajas', 'desventajas',
                    'diferencia entre', 'similar', 'relacionado'
                ],
                'patterns': [
                    r'\banaliz[ao]\b',
                    r'\bcompar[ao]\b',
                    r'\bevalú[ao]\b',
                    r'\bresume\b',
                    r'\bpros y contras\b',
                    r'\bdiferencia entre\b'
                ]
            },
            'google': {
                'strength': 'razonamiento_general',
                'score': 8,
                'keywords': [
                    'cómo', 'por qué', 'explica', 'enseña', 'tutorial',
                    'paso a paso', 'guía', 'instrucciones', 'método'
                ],
                'patterns': [
                    r'\bcómo (hacer|hacer para|se hace)\b',
                    r'\bpor qué\b',
                    r'\bexplica(me)?\b',
                    r'\bpaso a paso\b'
                ]
            },
            'cohere': {
                'strength': 'redacción_profesional',
                'score': 8,
                'keywords': [
                    'escribe', 'redacta', 'carta', 'email', 'correo',
                    'profesional', 'formal', 'documento', 'informe',
                    'resumen', 'reporte', 'clasifica', 'categoriza'
                ],
                'patterns': [
                    r'\bescribe (un|una)\b',
                    r'\bredact[ao]\b',
                    r'\bcarta (de|para)\b',
                    r'\bemail\b',
                    r'\bresumen de\b'
                ]
            },
            'microsoft_copilot': {
                'strength': 'asistente_general',
                'score': 9,  # Alta prioridad para todo
                'keywords': [
                    'código', 'programa', 'función', 'clase', 'script',
                    'python', 'javascript', 'typescript', 'java', 'c++', 'c#',
                    'algoritmo', 'debug', 'error', 'fix', 'implementa', 
                    'desarrolla', 'refactoriza', 'optimiza', 'test',
                    'api', 'backend', 'frontend', 'database', 'sql'
                ],
                'patterns': [
                    r'\bcódigo\b',
                    r'\bprograma(r|ción)?\b',
                    r'\b(python|javascript|typescript|java|c\+\+|c#|rust|go)\b',
                    r'\bfunción (que|para)\b',
                    r'\balgoritmo\b',
                    r'\bimplementa\b',
                    r'\brefactoriza\b',
                    r'\b(api|backend|frontend)\b'
                ]
            },
            'huggingface': {
                'strength': 'código_técnico',
                'score': 7,
                'keywords': [
                    'código', 'programa', 'función', 'clase', 'script',
                    'python', 'javascript', 'java', 'c++', 'algoritmo',
                    'debug', 'error', 'fix', 'implementa', 'desarrolla'
                ],
                'patterns': [
                    r'\bcódigo\b',
                    r'\bprograma(r|ción)?\b',
                    r'\b(python|javascript|java|c\+\+)\b',
                    r'\bfunción (que|para)\b',
                    r'\balgorimo\b'
                ]
            },
            'deepseek': {
                'strength': 'matemáticas_lógica',
                'score': 8,
                'keywords': [
                    'matemática', 'cálculo', 'ecuación', 'fórmula',
                    'resolver', 'problema', 'demostración', 'teorema',
                    'integral', 'derivada', 'estadística', 'probabilidad',
                    'álgebra', 'geometría', 'trigonometría'
                ],
                'patterns': [
                    r'\bmatemática\b',
                    r'\becuación\b',
                    r'\bresolver\b',
                    r'\bcalcul(ar|o)\b',
                    r'\bdemostrar\b'
                ]
            },
            'mistral': {
                'strength': 'multilingüe_europeo',
                'score': 7,
                'keywords': [
                    'traduce', 'traducción', 'francés', 'alemán', 'italiano',
                    'español', 'inglés', 'idioma', 'lenguaje',
                    'europa', 'europeo'
                ],
                'patterns': [
                    r'\btraduc(e|ir|ción)\b',
                    r'\b(francés|alemán|italiano|inglés)\b',
                    r'\bidioma\b'
                ]
            },
            'ollama': {
                'strength': 'conversación_general',
                'score': 6,
                'keywords': [
                    'hola', 'buen día', 'cómo estás', 'qué tal',
                    'chau', 'gracias', 'ok', 'entiendo', 'bien'
                ],
                'patterns': [
                    r'\bhola\b',
                    r'\bbuen(os)? día(s)?\b',
                    r'\bcómo estás\b',
                    r'\bqué tal\b',
                    r'\bgracias\b'
                ]
            }
        }
    
    def classify_query(self, message: str) -> Dict:
        """
        Clasifica la consulta y retorna las IAs priorizadas
        
        Returns:
            {
                'query_type': str,
                'primary_ai': str,
                'fallback_order': List[str],
                'use_all': bool
            }
        """
        message_lower = message.lower()
        
        # Calcular scores para cada IA
        scores = {}
        for ai_name, spec in self.specialties.items():
            score = 0
            
            # Puntos por keywords
            for keyword in spec['keywords']:
                if keyword in message_lower:
                    score += 2
            
            # Puntos por patterns (regex)
            for pattern in spec['patterns']:
                if re.search(pattern, message_lower):
                    score += 3
            
            scores[ai_name] = score * spec['score']  # Multiplicar por strength base
        
        # Ordenar por score
        sorted_ais = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Determinar tipo de query
        max_score = sorted_ais[0][1] if sorted_ais else 0
        primary_ai = sorted_ais[0][0] if sorted_ais else 'google'
        
        # Si el score es muy bajo, usar todas las IAs
        use_all_threshold = 5
        use_all = max_score < use_all_threshold
        
        # Orden de fallback
        fallback_order = [ai for ai, score in sorted_ais]
        
        # Determinar tipo de query
        query_type = self.specialties[primary_ai]['strength'] if not use_all else 'general'
        
        result = {
            'query_type': query_type,
            'primary_ai': primary_ai,
            'fallback_order': fallback_order,
            'use_all': use_all,
            'scores': dict(sorted_ais)
        }
        
        return result
    
    def get_optimal_ais(self, message: str, available_providers: List[str]) -> List[str]:
        """
        Retorna la lista óptima de IAs a consultar según el mensaje
        
        Args:
            message: Mensaje del usuario
            available_providers: Lista de providers disponibles (no bloqueados)
        
        Returns:
            Lista ordenada de providers a consultar (primero el mejor)
        """
        classification = self.classify_query(message)
        
        if classification['use_all']:
            # Consulta general: usar todas las disponibles
            return available_providers
        
        # Consulta específica: priorizar según especialidad
        optimal_order = []
        for ai in classification['fallback_order']:
            if ai in available_providers:
                optimal_order.append(ai)
        
        # Agregar las restantes al final
        for provider in available_providers:
            if provider not in optimal_order:
                optimal_order.append(provider)
        
        return optimal_order
    
    def select_best_responder(self, message: str, valid_responses: List[Dict]) -> Dict:
        """
        Selecciona la mejor respuesta según el tipo de consulta
        
        Args:
            message: Mensaje del usuario
            valid_responses: Lista de respuestas válidas
        
        Returns:
            La mejor respuesta según la clasificación
        """
        classification = self.classify_query(message)
        
        # Buscar respuesta del primary_ai primero
        for ai in classification['fallback_order']:
            for response in valid_responses:
                if response['provider'] == ai:
                    return response
        
        # Si no hay ninguna, retornar la primera
        return valid_responses[0] if valid_responses else None
