"""
Módulo de Voz de Any
Text-to-Speech (TTS) y Speech-to-Text (STT)
"""

import os
import threading
from pathlib import Path
import queue


class VoiceSystem:
    """Sistema de voz para Any - TTS y STT"""
    
    def __init__(self):
        self.is_speaking = False
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Configuración de voz
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None
        
        self._init_tts()
        self._init_stt()
    
    def _init_tts(self):
        """Inicializa el sistema de Text-to-Speech"""
        # Modo de TTS: 'gtts' (Google TTS - mejor calidad) o 'pyttsx3' (offline)
        self.tts_mode = 'gtts'  # Usar Google TTS por defecto
        self.selected_gtts_lang = 'es'  # Español (femenino por defecto)
        self.selected_gtts_tld = 'com.mx'  # Top-level domain para acento mexicano
        
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Configurar voz (buscar voces en español)
            voices = self.tts_engine.getProperty('voices')
            
            # Intentar encontrar voz femenina en español
            spanish_voice = None
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'es' in voice.languages:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        spanish_voice = voice.id
                        break
            
            # Si no hay voz en español, usar la primera femenina disponible
            if not spanish_voice:
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        spanish_voice = voice.id
                        break
            
            if spanish_voice:
                self.tts_engine.setProperty('voice', spanish_voice)
            
            # Configurar velocidad y volumen
            self.tts_engine.setProperty('rate', 160)  # Velocidad de habla
            self.tts_engine.setProperty('volume', 0.9)  # Volumen
            
            print("✅ TTS inicializado (pyttsx3 + Google TTS)")
        except Exception as e:
            print(f"❌ Error inicializando TTS: {e}")
            self.tts_engine = None
    
    def _init_stt(self):
        """Inicializa el sistema de Speech-to-Text"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Ajustar para ruido ambiente
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("✅ STT inicializado")
        except Exception as e:
            print(f"❌ Error inicializando STT: {e}")
            self.recognizer = None
            self.microphone = None
    
    def speak(self, text: str, async_mode: bool = True):
        """
        Convierte texto a voz
        
        Args:
            text: Texto a decir
            async_mode: Si True, habla en background sin bloquear
        """
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str):
        """Habla de forma sincrónica (bloquea hasta terminar)"""
        try:
            self.is_speaking = True
            
            if self.tts_mode == 'gtts':
                # Usar Google TTS (mejor calidad, voces naturales)
                self._speak_with_gtts(text)
            else:
                # Usar pyttsx3 (offline, voces robóticas)
                if self.tts_engine:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Error hablando: {e}")
        finally:
            self.is_speaking = False
    
    def _speak_with_gtts(self, text: str):
        """Habla usando Google TTS (requiere internet)"""
        try:
            from gtts import gTTS
            import pygame
            import tempfile
            import os
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
            
            # Generar audio con Google TTS
            tts = gTTS(text=text, lang=self.selected_gtts_lang, tld=self.selected_gtts_tld, slow=False)
            tts.save(temp_file)
            
            # Reproducir audio
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Esperar a que termine
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Limpiar
            pygame.mixer.quit()
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"❌ Error con Google TTS: {e}")
            # Fallback a pyttsx3
            if self.tts_engine:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> str:
        """
        Escucha y convierte voz a texto
        
        Args:
            timeout: Segundos a esperar por voz
            phrase_time_limit: Máximo de segundos de la frase
            
        Returns:
            Texto reconocido o mensaje de error
        """
        if not self.recognizer or not self.microphone:
            return "❌ Micrófono no disponible"
        
        try:
            self.is_listening = True
            
            with self.microphone as source:
                print("🎤 Escuchando...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Procesando audio...")
            
            # Intentar reconocer en español
            try:
                text = self.recognizer.recognize_google(audio, language='es-AR')
                return text
            except:
                # Si falla español argentino, intentar español general
                text = self.recognizer.recognize_google(audio, language='es-ES')
                return text
                
        except Exception as e:
            if "timed out" in str(e).lower():
                return "⏱️ No escuché nada"
            else:
                return f"❌ Error: {str(e)}"
        finally:
            self.is_listening = False
    
    def listen_async(self, callback, timeout: int = 5):
        """
        Escucha en modo asíncrono y llama al callback con el resultado
        
        Args:
            callback: Función a llamar con el texto reconocido
            timeout: Segundos a esperar
        """
        def listen_thread():
            result = self.listen(timeout=timeout)
            callback(result)
        
        thread = threading.Thread(target=listen_thread)
        thread.daemon = True
        thread.start()
    
    def stop_speaking(self):
        """Detiene la voz actual"""
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
                self.is_speaking = False
            except:
                pass
    
    def set_voice_speed(self, speed: int):
        """
        Cambia la velocidad de habla
        
        Args:
            speed: Velocidad (100-300, default 160)
        """
        if self.tts_engine:
            self.tts_engine.setProperty('rate', speed)
    
    def set_volume(self, volume: float):
        """
        Cambia el volumen
        
        Args:
            volume: Volumen (0.0 a 1.0)
        """
        if self.tts_engine:
            self.tts_engine.setProperty('volume', volume)
    
    def get_available_voices(self) -> list:
        """
        Obtiene lista de voces disponibles (Google TTS + pyttsx3)
        
        Returns:
            Lista de diccionarios con info de cada voz
        """
        voice_list = []
        
        # Voces de Google TTS (online, mejor calidad)
        # Formato: gtts-{lang}-{tld}
        google_voices = [
            {'id': 'gtts-es-com.mx', 'name': '🌟 Google Spanish Mexico (Female)', 'gender': 'Female', 'type': 'gtts'},
            {'id': 'gtts-es-com.ar', 'name': '🌟 Google Spanish Argentina (Female)', 'gender': 'Female', 'type': 'gtts'},
            {'id': 'gtts-es-es', 'name': '🌟 Google Spanish Spain (Female)', 'gender': 'Female', 'type': 'gtts'},
            {'id': 'gtts-es-us', 'name': '🌟 Google Spanish US (Female)', 'gender': 'Female', 'type': 'gtts'},
        ]
        voice_list.extend(google_voices)
        
        # Voces de pyttsx3 (offline, más robóticas)
        if self.tts_engine:
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                voice_info = {
                    'id': voice.id,
                    'name': f"💻 {voice.name[:40]}",
                    'languages': voice.languages if hasattr(voice, 'languages') else [],
                    'gender': 'Female' if 'female' in voice.name.lower() or 'zira' in voice.name.lower() else 'Male',
                    'type': 'pyttsx3'
                }
                voice_list.append(voice_info)
        
        return voice_list
    
    def set_voice(self, voice_id: str):
        """
        Cambia la voz actual
        
        Args:
            voice_id: ID de la voz a usar (ej: gtts-es-com.mx)
        """
        try:
            if voice_id.startswith('gtts-'):
                # Es una voz de Google TTS
                self.tts_mode = 'gtts'
                # Extraer idioma y tld (ej: gtts-es-com.mx -> lang='es', tld='com.mx')
                parts = voice_id.replace('gtts-', '').split('-', 1)
                self.selected_gtts_lang = parts[0]  # 'es'
                self.selected_gtts_tld = parts[1] if len(parts) > 1 else 'com'  # 'com.mx'
                return True
            else:
                # Es una voz de pyttsx3
                if self.tts_engine:
                    self.tts_mode = 'pyttsx3'
                    self.tts_engine.setProperty('voice', voice_id)
                    return True
        except Exception as e:
            print(f"❌ Error cambiando voz: {e}")
            return False
        return False
    
    def get_current_voice(self) -> str:
        """Retorna el ID de la voz actual"""
        if self.tts_mode == 'gtts':
            return f'gtts-{self.selected_gtts_lang}-{self.selected_gtts_tld}'
        elif self.tts_engine:
            return self.tts_engine.getProperty('voice')
        return None
