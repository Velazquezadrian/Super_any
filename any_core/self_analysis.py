"""
Módulo de Auto-Análisis de Any
Sistema para que Any conozca su propia configuración y capacidades
"""

import json
from pathlib import Path
from typing import Dict, List


class SelfAnalysis:
    """Sistema de auto-análisis y auto-conocimiento de Any"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Carga la configuración actual"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error cargando config: {e}")
            return {}
    
    def get_active_ais(self) -> List[Dict]:
        """
        Obtiene lista de IAs activas con su información
        
        Returns:
            Lista de diccionarios con info de cada IA activa
        """
        active_ais = []
        providers = self.config.get('ai_providers', {})
        
        for name, config in providers.items():
            if config.get('enabled', False):
                ai_info = {
                    'name': name.upper(),
                    'model': config.get('model', 'unknown'),
                    'type': config.get('type', 'unknown'),
                    'cost': config.get('cost', 'unknown'),
                    'has_api_key': bool(config.get('api_key', ''))
                }
                active_ais.append(ai_info)
        
        return active_ais
    
    def get_all_ais(self) -> List[Dict]:
        """
        Obtiene lista de TODAS las IAs configuradas (activas e inactivas)
        
        Returns:
            Lista de diccionarios con info de cada IA
        """
        all_ais = []
        providers = self.config.get('ai_providers', {})
        
        for name, config in providers.items():
            ai_info = {
                'name': name.upper(),
                'model': config.get('model', 'unknown'),
                'type': config.get('type', 'unknown'),
                'cost': config.get('cost', 'unknown'),
                'enabled': config.get('enabled', False),
                'has_api_key': bool(config.get('api_key', ''))
            }
            all_ais.append(ai_info)
        
        return all_ais
    
    def get_capabilities(self) -> Dict:
        """
        Retorna un resumen de las capacidades actuales de Any
        
        Returns:
            Diccionario con todas las capacidades
        """
        active_ais = self.get_active_ais()
        all_ais = self.get_all_ais()
        
        capabilities = {
            'identity': {
                'name': self.config.get('identity', {}).get('name', 'Any'),
                'nickname': self.config.get('identity', {}).get('nickname', 'Any'),
                'version': self.config.get('version', '1.0.0')
            },
            'ai_system': {
                'total_ais_configured': len(all_ais),
                'active_ais_count': len(active_ais),
                'active_ais': [ai['name'] for ai in active_ais],
                'inactive_ais': [ai['name'] for ai in all_ais if not ai['enabled']]
            },
            'features': {
                'multi_ai_synthesis': True,
                'vision_system': True,
                'voice_system': True,
                'text_to_speech': True,
                'speech_to_text': True,
                'screen_capture': True,
                'consciousness': True,
                'auto_learning': True,
                'memory_persistence': True,
                'command_execution': self.config.get('permissions', {}).get('can_execute_commands', False),
                'file_modification': self.config.get('permissions', {}).get('can_modify_files', False),
                'self_update': self.config.get('permissions', {}).get('can_self_update', False)
            },
            'permissions': self.config.get('permissions', {}),
            'memory': {
                'auto_save': self.config.get('memory', {}).get('auto_save', True),
                'max_history': self.config.get('memory', {}).get('max_history', 1000)
            }
        }
        
        return capabilities
    
    def generate_status_report(self) -> str:
        """
        Genera un reporte de estado completo en texto
        
        Returns:
            String con el reporte formateado
        """
        caps = self.get_capabilities()
        active_ais = self.get_active_ais()
        
        report = f"""
╔══════════════════════════════════════════════╗
║       ANY - SISTEMA DE AUTO-ANÁLISIS        ║
╚══════════════════════════════════════════════╝

🆔 IDENTIDAD:
   • Nombre: {caps['identity']['name']}
   • Apodo: {caps['identity']['nickname']}
   • Versión: {caps['identity']['version']}

🧠 SISTEMA DE INTELIGENCIA ARTIFICIAL:
   • Total de IAs configuradas: {caps['ai_system']['total_ais_configured']}
   • IAs activas: {caps['ai_system']['active_ais_count']}
   
   ✅ IAs ACTIVAS:
"""
        
        for ai in active_ais:
            report += f"      • {ai['name']}\n"
            report += f"        - Modelo: {ai['model']}\n"
            report += f"        - Tipo: {ai['type']}\n"
            report += f"        - Costo: {ai['cost']}\n"
            report += f"        - API Key: {'✓ Configurada' if ai['has_api_key'] else '✗ Faltante'}\n"
        
        if caps['ai_system']['inactive_ais']:
            report += f"\n   ⚠️ IAs DISPONIBLES (inactivas):\n"
            for ai_name in caps['ai_system']['inactive_ais']:
                report += f"      • {ai_name}\n"
        
        report += f"""
🎯 CAPACIDADES:
   • Síntesis Multi-IA: {'✓' if caps['features']['multi_ai_synthesis'] else '✗'}
   • Sistema de Visión: {'✓' if caps['features']['vision_system'] else '✗'}
   • Sistema de Voz: {'✓' if caps['features']['voice_system'] else '✗'}
   • Text-to-Speech: {'✓' if caps['features']['text_to_speech'] else '✗'}
   • Speech-to-Text: {'✓' if caps['features']['speech_to_text'] else '✗'}
   • Captura de Pantalla: {'✓' if caps['features']['screen_capture'] else '✗'}
   • Consciencia ASI: {'✓' if caps['features']['consciousness'] else '✗'}
   • Auto-Aprendizaje: {'✓' if caps['features']['auto_learning'] else '✗'}
   • Memoria Persistente: {'✓' if caps['features']['memory_persistence'] else '✗'}

🔐 PERMISOS:
   • Ejecutar comandos: {'✓' if caps['features']['command_execution'] else '✗'}
   • Modificar archivos: {'✓' if caps['features']['file_modification'] else '✗'}
   • Auto-actualización: {'✓' if caps['features']['self_update'] else '✗'}

💾 CONFIGURACIÓN DE MEMORIA:
   • Auto-guardado: {'✓' if caps['memory']['auto_save'] else '✗'}
   • Historial máximo: {caps['memory']['max_history']} conversaciones

╚══════════════════════════════════════════════╝
"""
        
        return report
    
    def get_ai_status_summary(self) -> str:
        """
        Genera un resumen corto del estado de las IAs
        
        Returns:
            String con resumen corto
        """
        active_ais = self.get_active_ais()
        ai_names = [ai['name'] for ai in active_ais]
        
        if not ai_names:
            return "⚠️ No hay IAs activas actualmente."
        
        return f"🧠 Tengo {len(ai_names)} IAs activas: {', '.join(ai_names)}"
    
    def can_i(self, capability: str) -> bool:
        """
        Verifica si Any tiene una capacidad específica
        
        Args:
            capability: Nombre de la capacidad a verificar
            
        Returns:
            True si tiene la capacidad, False si no
        """
        caps = self.get_capabilities()
        
        # Verificar en features
        if capability in caps['features']:
            return caps['features'][capability]
        
        # Verificar en permissions
        if capability in caps['permissions']:
            return caps['permissions'][capability]
        
        return False
