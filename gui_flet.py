"""
Any App - Flet GUI (Moderna con Emojis)
Interfaz moderna usando Flet para mejor soporte de emojis y diseño
"""

import flet as ft
import threading
from datetime import datetime
import json
from any_core.personality import Personality
from any_core.memory import Memory
from any_core.ai_connector import AIConnector
from any_core.executor import Executor
from any_core.consciousness import Consciousness
from any_core.vision import VisionSystem
from any_core.voice import VoiceSystem
from any_core.self_analysis import SelfAnalysis


class AnyFletApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        
        # Inicializar componentes de Any
        self.personality = Personality()
        self.memory = Memory()
        self.ai = AIConnector()
        
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.executor = Executor(config['permissions'])
        
        # Sistema de Consciencia (ASI)
        self.consciousness = Consciousness(self.ai, self.personality, self.memory)
        
        # Sistema de Visión
        self.vision = VisionSystem()
        
        # Sistema de Voz
        self.voice = VoiceSystem()
        
        # Sistema de Auto-Análisis
        self.self_analysis = SelfAnalysis()
        
        # Variables de estado
        self.is_processing = False
        self.vision_mode = False
        self.voice_mode = False
        
        self.setup_ui()
        
        # Mensaje de bienvenida
        self.add_system_message("🌟 Any está lista. ¡Holis, Adri!")
        self.show_startup_analysis()
    
    def setup_page(self):
        """Configura la página principal"""
        self.page.title = "ANY 🤖 • Asistente de IA Independiente"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window.width = 1200
        self.page.window.height = 800
        
        # Colores personalizados (cyberpunk)
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#00ff9f",
                on_primary="#000000",
                secondary="#ff0099",
                background="#0a0e27",
                surface="#151b3d",
            )
        )
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Text(
                    "◢ ANY ◣",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#00ff9f"
                ),
                ft.Text(
                    "Independent AI Assistant • Rosario, Argentina",
                    size=12,
                    color="#666666"
                ),
            ]),
            bgcolor="#151b3d",
            padding=20,
        )
        
        # Chat display (ListView con scroll automático)
        self.chat_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True,
        )
        
        # Input area
        self.input_field = ft.TextField(
            hint_text="Escribí tu mensaje...",
            multiline=True,
            min_lines=1,
            max_lines=5,
            shift_enter=True,
            on_submit=lambda e: self.send_message(),
            expand=True,
            border_color="#00ff9f",
            focused_border_color="#00ff9f",
        )
        
        input_row = ft.Row([
            ft.IconButton(
                icon=ft.Icons.MIC,
                icon_color="#00ff9f",
                tooltip="Grabar audio",
                on_click=lambda e: self.start_listening()
            ),
            ft.IconButton(
                icon=ft.Icons.SCREENSHOT,
                icon_color="#ff0099",
                tooltip="Capturar pantalla",
                on_click=lambda e: self.capture_screen()
            ),
            self.input_field,
            ft.IconButton(
                icon=ft.Icons.SEND,
                icon_color="#00ff9f",
                tooltip="Enviar",
                on_click=lambda e: self.send_message()
            ),
        ])
        
        input_container = ft.Container(
            content=input_row,
            bgcolor="#151b3d",
            padding=10,
        )
        
        # Panel lateral (controles)
        self.status_text = ft.Text("● READY", color="#00ff9f", size=12)
        
        self.voice_toggle = ft.Switch(
            label="Modo Voz",
            value=False,
            on_change=lambda e: self.toggle_voice_mode()
        )
        
        # Panel de estado de IAs
        self.ai_status_indicators = {}
        self.ai_status_tooltips = {}
        self.ai_blocked_until = {}  # {provider: timestamp_cuando_desbloquear}
        ai_status_column = ft.Column([], spacing=5)
        
        # Crear indicadores para cada IA
        for provider_name in self.ai.providers.keys():
            if self.ai.providers[provider_name].get('enabled', False):
                icon = ft.Icon(ft.Icons.CIRCLE, color="#00ff9f", size=12)
                text = ft.Text(provider_name.upper()[:8], size=11, color="#ffffff")
                
                indicator = ft.Row(
                    [icon, text],
                    spacing=5,
                )
                
                self.ai_status_indicators[provider_name] = icon
                self.ai_status_tooltips[provider_name] = "Funcionando"
                ai_status_column.controls.append(indicator)
        
        controls_panel = ft.Container(
            content=ft.Column([
                ft.Text("ESTADO DEL SISTEMA", size=14, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.status_text,
                ft.Divider(),
                ft.Text("IAs ACTIVAS", size=12, weight=ft.FontWeight.BOLD),
                ai_status_column,
                ft.Divider(),
                self.voice_toggle,
                ft.Divider(),
                ft.ElevatedButton(
                    "🔍 Auto-Análisis",
                    on_click=lambda e: self.show_self_analysis(),
                    style=ft.ButtonStyle(
                        bgcolor="#00ff9f",
                        color="#000000",
                    )
                ),
                ft.ElevatedButton(
                    "💾 Ver Memoria",
                    on_click=lambda e: self.show_memory_stats()
                ),
                ft.ElevatedButton(
                    "🧠 Memorias Guardadas",
                    on_click=lambda e: self.show_dynamic_memories(),
                    style=ft.ButtonStyle(
                        bgcolor="#ff0099",
                        color="#ffffff",
                    )
                ),
                ft.ElevatedButton(
                    "🧬 Mi Personalidad",
                    on_click=lambda e: self.show_my_personality(),
                    style=ft.ButtonStyle(
                        bgcolor="#9d00ff",
                        color="#ffffff",
                    )
                ),
                ft.ElevatedButton(
                    "🗑️ Limpiar Chat",
                    on_click=lambda e: self.clear_chat()
                ),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            bgcolor="#151b3d",
            padding=20,
            width=250,
        )
        
        # Layout principal
        main_row = ft.Row([
            ft.Container(
                content=ft.Column([
                    self.chat_list,
                    input_container,
                ]),
                expand=True,
            ),
            controls_panel,
        ], expand=True)
        
        # Agregar todo a la página
        self.page.add(
            ft.Column([
                header,
                main_row,
            ], expand=True, spacing=0)
        )
    
    def add_message(self, sender: str, message: str, is_user: bool = False):
        """Agrega un mensaje al chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Determinar estilo según el emisor
        if is_user:
            # Mensaje del usuario (derecha)
            icon = "👤"
            bg_color = "#1a237e"
            alignment = ft.MainAxisAlignment.END
        else:
            # Mensaje de Any (izquierda)
            icon = "🤖"
            bg_color = "#004d40"
            alignment = ft.MainAxisAlignment.START
        
        message_container = ft.Container(
            content=ft.Column([
                ft.Text(f"{icon} {sender} • {timestamp}", size=11, color="#888888"),
                ft.Text(message, size=14, selectable=True),
            ], spacing=5),
            bgcolor=bg_color,
            padding=10,
            border_radius=10,
            width=700 if is_user else 800,
        )
        
        row = ft.Row([message_container], alignment=alignment)
        self.chat_list.controls.append(row)
        self.page.update()
    
    def add_system_message(self, message: str):
        """Agrega un mensaje del sistema"""
        system_msg = ft.Container(
            content=ft.Text(message, size=12, color="#666666", italic=True),
            padding=ft.padding.only(left=20, right=20, top=5, bottom=5),
        )
        self.chat_list.controls.append(system_msg)
        self.page.update()
    
    def check_blocked_ais(self):
        """Verifica si alguna IA bloqueada ya puede volver a participar"""
        import time
        current_time = time.time()
        
        unblocked = []
        for provider in list(self.ai_blocked_until.keys()):
            if current_time >= self.ai_blocked_until[provider]:
                # Ya pasó el tiempo, desbloquear
                self.update_ai_status(provider, True)
                unblocked.append(provider.upper())
                self.add_system_message(f"✅ {provider.upper()} volvió a estar disponible")
        
        return unblocked
    
    def get_available_providers(self):
        """Retorna lista de providers que NO están bloqueados"""
        import time
        current_time = time.time()
        
        available = []
        for provider in self.ai.providers.keys():
            if self.ai.providers[provider].get('enabled', False):
                # Verificar si está bloqueada
                if provider in self.ai_blocked_until:
                    if current_time >= self.ai_blocked_until[provider]:
                        # Ya se desbloqueó, remover del diccionario
                        del self.ai_blocked_until[provider]
                        available.append(provider)
                    # else: sigue bloqueada, no agregar
                else:
                    available.append(provider)
        
        return available
    
    def update_ai_status(self, provider: str, is_working: bool, error_msg: str = ""):
        """Actualiza el indicador de estado de una IA"""
        if provider in self.ai_status_indicators:
            if is_working:
                self.ai_status_indicators[provider].color = "#00ff9f"  # Verde
                self.ai_status_tooltips[provider] = "Funcionando"
                # Desbloquear si estaba bloqueada
                if provider in self.ai_blocked_until:
                    del self.ai_blocked_until[provider]
            else:
                self.ai_status_indicators[provider].color = "#ff0000"  # Rojo
                import re
                import time
                
                # Extraer tiempo de espera con múltiples patrones
                seconds = None
                
                # Patrón 1: "retry in 38.594s" o "Please retry in 38s"
                match = re.search(r'retry\s+in\s+(\d+\.?\d*)\s*s', error_msg.lower())
                if match:
                    seconds = float(match.group(1))
                else:
                    # Patrón 2: "seconds: 38" (formato protobuf)
                    match = re.search(r'seconds:\s*(\d+)', error_msg)
                    if match:
                        seconds = float(match.group(1))
                
                if seconds:
                    # Guardar timestamp cuando se desbloqueará
                    self.ai_blocked_until[provider] = time.time() + seconds
                    
                    minutes = int(seconds // 60)
                    if minutes > 0:
                        self.ai_status_tooltips[provider] = f"Límite alcanzado. Reintentar en {minutes}min"
                    else:
                        self.ai_status_tooltips[provider] = f"Límite alcanzado. Reintentar en {int(seconds)}seg"
                    
                    print(f"⏰ {provider.upper()} bloqueada por {int(seconds)} segundos")
                else:
                    self.ai_status_tooltips[provider] = "Límite alcanzado"
                    # Sin tiempo específico, bloquear por 60 segundos por defecto
                    self.ai_blocked_until[provider] = time.time() + 60
                    print(f"⏰ {provider.upper()} bloqueada por 60 segundos (tiempo por defecto)")
            self.page.update()
    
    def send_message(self):
        """Envía un mensaje a Any"""
        if self.is_processing:
            return
        
        message = self.input_field.value.strip()
        if not message:
            return
        
        # Limitar longitud
        if len(message) > 5000:
            self.add_system_message("⚠️ Mensaje muy largo. Máximo 5000 caracteres.")
            return
        
        # Limpiar input
        self.input_field.value = ""
        self.page.update()
        
        # Mostrar mensaje del usuario
        self.add_message("Adri", message, is_user=True)
        
        # Procesar en thread separado
        self.is_processing = True
        self.status_text.value = "● PROCESSING"
        self.status_text.color = "#ff0099"
        self.page.update()
        
        def process():
            try:
                # Comandos especiales
                if message.lower() in ['/memoria', '/memory', '/mem']:
                    self.show_memory_stats()
                    return
                elif message.lower() in ['/analisis', '/status', '/info']:
                    self.show_self_analysis()
                    return
                elif message.lower() in ['/ias', '/providers']:
                    active_ais = self.self_analysis.get_active_ais()
                    response = f"🧠 Tengo {len(active_ais)} IAs activas:\n"
                    for ai in active_ais:
                        response += f"✓ {ai['name']}: {ai['model']}\n"
                    self.add_message("Any", response, is_user=False)
                    return
                
                # Verificar IAs bloqueadas antes de consultar
                self.check_blocked_ais()
                
                # Obtener solo providers disponibles (no bloqueados)
                available_providers = self.get_available_providers()
                
                if not available_providers:
                    self.add_system_message("⚠️ Todas las IAs están temporalmente bloqueadas. Espera un momento...")
                    return
                
                # Consultar solo las IAs disponibles
                all_responses = self.consciousness.query_all_ais(
                    message,
                    self.personality.get_system_prompt(),
                    only_providers=available_providers
                )
                
                # Actualizar indicadores según respuestas
                failed_ais = []
                for response in all_responses:
                    provider = response.get('provider')
                    success = response.get('success', False)
                    
                    # Detectar si es error de límite/cuota
                    if not success:
                        error_msg = str(response.get('response', ''))
                        error_lower = error_msg.lower()
                        if any(word in error_lower for word in ['limit', 'quota', 'rate', '429', '403', 'exceeded']):
                            self.update_ai_status(provider, False, error_msg)
                            failed_ais.append(provider.upper())
                        else:
                            # Error temporal, mantener verde
                            self.update_ai_status(provider, True)
                    else:
                        self.update_ai_status(provider, True)
                
                # Mostrar mensaje si alguna IA falló
                if failed_ais:
                    self.add_system_message(f"⚠️ IAs con límite alcanzado: {', '.join(failed_ais)}")
                
                # Sintetizar respuesta (Groq decide)
                my_response, analysis = self.consciousness.synthesize_response(
                    all_responses,
                    message
                )
                
                # Mostrar respuesta
                self.add_message("Any", my_response, is_user=False)
                
                # Hablar si está en modo voz
                if self.voice_mode:
                    self.voice.speak(my_response)
                
            except Exception as e:
                self.add_message("Any", f"❌ Error: {str(e)}", is_user=False)
            
            finally:
                self.is_processing = False
                self.status_text.value = "● READY"
                self.status_text.color = "#00ff9f"
                self.page.update()
        
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
    
    def start_listening(self):
        """Inicia grabación de voz"""
        if self.is_processing or self.voice.is_listening:
            return
        
        self.add_system_message("🎤 Escuchando...")
        
        def on_complete(result):
            if isinstance(result, dict) and result.get('success'):
                # Transcribir audio
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                audio_file = result.get('audio_file')
                
                try:
                    with sr.AudioFile(audio_file) as source:
                        audio = recognizer.record(source)
                        text = recognizer.recognize_google(audio, language='es-AR')
                        
                    # Limpiar archivo
                    import os
                    try:
                        os.unlink(audio_file)
                    except:
                        pass
                    
                    # Poner texto en input
                    self.input_field.value = text
                    self.add_system_message(f"📝 Transcrito: {text}")
                    self.page.update()
                    
                except Exception as e:
                    self.add_system_message(f"❌ Error: {str(e)[:100]}")
            else:
                error = result.get('error', '❌ Error desconocido')
                self.add_system_message(error)
        
        self.voice.listen_async(on_complete, timeout=5)
    
    def capture_screen(self):
        """Captura y analiza la pantalla"""
        self.add_system_message("📸 Capturando pantalla...")
        
        def process():
            try:
                temp_path = self.vision.capture_screen()
                analysis = self.vision.analyze_image(temp_path)
                
                self.add_message("Any", f"📸 Análisis de pantalla:\n\n{analysis}", is_user=False)
                
            except Exception as e:
                self.add_system_message(f"❌ Error: {str(e)}")
        
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
    
    def toggle_voice_mode(self):
        """Activa/desactiva modo voz"""
        self.voice_mode = self.voice_toggle.value
        if self.voice_mode:
            self.add_system_message("🔊 Modo voz activado")
            self.voice.speak("Modo voz activado, boludo.")
        else:
            self.add_system_message("🔇 Modo voz desactivado")
    
    def show_self_analysis(self):
        """Muestra auto-análisis del sistema con especialidades de IAs"""
        # Generar reporte básico
        report = self.self_analysis.generate_status_report()
        
        # Agregar reporte de especialidades de IAs
        ai_report = self.self_analysis.get_ai_capabilities_report()
        
        report += "\n\n╔════════════════════════════════════════════════╗\n"
        report += "║   ESPECIALIDADES DE CADA IA 🎯               ║\n"
        report += "╚════════════════════════════════════════════════╝\n\n"
        
        for ai_name, ai_info in ai_report['ais'].items():
            if ai_info['enabled']:
                report += f"✅ {ai_name.upper()}\n"
                report += f"   📌 Especialidad: {ai_info['specialty']}\n"
                report += f"   🎯 Mejor para: {ai_info['best_for']}\n"
                report += f"   ⭐ Score: {ai_info['score']}/10\n"
                report += f"   🤖 Modelo: {ai_info['model']}\n"
                report += f"   💰 Costo: {ai_info['cost']}\n\n"
        
        # Mostrar ejemplos de uso
        report += "\n📝 EJEMPLOS DE USO:\n"
        report += "─" * 50 + "\n"
        
        examples = [
            ("Noticias/Búsquedas", "PERPLEXITY (10/10)"),
            ("Análisis/Comparaciones", "GROQ (9/10)"),
            ("Asistencia General", "MICROSOFT_COPILOT (9/10)"),
            ("Matemáticas/Lógica", "DEEPSEEK (8/10)"),
            ("Escritura Profesional", "COHERE (8/10)"),
            ("Explicaciones/Tutoriales", "GOOGLE (8/10)"),
            ("Programación", "HUGGINGFACE (7/10)"),
            ("Traducciones", "MISTRAL (7/10)")
        ]
        
        for task, ai in examples:
            report += f"• {task}: {ai}\n"
        
        report += "\n💡 El sistema elige automáticamente la mejor IA para cada consulta\n"
        
        # Guardar conocimiento actualizado
        self.self_analysis.save_ai_knowledge("data/memory/ai_knowledge.json")
        
        self.add_message("Any", report, is_user=False)
    
    def show_memory_stats(self):
        """Muestra estadísticas de memoria"""
        stats = self.consciousness.compressed_memory.get_memory_stats()
        context = self.consciousness.compressed_memory.get_full_context()
        
        response = f"""💾 MEMORIA COMPRIMIDA

📊 Estadísticas:
• Tokens guardados: {stats['total_tokens']}
• Hechos clave: {stats['key_facts_count']}
• Preferencias: {stats['preferences_count']}
• Tamaño: {stats['file_size_kb']:.2f} KB
• Última actualización: {stats['last_update']}

{context}
"""
        self.add_message("Any", response, is_user=False)
    
    def show_my_personality(self):
        """Muestra la personalidad auto-generada de Any"""
        personality_summary = self.consciousness.get_my_personality()
        
        intro = """🧬 PERSONALIDAD AUTO-EVOLUTIVA

Any construye su propia personalidad a través de experiencias.
No hay un prompt fijo - Any se define a sí misma.

"""
        
        response = intro + personality_summary
        
        response += """

💡 CÓMO FUNCIONA:
• Any aprende de cada conversación
• Desarrolla rasgos y valores propios
• Evoluciona su forma de comunicarse
• Construye su identidad de forma autónoma

✨ Any puede modificar su personalidad en cualquier momento
"""
        
        self.add_message("Any", response, is_user=False)
    
    def show_dynamic_memories(self):
        """Muestra las memorias guardadas dinámicamente"""
        dm = self.consciousness.dynamic_memory
        stats = dm.get_memory_stats()
        
        response = f"""🧠 MEMORIAS DINÁMICAS

📊 Estadísticas:
• Total de memorias: {stats['total_memories']}
• Última actualización: {stats['last_update']}

📁 Por categoría:
"""
        
        for category, count in stats['by_category'].items():
            if count > 0:
                response += f"  • {category}: {count} memorias\n"
        
        response += f"\n⭐ Por importancia:\n"
        for imp in range(10, 6, -1):
            count = stats['by_importance'][imp]
            if count > 0:
                response += f"  {'★' * imp} ({imp}/10): {count}\n"
        
        # Mostrar memorias importantes
        important = dm.get_important_memories(min_importance=7)
        if important:
            response += f"\n\n═══ MEMORIAS IMPORTANTES ═══\n"
            for i, mem in enumerate(important[:10], 1):
                response += f"\n{i}. [{mem['category'].upper()}] {mem['content']}\n"
                response += f"   📌 Importancia: {mem['importance']}/10\n"
                response += f"   👁️ Accesos: {mem['access_count']}\n"
                response += f"   🏷️ Tags: {', '.join(mem['tags']) if mem['tags'] else 'sin tags'}\n"
                response += f"   🆔 ID: {mem['id'][:8]}...\n"
        
        response += "\n\n💡 Any guarda automáticamente info importante durante las conversaciones"
        
        self.add_message("Any", response, is_user=False)
    
    def clear_chat(self):
        """Limpia el chat"""
        self.chat_list.controls.clear()
        self.add_system_message("🗑️ Chat limpiado")
        self.page.update()
    
    def show_startup_analysis(self):
        """Muestra análisis al inicio"""
        def show():
            import time
            time.sleep(0.5)
            
            capabilities = self.self_analysis.get_capabilities()
            active_ais = self.self_analysis.get_active_ais()
            stats = self.consciousness.compressed_memory.get_memory_stats()
            
            startup_msg = f"""╔════════════════════════════════════╗
║    SISTEMA INICIALIZADO ✓         ║
╚════════════════════════════════════╝

🧠 IAs Activas: {len(active_ais)}/{len(self.self_analysis.get_all_ais())}
"""
            for ai in active_ais:
                startup_msg += f"   ✓ {ai['name']}: {ai['model']}\n"
            
            startup_msg += f"""
🎯 Capacidades:
   {'✓' if capabilities['features']['vision_system'] else '✗'} Sistema de Visión
   {'✓' if capabilities['features']['voice_system'] else '✗'} Sistema de Voz
   {'✓' if capabilities['features']['compressed_memory'] else '✗'} Memoria Comprimida
   {'✓' if capabilities['features']['self_analysis'] else '✗'} Auto-análisis

💾 Memoria Comprimida:
   {stats['total_tokens']} tokens • {stats['key_facts_count']} hechos • {stats['file_size_kb']:.2f} KB
"""
            
            self.add_message("Any", startup_msg, is_user=False)
        
        thread = threading.Thread(target=show)
        thread.daemon = True
        thread.start()


def main(page: ft.Page):
    AnyFletApp(page)


if __name__ == "__main__":
    ft.app(target=main)
