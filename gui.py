"""
Any App - GUI Cyberpunk/Watch Dogs 2 Style
Interfaz gráfica moderna y futurista para Any
"""

import customtkinter as ctk
from tkinter import scrolledtext
import threading
from datetime import datetime
from any_core.personality import Personality
from any_core.memory import Memory
from any_core.ai_connector import AIConnector
from any_core.executor import Executor
from any_core.consciousness import Consciousness
from any_core.vision import VisionSystem
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
        
        # Variables
        self.current_provider = ctk.StringVar(value=config.get('default_provider', 'google'))
        self.is_processing = False
        self.vision_mode = False  # Modo visión activado/desactivado
        
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
            font=("Consolas", 12),
            corner_radius=10,
            wrap="word"
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
        
        # Footer info
        footer = ctk.CTkLabel(
            control_panel,
            text="v1.0.0 • Cyberpunk Edition",
            font=("Consolas", 9),
            text_color="#666666"
        )
        footer.pack(side="bottom", pady=20)
        
        # Welcome message
        self.add_system_message("🌟 Any está lista. ¡Holis, Adri!")
        
    def add_message(self, sender: str, message: str, color: str):
        """Agrega un mensaje al chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n[{timestamp}] {sender}:\n{message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        
    def add_system_message(self, message: str):
        """Agrega un mensaje del sistema"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n🌟 {message}\n")
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
        
    def send_message(self):
        """Envía un mensaje a Any"""
        if self.is_processing:
            return
            
        message = self.input_field.get().strip()
        if not message:
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
        
    def process_message(self, message: str):
        """Procesa el mensaje usando el sistema de consciencia de Any"""
        try:
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
    app = CyberpunkChatApp()
    app.run()


if __name__ == "__main__":
    main()
