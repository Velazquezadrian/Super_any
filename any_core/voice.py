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
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10, save_audio: bool = True) -> dict:
        """
        Escucha y guarda el audio para análisis directo de IA (sin transcribir)
        
        Args:
            timeout: Segundos a esperar por voz
            phrase_time_limit: Máximo de segundos de la frase
            save_audio: Si True, guarda el audio en archivo temporal
            
        Returns:
            Dict con 'audio_file' (ruta al archivo de audio)
        """
        if not self.recognizer or not self.microphone:
            return {
                "error": "❌ Micrófono no disponible",
                "audio_file": None
            }
        
        try:
            self.is_listening = True
            
            with self.microphone as source:
                print("🎤 Escuchando...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("💾 Guardando audio para análisis de IA...")
            
            # Guardar audio en archivo temporal
            audio_file = None
            if save_audio:
                try:
                    import tempfile
                    import wave
                    
                    # Crear archivo temporal WAV
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                    audio_file = temp_file.name
                    temp_file.close()
                    
                    # Guardar audio en formato WAV
                    with wave.open(audio_file, 'wb') as wf:
                        wf.setnchannels(1)  # Mono
                        wf.setsampwidth(2)  # 16-bit
                        wf.setframerate(audio.sample_rate)
                        wf.writeframes(audio.frame_data)
                    
                    print(f"✅ Audio guardado: {audio_file}")
                    
                except Exception as e:
                    print(f"⚠️ Error guardando audio: {e}")
                    import traceback
                    traceback.print_exc()
            
            return {
                "audio_file": audio_file,
                "success": True
            }
                
        except Exception as e:
            if "timed out" in str(e).lower():
                return {
                    "error": "⏱️ No escuché nada",
                    "audio_file": None,
                    "success": False
                }
            else:
                return {
                    "error": f"❌ Error: {str(e)}",
                    "audio_file": None,
                    "success": False
                }
        finally:
            self.is_listening = False
    
    def _analyze_audio(self, audio) -> dict:
        """
        Analiza características del audio (volumen, duración, tono estimado)
        
        Returns:
            Dict con análisis: volumen, duración, tono, emoción estimada
        """
        try:
            import numpy as np
            
            # Convertir audio a array numpy de forma segura
            try:
                audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
            except Exception as e:
                print(f"⚠️ Error convirtiendo audio a numpy: {e}")
                raise
            
            # Calcular duración
            sample_rate = audio.sample_rate if hasattr(audio, 'sample_rate') else 16000
            duration = len(audio_data) / sample_rate if len(audio_data) > 0 else 0
            
            if duration == 0 or len(audio_data) == 0:
                raise Exception("Audio vacío")
            
            # Calcular volumen promedio (RMS) con manejo seguro
            audio_float = audio_data.astype(float)
            rms = np.sqrt(np.mean(audio_float**2))
            
            # Evitar log(0) y valores negativos
            if rms <= 0:
                rms = 1
            volume_db = 20 * np.log10(rms)
            
            # Clasificar volumen con rangos más realistas
            if volume_db < 30:
                volume_level = "Muy Bajo"
            elif volume_db < 45:
                volume_level = "Bajo"
            elif volume_db < 60:
                volume_level = "Normal"
            elif volume_db < 75:
                volume_level = "Alto"
            else:
                volume_level = "Muy Alto"
            
            # Estimar velocidad de habla (cambios de energía)
            if len(audio_data) > 1:
                energy_changes = np.sum(np.abs(np.diff(audio_data))) / len(audio_data)
            else:
                energy_changes = 0
            
            if energy_changes > 100:
                speech_rate = "Rápido"
            elif energy_changes > 50:
                speech_rate = "Normal"
            else:
                speech_rate = "Lento"
            
            # Estimar tono general
            positive_samples = np.sum(audio_data > 0)
            positive_ratio = positive_samples / len(audio_data) if len(audio_data) > 0 else 0.5
            
            if positive_ratio > 0.55:
                tone_estimate = "Alto"
            elif positive_ratio < 0.45:
                tone_estimate = "Bajo"
            else:
                tone_estimate = "Medio"
            
            # Estimar emoción combinando indicadores
            emotion = self._estimate_emotion(volume_level, speech_rate, tone_estimate, duration)
            
            return {
                "duration": duration,
                "volume_db": volume_db,
                "volume_level": volume_level,
                "speech_rate": speech_rate,
                "tone_estimate": tone_estimate,
                "emotion_estimate": emotion
            }
            
        except Exception as e:
            print(f"⚠️ Error en análisis de audio: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _estimate_emotion(self, volume, rate, tone, duration) -> str:
        """Estima la emoción probable basado en características de audio"""
        
        # Feliz/Emocionado: Alto volumen, rápido, tono alto
        if "Alto" in volume and "Rápido" in rate and "Alto" in tone:
            return "Feliz/Emocionado 😄"
        
        # Enojado: Muy alto volumen, rápido, tono variable
        if "Muy Alto" in volume and "Rápido" in rate:
            return "Enojado/Frustrado 😠"
        
        # Triste: Bajo volumen, lento, tono bajo
        if "Bajo" in volume and "Lento" in rate and "Bajo" in tone:
            return "Triste/Desanimado 😔"
        
        # Nervioso: Rápido, volumen variable
        if "Rápido" in rate and duration < 3:
            return "Nervioso/Ansioso 😰"
        
        # Cansado: Lento, bajo volumen
        if "Lento" in rate and "Bajo" in volume:
            return "Cansado/Aburrido 😴"
        
        # Sorprendido: Volumen alto, tono alto, corto
        if "Alto" in volume and "Alto" in tone and duration < 2:
            return "Sorprendido 😮"
        
        # Calmado: Volumen normal, velocidad normal
        if "Normal" in volume and "Normal" in rate:
            return "Calmado/Neutral 😊"
        
        return "Neutral 😐"
    
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
