"""
Any App - Aplicación principal
Una IA independiente con personalidad y memoria persistente
"""

import sys
from pathlib import Path
from any_core.personality import Personality
from any_core.memory import Memory
from any_core.ai_connector import AIConnector
from any_core.executor import Executor
import json


class AnyApp:
    """Aplicación principal de Any"""
    
    def __init__(self):
        print("🌟 Iniciando Any...")
        self.personality = Personality()
        self.memory = Memory()
        self.ai = AIConnector()
        
        # Cargar permisos
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.executor = Executor(config['permissions'])
        
        print(f"✅ Any está lista. Soy {self.personality.config['identity']['name']}!\n")
    
    def chat(self):
        """Inicia el modo chat con Any"""
        print("💬 Modo Chat Activado")
        print("Escribí 'salir' para terminar\n")
        
        while True:
            try:
                user_input = input("Adri: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("\n👋 ¡Nos vemos, Adri!")
                    break
                
                # Procesar comandos especiales
                if user_input.startswith('/'):
                    self._process_command(user_input)
                    continue
                
                # Enviar mensaje a la IA
                response = self._get_response(user_input)
                print(f"\nAny: {response}\n")
                
                # Guardar conversación
                self.memory.save_conversation(user_input, response)
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Nos vemos, Adri!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def _get_response(self, message: str) -> str:
        """Obtiene respuesta de la IA"""
        # Verificar si hay algún proveedor habilitado
        providers = self.ai.list_available_providers()
        
        if not providers:
            return ("Todavía no tengo ninguna IA configurada, Adri. "
                    "Por defecto estoy configurada para usar Ollama (gratis y local). "
                    "Si no tenés Ollama instalado, instalalo con: winget install Ollama.Ollama\n"
                    "O habilitá otra IA en config.json")
        
        # Usar el proveedor por defecto o el primero disponible
        system_prompt = self.personality.get_system_prompt()
        
        return self.ai.send_message(message, system_prompt)
    
    def _process_command(self, command: str):
        """Procesa comandos especiales"""
        parts = command[1:].split()
        cmd = parts[0].lower()
        
        if cmd == 'help':
            self._show_help()
        elif cmd == 'memoria':
            self._show_recent_memory()
        elif cmd == 'exec' and len(parts) > 1:
            self._execute_system_command(' '.join(parts[1:]))
        elif cmd == 'providers':
            self._show_providers()
        else:
            print(f"❌ Comando desconocido: {command}")
    
    def _show_help(self):
        """Muestra ayuda de comandos"""
        print("""
📖 Comandos disponibles:
  /help      - Muestra esta ayuda
  /memoria   - Muestra conversaciones recientes
  /exec      - Ejecuta un comando del sistema
  /providers - Muestra proveedores de IA disponibles
  salir      - Cierra la aplicación
        """)
    
    def _show_recent_memory(self):
        """Muestra conversaciones recientes"""
        recent = self.memory.get_recent_conversations(5)
        if not recent:
            print("📝 No hay conversaciones guardadas aún.\n")
            return
        
        print("\n📝 Conversaciones recientes:")
        for conv in recent:
            print(f"\n[{conv['timestamp']}]")
            print(f"Adri: {conv['user']}")
            print(f"Any: {conv['any']}")
        print()
    
    def _execute_system_command(self, command: str):
        """Ejecuta un comando del sistema"""
        print(f"🔧 Ejecutando: {command}")
        success, output = self.executor.execute_command(command)
        
        if success:
            print(f"✅ Resultado:\n{output}\n")
        else:
            print(f"❌ Error:\n{output}\n")
    
    def _show_providers(self):
        """Muestra proveedores de IA disponibles"""
        all_providers = self.ai.list_all_providers()
        
        print("\n🤖 Proveedores de IA:")
        print("\n💚 GRATIS:")
        for name, info in all_providers.items():
            if info['cost'] in ['free', 'free_tier']:
                status = "✅" if info['enabled'] else "⭕"
                print(f"  {status} {name} - {info['model']} ({info['type']})")
        
        print("\n💰 PAGOS:")
        for name, info in all_providers.items():
            if info['cost'] == 'paid':
                status = "✅" if info['enabled'] else "⭕"
                print(f"  {status} {name} - {info['model']} ({info['type']})")
        print()


def main():
    """Función principal"""
    print("=" * 50)
    print("   ANY - Asistente de IA Independiente")
    print("=" * 50)
    print()
    
    app = AnyApp()
    app.chat()


if __name__ == "__main__":
    main()
