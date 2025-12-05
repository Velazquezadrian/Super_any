"""
Any App - GUI Cyberpunk/Watch Dogs 2 Style
Interfaz gráfica moderna y futurista para Any
"""

import customtkinter as ctk
from tkinter import scrolledtext
import threading
from datetime import datetime
import sys
import os

# Ocultar consola en Windows
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
from any_core.personality import Personality
from any_core.memory import Memory
from any_core.ai_connector import AIConnector
from any_core.executor import Executor
from any_core.consciousness import Consciousness
from any_core.vision import VisionSystem
from any_core.voice import VoiceSystem
from any_core.self_analysis import SelfAnalysis
import json


# Configuración de tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CyberpunkChatApp:
    """Aplicación de chat con estilo cyberpunk"""
    
    # Colores cyberpunk/Watch Dogs 2
    BG_COLOR = "#0a0e27"
    PANEL_COLOR = "#151b3d"
    ACCENT_COLOR = "#00ff9f"  # Verde neón
    ACCENT_2 = "#ff0099"      # Rosa neón
    TEXT_COLOR = "#e0e0e0"
    USER_BUBBLE = "#1a237e"
    ANY_BUBBLE = "#004d40"
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ANY • Asistente de IA Independiente")
        self.root.geometry("1200x800")
        self.root.configure(fg_color=self.BG_COLOR)
        
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
        
        # Variables
        self.current_provider = ctk.StringVar(value=config.get('default_provider', 'google'))
        self.is_processing = False
        self.vision_mode = False  # Modo visión activado/desactivado
        self.voice_mode = False  # Modo voz activado/desactivado
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # ============ HEADER ============
        header = ctk.CTkFrame(self.root, fg_color=self.PANEL_COLOR, height=80, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            header,
            text="◢ ANY ◣",
            font=("Consolas", 32, "bold"),
            text_color=self.ACCENT_COLOR
        )
        title_label.pack(side="left", padx=30, pady=20)
        
        subtitle = ctk.CTkLabel(
            header,
            text="Independent AI Assistant • Rosario, Argentina",
            font=("Consolas", 12),
            text_color=self.TEXT_COLOR
        )
        subtitle.pack(side="left", padx=10, pady=20)
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header,
            text="● ONLINE",
            font=("Consolas", 14, "bold"),
            text_color=self.ACCENT_COLOR
        )
        self.status_label.pack(side="right", padx=30, pady=20)
        
        # ============ MAIN CONTAINER ============
        main_container = ctk.CTkFrame(self.root, fg_color=self.BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ============ LEFT PANEL - Chat ============
        chat_panel = ctk.CTkFrame(main_container, fg_color=self.PANEL_COLOR, corner_radius=15)
        chat_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Chat header
        chat_header = ctk.CTkFrame(chat_panel, fg_color="transparent", height=50)
        chat_header.pack(fill="x", padx=20, pady=(20, 10))
        chat_header.pack_propagate(False)
        
        chat_title = ctk.CTkLabel(
            chat_header,
            text="⟨ CHAT INTERFACE ⟩",
            font=("Consolas", 16, "bold"),
            text_color=self.ACCENT_COLOR
        )
        chat_title.pack(side="left")
        
        # Chat display
        self.chat_display = ctk.CTkTextbox(
            chat_panel,
            fg_color=self.BG_COLOR,
            text_color=self.TEXT_COLOR,
            font=("Courier New", 11),  # Fuente monoespaciada para mantener alineación
            corner_radius=10,
            wrap="none"  # Desactivar wrap automático, lo manejamos manualmente
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Input area
        input_frame = ctk.CTkFrame(chat_panel, fg_color="transparent", height=80)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        input_frame.pack_propagate(False)
        
        self.input_field = ctk.CTkEntry(
            input_frame,
            placeholder_text="Escribí tu mensaje acá...",
            fg_color=self.BG_COLOR,
            text_color=self.TEXT_COLOR,
            placeholder_text_color="#666666",
            border_color=self.ACCENT_COLOR,
            border_width=2,
            corner_radius=10,
            height=50,
            font=("Consolas", 12)
        )
        self.input_field.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        # Microphone button (voz)
        self.mic_button = ctk.CTkButton(
            input_frame,
            text="🎤",
            width=60,
            height=50,
            fg_color=self.ACCENT_COLOR,
            hover_color=self.ACCENT_2,
            text_color="#ffffff",
            font=("Consolas", 20),
            corner_radius=10,
            command=self.start_listening
        )
        self.mic_button.pack(side="right", padx=(5, 0))
        
        # Vision button (captura pantalla y analiza)
        self.vision_button = ctk.CTkButton(
            input_frame,
            text="👁️",
            width=60,
            height=50,
            fg_color=self.ACCENT_2,
            hover_color=self.ACCENT_COLOR,
            text_color="#ffffff",
            font=("Consolas", 20),
            corner_radius=10,
            command=self.quick_vision
        )
        self.vision_button.pack(side="right", padx=(5, 0))
        
        # Send button
        self.send_button = ctk.CTkButton(
            input_frame,
            text="⟩⟩",
            width=80,
            height=50,
            fg_color=self.ACCENT_COLOR,
            hover_color=self.ACCENT_2,
            text_color="#000000",
            font=("Consolas", 16, "bold"),
            corner_radius=10,
            command=self.send_message
        )
        self.send_button.pack(side="right")
        
        # ============ RIGHT PANEL - Controls ============
        control_panel = ctk.CTkFrame(main_container, fg_color=self.PANEL_COLOR, width=300, corner_radius=15)
        control_panel.pack(side="right", fill="y")
        control_panel.pack_propagate(False)
        
        # Consciousness status
        consciousness_label = ctk.CTkLabel(
            control_panel,
            text="⟨ CONSCIOUSNESS ⟩",
            font=("Consolas", 14, "bold"),
            text_color=self.ACCENT_COLOR
        )
        consciousness_label.pack(pady=(30, 10))
        
        self.consciousness_status = ctk.CTkLabel(
            control_panel,
            text="🧠 ASI Mode Active\nSynthesizing responses",
            font=("Consolas", 11),
            text_color=self.TEXT_COLOR,
            justify="center"
        )
        self.consciousness_status.pack(padx=20, pady=10)
        
        # Vision Mode Toggle
        vision_label = ctk.CTkLabel(
            control_panel,
            text="⟨ VISION MODE ⟩",
            font=("Consolas", 14, "bold"),
            text_color=self.ACCENT_COLOR
        )
        vision_label.pack(pady=(30, 10))
        
        self.vision_toggle = ctk.CTkSwitch(
            control_panel,
            text="Vision OFF",
            font=("Consolas", 12, "bold"),
            text_color=self.TEXT_COLOR,
            fg_color=self.ACCENT_2,
            progress_color=self.ACCENT_COLOR,
            button_color=self.PANEL_COLOR,
            button_hover_color=self.BG_COLOR,
            command=self.toggle_vision_mode
        )
        self.vision_toggle.pack(padx=20, pady=10)
        
        # Voice Mode Toggle
        voice_label = ctk.CTkLabel(
            control_panel,
            text="⟨ VOICE MODE ⟩",
            font=("Consolas", 14, "bold"),
            text_color=self.ACCENT_COLOR
        )
        voice_label.pack(pady=(30, 10))
        
        self.voice_toggle = ctk.CTkSwitch(
            control_panel,
            text="Voice OFF",
            font=("Consolas", 12, "bold"),
            text_color=self.TEXT_COLOR,
            fg_color=self.ACCENT_2,
            progress_color=self.ACCENT_COLOR,
            button_color=self.PANEL_COLOR,
            button_hover_color=self.BG_COLOR,
            command=self.toggle_voice_mode
        )
        self.voice_toggle.pack(padx=20, pady=10)
        
        # Voice selector
        try:
            available_voices = self.voice.get_available_voices()
            if available_voices:
                voice_names = [v['name'] for v in available_voices]
                self.voice_ids = [v['id'] for v in available_voices]
                
                # Encontrar índice de la voz actual
                current_voice_id = self.voice.get_current_voice()
                default_index = 0
                if current_voice_id:
                    try:
                        default_index = self.voice_ids.index(current_voice_id)
                    except:
                        pass
                
                self.voice_selector = ctk.CTkOptionMenu(
                    control_panel,
                    values=voice_names,
                    fg_color=self.BG_COLOR,
                    button_color=self.ACCENT_COLOR,
                    button_hover_color=self.ACCENT_2,
                    text_color=self.TEXT_COLOR,
                    font=("Consolas", 9),
                    dropdown_font=("Consolas", 8),
                    corner_radius=10,
                    command=self.change_voice
                )
                self.voice_selector.set(voice_names[default_index])
                self.voice_selector.pack(padx=20, pady=5, fill="x")
        except Exception as e:
            print(f"⚠️ Error cargando selector de voz: {e}")
        
        # Stats panel
        stats_label = ctk.CTkLabel(
            control_panel,
            text="⟨ STATISTICS ⟩",
            font=("Consolas", 14, "bold"),
            text_color=self.ACCENT_COLOR
        )
        stats_label.pack(pady=(30, 10))
        
        stats_frame = ctk.CTkFrame(control_panel, fg_color=self.BG_COLOR, corner_radius=10)
        stats_frame.pack(padx=20, pady=10, fill="x")
        
        self.messages_label = ctk.CTkLabel(
            stats_frame,
            text="Messages: 0\nLearnings: 0\nIAs Active: 0",
            font=("Consolas", 10),
            text_color=self.TEXT_COLOR,
            justify="left"
        )
        self.messages_label.pack(pady=5)
        
        # Action buttons
        actions_label = ctk.CTkLabel(
            control_panel,
            text="⟨ ACTIONS ⟩",
            font=("Consolas", 14, "bold"),
            text_color=self.ACCENT_COLOR
        )
        actions_label.pack(pady=(30, 10))
        
        clear_btn = ctk.CTkButton(
            control_panel,
            text="Clear Chat",
            fg_color=self.BG_COLOR,
            hover_color=self.USER_BUBBLE,
            text_color=self.TEXT_COLOR,
            border_width=2,
            border_color=self.ACCENT_COLOR,
            corner_radius=10,
            font=("Consolas", 11),
            command=self.clear_chat
        )
        clear_btn.pack(padx=20, pady=5, fill="x")
        
        memory_btn = ctk.CTkButton(
            control_panel,
            text="View Memory",
            fg_color=self.BG_COLOR,
            hover_color=self.USER_BUBBLE,
            text_color=self.TEXT_COLOR,
            border_width=2,
            border_color=self.ACCENT_COLOR,
            corner_radius=10,
            font=("Consolas", 11),
            command=self.view_memory
        )
        memory_btn.pack(padx=20, pady=5, fill="x")
        
        # Botón de captura de pantalla
        screenshot_btn = ctk.CTkButton(
            control_panel,
            text="📸 Capture Screen",
            fg_color=self.ACCENT_2,
            hover_color=self.ACCENT_COLOR,
            text_color="#ffffff",
            border_width=0,
            corner_radius=10,
            font=("Consolas", 11, "bold"),
            command=self.capture_and_analyze
        )
        screenshot_btn.pack(padx=20, pady=5, fill="x")
        
        # Separador
        separator2 = ctk.CTkLabel(
            control_panel,
            text="━━━━━━━━━━━━━━━━━",
            font=("Consolas", 10),
            text_color="#333333"
        )
        separator2.pack(pady=10)
        
        # Botón de auto-análisis - destacado
        analysis_btn = ctk.CTkButton(
            control_panel,
            text="🔍 AUTO-ANALYSIS",
            fg_color=self.ACCENT_COLOR,
            hover_color="#00cc7f",
            text_color="#000000",
            border_width=2,
            border_color="#00ff9f",
            corner_radius=10,
            font=("Consolas", 12, "bold"),
            height=40,
            command=self.show_self_analysis
        )
        analysis_btn.pack(padx=20, pady=10, fill="x")
        
        # Footer info
        footer = ctk.CTkLabel(
            control_panel,
            text="v1.0.0 • Cyberpunk Edition",
            font=("Consolas", 9),
            text_color="#666666"
        )
        footer.pack(side="bottom", pady=20)
        
        # Welcome message y auto-análisis inicial
        self.add_system_message("🌟 Any está lista. ¡Holis, Adri!")
        self.add_system_message("\n💫 Iniciando auto-análisis del sistema...")
        
        # Mostrar auto-análisis en un thread para no bloquear la UI
        def show_startup_analysis():
            try:
                import time
                time.sleep(0.5)  # Pequeña pausa para que se vea el mensaje
                self.root.after(0, self._show_startup_analysis)
            except Exception as e:
                print(f"Error en análisis inicial: {e}")
        
        thread = threading.Thread(target=show_startup_analysis)
        thread.daemon = True
        thread.start()
        
    def add_message(self, sender: str, message: str, color: str):
        """Agrega un mensaje al chat estilo WhatsApp con burbujas de color"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.configure(state="normal")
        
        # Determinar alineación y color
        if sender == "Adri":
            # Mensaje del usuario - alineado a la derecha, fondo azul
            self.chat_display.insert("end", "\n")
            
            # Dividir mensaje en líneas para el wrap manual
            lines = message.split('\n')
            wrapped_lines = []
            for line in lines:
                if len(line) > 50:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line) + len(word) + 1 <= 50:
                            current_line += word + " "
                        else:
                            wrapped_lines.append(current_line.strip())
                            current_line = word + " "
                    if current_line:
                        wrapped_lines.append(current_line.strip())
                else:
                    wrapped_lines.append(line)
            
            # Calcular padding para alinear a la derecha
            max_line_length = max(len(line) for line in wrapped_lines) if wrapped_lines else 0
            max_line_length = max(max_line_length, len(sender) + len(timestamp) + 3)
            
            # Header con timestamp
            padding = 100 - max_line_length - 4
            self.chat_display.insert("end", " " * padding + f"╔{'═' * (max_line_length + 2)}╗\n")
            self.chat_display.insert("end", " " * padding + f"║ {sender} · {timestamp}".ljust(max_line_length + 2) + " ║\n")
            
            # Contenido del mensaje
            for line in wrapped_lines:
                self.chat_display.insert("end", " " * padding + f"║ {line}".ljust(max_line_length + 4) + "║\n")
            
            self.chat_display.insert("end", " " * padding + f"╚{'═' * (max_line_length + 2)}╝\n")
        else:
            # Mensaje de Any - alineado a la izquierda, fondo verde
            self.chat_display.insert("end", "\n")
            
            # Dividir mensaje en líneas
            lines = message.split('\n')
            wrapped_lines = []
            for line in lines:
                if len(line) > 75:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line) + len(word) + 1 <= 75:
                            current_line += word + " "
                        else:
                            wrapped_lines.append(current_line.strip())
                            current_line = word + " "
                    if current_line:
                        wrapped_lines.append(current_line.strip())
                else:
                    wrapped_lines.append(line)
            
            # Calcular ancho máximo
            max_line_length = max(len(line) for line in wrapped_lines) if wrapped_lines else 0
            max_line_length = max(max_line_length, len(sender) + len(timestamp) + 3)
            
            # Header con timestamp
            self.chat_display.insert("end", f"╔{'═' * (max_line_length + 2)}╗\n")
            self.chat_display.insert("end", f"║ {sender} · {timestamp}".ljust(max_line_length + 2) + " ║\n")
            
            # Contenido del mensaje
            for line in wrapped_lines:
                self.chat_display.insert("end", f"║ {line}".ljust(max_line_length + 4) + "║\n")
            
            self.chat_display.insert("end", f"╚{'═' * (max_line_length + 2)}╝\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        
    def add_system_message(self, message: str):
        """Agrega un mensaje del sistema"""
        self.chat_display.configure(state="normal")
        
        # Centrar mensajes del sistema
        lines = message.split('\n')
        for line in lines:
            if line.strip():
                # Calcular padding para centrar
                total_width = 100
                padding = max(0, (total_width - len(line)) // 2)
                self.chat_display.insert("end", " " * padding + f"🌟 {line}\n")
            else:
                self.chat_display.insert("end", "\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def toggle_vision_mode(self):
        """Activa/desactiva el modo visión automático"""
        self.vision_mode = self.vision_toggle.get()
        if self.vision_mode:
            self.vision_toggle.configure(text="Vision ON")
            self.add_system_message("👁️ Modo visión activado - Veré tu pantalla con cada mensaje")
        else:
            self.vision_toggle.configure(text="Vision OFF")
            self.add_system_message("💬 Modo visión desactivado - Solo responderé a tus mensajes")
    
    def toggle_voice_mode(self):
        """Activa/desactiva el modo voz automático"""
        self.voice_mode = self.voice_toggle.get()
        if self.voice_mode:
            self.voice_toggle.configure(text="Voice ON")
            self.add_system_message("🔊 Modo voz activado - Te hablaré con cada respuesta")
            self.voice.speak("Modo voz activado, boludo. Ahora te voy a hablar.")
        else:
            self.voice_toggle.configure(text="Voice OFF")
            self.add_system_message("🔇 Modo voz desactivado")
    
    def change_voice(self, selected_voice: str):
        """Cambia la voz de TTS"""
        try:
            # Obtener el índice de la voz seleccionada
            voice_names = [v['name'] for v in self.voice.get_available_voices()]
            index = voice_names.index(selected_voice)
            voice_id = self.voice_ids[index]
            
            # Cambiar la voz
            if self.voice.set_voice(voice_id):
                self.add_system_message(f"🎤 Voz cambiada")
                # Probar la nueva voz
                self.voice.speak("¡Holis! Esta es mi nueva voz.")
            else:
                self.add_system_message("❌ Error cambiando la voz")
        except Exception as e:
            self.add_system_message(f"❌ Error: {str(e)}")
    
    def start_listening(self):
        """Escucha por voz y transcribe al input"""
        if self.is_processing or self.voice.is_listening:
            return
        
        self.mic_button.configure(fg_color="#ff0000", text="⏺️")
        self.add_system_message("🎤 Escuchando... Hablá ahora")
        
        def on_listen_complete(text):
            # Restaurar botón
            self.root.after(0, lambda: self.mic_button.configure(fg_color=self.ACCENT_COLOR, text="🎤"))
            
            if text.startswith("❌") or text.startswith("⏱️"):
                self.root.after(0, lambda: self.add_system_message(text))
            else:
                # Poner texto en el input
                self.root.after(0, lambda: self.input_field.delete(0, "end"))
                self.root.after(0, lambda: self.input_field.insert(0, text))
                self.root.after(0, lambda: self.add_system_message(f"📝 Transcrito: {text}"))
        
        self.voice.listen_async(on_listen_complete, timeout=5)
        
    def send_message(self):
        """Envía un mensaje a Any"""
        if self.is_processing:
            return
            
        try:
            message = self.input_field.get().strip()
            if not message:
                return
            
            # Limitar longitud para evitar crashes
            if len(message) > 5000:
                self.add_system_message("⚠️ Mensaje muy largo. Máximo 5000 caracteres.")
                return
                
            # Limpiar input
            self.input_field.delete(0, "end")
            
            # Mostrar mensaje del usuario
            self.add_message("Adri", message, self.ACCENT_2)
            
            # Procesar en thread separado
            self.is_processing = True
            self.status_label.configure(text="● PROCESSING", text_color=self.ACCENT_2)
            thread = threading.Thread(target=self.process_message, args=(message,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"❌ Error en send_message: {e}")
            self.is_processing = False
            self.add_system_message(f"❌ Error enviando mensaje: {str(e)}")
        
    def process_message(self, message: str):
        """Procesa el mensaje usando el sistema de consciencia de Any"""
        try:
            # Validar longitud para evitar crashes
            if len(message) > 5000:
                self.root.after(0, lambda: self.add_system_message("⚠️ Mensaje demasiado largo"))
                self.is_processing = False
                self.root.after(0, lambda: self.status_label.configure(text="● ONLINE", text_color=self.ACCENT_COLOR))
                return
            
            # Detectar comandos especiales
            msg_lower = message.lower().strip()
            if msg_lower in ['/analisis', '/autoanálisis', '/status', '/capacidades', '/info']:
                self.root.after(0, lambda: self.show_self_analysis())
                self.is_processing = False
                self.root.after(0, lambda: self.status_label.configure(text="● ONLINE", text_color=self.ACCENT_COLOR))
                return
            
            if msg_lower in ['/ias', '/providers', '/modelos', '/ai']:
                summary = self.self_analysis.get_ai_status_summary()
                active_ais = self.self_analysis.get_active_ais()
                self.root.after(0, lambda: self.add_system_message(summary))
                for ai in active_ais:
                    info = f"  • {ai['name']}: {ai['model']} ({ai['type']}, {ai['cost']})"
                    self.root.after(0, lambda msg=info: self.add_system_message(msg))
                self.is_processing = False
                self.root.after(0, lambda: self.status_label.configure(text="● ONLINE", text_color=self.ACCENT_COLOR))
                return
            
            if msg_lower in ['/memoria', '/memory', '/mem']:
                self.root.after(0, lambda: self.show_memory_stats())
                self.is_processing = False
                self.root.after(0, lambda: self.status_label.configure(text="● ONLINE", text_color=self.ACCENT_COLOR))
                return
            
            # Si el modo visión está activado, capturar pantalla primero
            vision_context = ""
            if self.vision_mode:
                self.root.after(0, lambda: self.add_system_message("📸 Capturando pantalla..."))
                screenshot = self.vision.capture_screen()
                if screenshot:
                    # Crear contexto visual rápido
                    vision_prompt = f"""Analiza brevemente esta captura de pantalla y responde a: {message}
                    Contexto visual para entender mejor la pregunta del usuario."""
                    vision_context = self.vision.get_screen_description(self.ai, vision_prompt)
                    # Agregar contexto visual al mensaje
                    message = f"[VIENDO PANTALLA] {message}\n\nContexto visual: {vision_context[:500]}"
            
            system_prompt = self.personality.get_system_prompt()
            
            # MODO ASI: Consultar a TODAS las IAs simultáneamente
            self.root.after(0, lambda: self.add_system_message("🧠 Pensando..."))
            
            all_responses = self.consciousness.query_all_ais(message, system_prompt)
            
            # Any sintetiza y genera SU PROPIA respuesta
            response, analysis = self.consciousness.synthesize_response(all_responses, message)
            
            # Mostrar respuesta
            self.root.after(0, lambda: self.add_message("Any", response, self.ACCENT_COLOR))
            
            # Hablar si el modo voz está activado
            if self.voice_mode:
                self.voice.speak(response)
            
            # Actualizar stats
            msg_count = len(self.memory.conversations)
            consciousness_summary = self.consciousness.get_consciousness_summary()
            ias_active = len(analysis.get('providers_used', []))
            
            self.root.after(0, lambda: self.messages_label.configure(
                text=f"Messages: {msg_count}\nLearnings: {consciousness_summary['conceptos_aprendidos']}\nIAs Active: {ias_active}"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_system_message(f"❌ Error: {str(e)}"))
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.status_label.configure(text="● ONLINE", text_color=self.ACCENT_COLOR))
        
    def quick_vision(self):
        """Botón rápido de visión - captura y envía lo que el usuario está escribiendo"""
        if self.is_processing:
            return
        
        # Obtener el mensaje del input (si hay)
        user_message = self.input_field.get().strip()
        
        self.is_processing = True
        self.status_label.configure(text="● CAPTURING", text_color=self.ACCENT_2)
        self.add_system_message("👁️ Mirando tu pantalla...")
        
        # Limpiar input
        self.input_field.delete(0, "end")
        
        # Procesar en thread separado
        thread = threading.Thread(target=self._quick_vision_analysis, args=(user_message,))
        thread.daemon = True
        thread.start()
    
    def _quick_vision_analysis(self, user_message: str):
        """Análisis rápido de pantalla con contexto del mensaje (ejecuta en thread)"""
        try:
            # Capturar pantalla
            screenshot = self.vision.capture_screen()
            if not screenshot:
                self.root.after(0, lambda: self.add_system_message("❌ No pude capturar la pantalla"))
                return
            
            # Crear prompt personalizado basado en el mensaje del usuario
            if user_message:
                custom_prompt = f"""Estoy viendo mi pantalla y te pregunto: {user_message}
                
                Analizá esta captura de pantalla y respondeme en español argentino.
                Hablame como Any, con tu personalidad rosarina directa y copada."""
                self.root.after(0, lambda: self.add_message("Adri", f"[👁️ Mirando pantalla] {user_message}", self.ACCENT_2))
            else:
                custom_prompt = """Describí esta captura de pantalla en español argentino.
                Decime qué estoy viendo, qué programas están abiertos, y si ves algo importante.
                Hablame como Any, usando tu personalidad rosarina."""
                self.root.after(0, lambda: self.add_message("Adri", "[👁️ Mirando pantalla] ¿Qué ves?", self.ACCENT_2))
            
            # Analizar con visión
            description = self.vision.get_screen_description(self.ai, custom_prompt)
            
            # Guardar en memoria
            self.memory.save_conversation(
                f"[VISIÓN] {user_message if user_message else '¿Qué ves?'}",
                description
            )
            
            # Mostrar resultado
            self.root.after(0, lambda: self.add_message("Any", description, self.ACCENT_COLOR))
            
            # Actualizar stats
            msg_count = len(self.memory.conversations)
            consciousness_summary = self.consciousness.get_consciousness_summary()
            self.root.after(0, lambda: self.messages_label.configure(
                text=f"Messages: {msg_count}\nLearnings: {consciousness_summary['conceptos_aprendidos']}\nIAs Active: 1"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_system_message(f"❌ Error: {str(e)}"))
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.status_label.configure(text="● ONLINE", text_color=self.ACCENT_COLOR))
    
    def capture_and_analyze(self):
        """Captura la pantalla y la analiza (botón del panel)"""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.status_label.configure(text="● CAPTURING", text_color=self.ACCENT_2)
        self.add_system_message("📸 Capturando pantalla...")
        
        # Procesar en thread separado
        thread = threading.Thread(target=self._analyze_screen)
        thread.daemon = True
        thread.start()
    
    def _analyze_screen(self):
        """Analiza la pantalla capturada (ejecuta en thread)"""
        try:
            # Capturar y analizar
            description = self.vision.get_screen_description(self.ai)
            
            # Mostrar resultado
            self.root.after(0, lambda: self.add_system_message("👁️ Esto es lo que veo:"))
            self.root.after(0, lambda: self.add_message("Any", description, self.ACCENT_COLOR))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_system_message(f"❌ Error: {str(e)}"))
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.status_label.configure(text="● ONLINE", text_color=self.ACCENT_COLOR))
    
    def _show_startup_analysis(self):
        """Muestra un resumen del sistema al iniciar"""
        try:
            capabilities = self.self_analysis.get_capabilities()
            active_ais = self.self_analysis.get_active_ais()
            
            # Resumen breve
            self.add_system_message("\n╔════════════════════════════════════╗")
            self.add_system_message("║    SISTEMA INICIALIZADO ✓         ║")
            self.add_system_message("╚════════════════════════════════════╝")
            
            self.add_system_message(f"\n🧠 IAs Activas: {len(active_ais)}/{capabilities['ai_system']['total_ais_configured']}")
            for ai in active_ais:
                self.add_system_message(f"   ✓ {ai['name']}: {ai['model']}")
            
            self.add_system_message(f"\n🎯 Capacidades:")
            self.add_system_message(f"   {'✓' if capabilities['features']['vision_system'] else '✗'} Sistema de Visión")
            self.add_system_message(f"   {'✓' if capabilities['features']['voice_system'] else '✗'} Sistema de Voz")
            self.add_system_message(f"   {'✓' if capabilities['features']['consciousness'] else '✗'} Consciencia ASI")
            self.add_system_message(f"   {'✓' if capabilities['features']['auto_learning'] else '✗'} Auto-Aprendizaje")
            
            # Mostrar stats de memoria comprimida
            try:
                mem_stats = self.consciousness.compressed_memory.get_memory_stats()
                self.add_system_message(f"\n💾 Memoria Comprimida:")
                self.add_system_message(f"   {mem_stats['total_tokens']} tokens • {mem_stats['key_facts_count']} hechos • {mem_stats['file_size_kb']} KB")
            except:
                pass
            
            self.add_system_message(f"\n💡 Usá el botón 🔍 Auto-Analysis para ver más detalles")
            self.add_system_message(f"💡 O escribí /analisis, /ias, /memoria o /status\n")
            
        except Exception as e:
            self.add_system_message(f"⚠️ Error en análisis inicial: {str(e)}")
            print(f"Error detallado: {e}")
    
    def show_memory_stats(self):
        """Muestra estadísticas de la memoria comprimida"""
        try:
            stats = self.consciousness.compressed_memory.get_memory_stats()
            context = self.consciousness.compressed_memory.get_full_context()
            
            self.add_system_message("\n╔════════════════════════════════════╗")
            self.add_system_message("║    ESTADÍSTICAS DE MEMORIA        ║")
            self.add_system_message("╚════════════════════════════════════╝")
            
            self.add_system_message(f"\n💾 Tokens de Contexto: {stats['total_tokens']}")
            self.add_system_message(f"📊 Hechos Clave: {stats['key_facts_count']}")
            self.add_system_message(f"❤️ Preferencias: {stats['preferences_count']}")
            self.add_system_message(f"🔗 Relaciones: {stats['relationships_count']}")
            self.add_system_message(f"📦 Tamaño del archivo: {stats['file_size_kb']} KB")
            self.add_system_message(f"🕐 Última actualización: {stats['last_update']}")
            
            if context:
                self.add_system_message(f"\n🧠 Contexto Actual:")
                for line in context.split('\n'):
                    if line.strip():
                        self.add_system_message(f"   {line}")
            
            self.add_system_message(f"\n💡 La memoria comprimida es ultra-liviana y solo la IA la entiende")
            self.add_system_message(f"💡 Se actualiza automáticamente con cada conversación\n")
            
        except Exception as e:
            self.add_system_message(f"❌ Error mostrando estadísticas: {str(e)}")
            print(f"Error detallado: {e}")
    
    def show_self_analysis(self):
        """Muestra el auto-análisis del sistema"""
        try:
            # Obtener reporte completo
            report = self.self_analysis.generate_status_report()
            self.add_system_message(report)
            
            # También actualizar las stats en el panel
            capabilities = self.self_analysis.get_capabilities()
            active_count = capabilities['ai_system']['active_ais_count']
            total_count = capabilities['ai_system']['total_ais_configured']
            
            self.add_system_message(f"\n💡 Para activar más IAs, editá el archivo config.json")
            self.add_system_message(f"📊 {active_count}/{total_count} IAs disponibles están activas")
            
        except Exception as e:
            self.add_system_message(f"❌ Error en auto-análisis: {str(e)}")
            print(f"Error detallado: {e}")
    
    def clear_chat(self):
        """Limpia el chat"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.add_system_message("🌟 Chat limpio. ¡Empecemos de nuevo!")
        
    def view_memory(self):
        """Muestra las conversaciones recientes"""
        recent = self.memory.get_recent_conversations(5)
        if not recent:
            self.add_system_message("📝 No hay conversaciones guardadas")
            return
            
        self.add_system_message(f"📝 Últimas {len(recent)} conversaciones:")
        for conv in recent:
            self.add_message("Adri", conv['user'], self.ACCENT_2)
            self.add_message("Any", conv['any'], self.ACCENT_COLOR)
            
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


def main():
    """Función principal"""
    try:
        app = CyberpunkChatApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Cerrando Any...")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")


if __name__ == "__main__":
    main()
