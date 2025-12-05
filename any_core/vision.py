"""
Módulo de Visión de Any
Captura y analiza la pantalla del usuario para dar consejos en vivo
"""

import io
import base64
from PIL import ImageGrab, Image
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


class VisionSystem:
    """Sistema de visión de Any para capturar y analizar pantalla"""
    
    def __init__(self):
        self.screenshots_dir = Path("data/screenshots")
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.last_screenshot = None
        
    def capture_screen(self, save: bool = False) -> Optional[Image.Image]:
        """
        Captura la pantalla completa
        
        Args:
            save: Si True, guarda la captura en disco
            
        Returns:
            Imagen capturada o None si hay error
        """
        try:
            # Capturar pantalla
            screenshot = ImageGrab.grab()
            
            # Reducir tamaño para enviar a IAs (ancho máximo 1280px)
            if screenshot.width > 1280:
                ratio = 1280 / screenshot.width
                new_size = (1280, int(screenshot.height * ratio))
                screenshot = screenshot.resize(new_size, Image.Resampling.LANCZOS)
            
            self.last_screenshot = screenshot
            
            # Guardar si se solicita
            if save:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = self.screenshots_dir / f"capture_{timestamp}.png"
                screenshot.save(filepath)
            
            return screenshot
        except Exception as e:
            print(f"❌ Error capturando pantalla: {e}")
            return None
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> Optional[Image.Image]:
        """
        Captura una región específica de la pantalla
        
        Args:
            x, y: Coordenadas de la esquina superior izquierda
            width, height: Dimensiones de la región
            
        Returns:
            Imagen capturada o None si hay error
        """
        try:
            bbox = (x, y, x + width, y + height)
            screenshot = ImageGrab.grab(bbox=bbox)
            self.last_screenshot = screenshot
            return screenshot
        except Exception as e:
            print(f"❌ Error capturando región: {e}")
            return None
    
    def image_to_base64(self, image: Image.Image) -> str:
        """
        Convierte una imagen a base64 para enviar a IAs
        
        Args:
            image: Imagen PIL
            
        Returns:
            String base64 de la imagen
        """
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')
    
    def get_screen_description(self, ai_connector, custom_prompt: str = None) -> str:
        """
        Captura la pantalla y usa visión de IA para describirla
        
        Args:
            ai_connector: Instancia de AIConnector
            custom_prompt: Prompt personalizado (por defecto: descripción general)
            
        Returns:
            Descripción de la pantalla por la IA
        """
        screenshot = self.capture_screen()
        if not screenshot:
            return "❌ No pude capturar la pantalla"
        
        # Convertir a base64
        img_base64 = self.image_to_base64(screenshot)
        
        # Prompt por defecto
        if custom_prompt is None:
            custom_prompt = """Describí esta captura de pantalla en español argentino.
            Decime qué estoy viendo, qué programas están abiertos, y si ves algo importante o raro.
            Hablame como Any, usando tu personalidad rosarina."""
        
        # Usar Google Gemini con visión (es el que mejor funciona gratis)
        try:
            import google.generativeai as genai
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            
            # Configurar Gemini
            config = ai_connector.providers.get('google', {})
            if not config.get('enabled', False):
                return "❌ Google Gemini no está habilitado (necesario para visión)"
            
            genai.configure(api_key=config['api_key'])
            
            # Usar modelo con visión más actualizado
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Convertir base64 a objeto de imagen para Gemini
            image_parts = [{
                'mime_type': 'image/png',
                'data': base64.b64decode(img_base64)
            }]
            
            response = model.generate_content(
                [custom_prompt, image_parts[0]],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            return response.text
            
        except Exception as e:
            return f"❌ Error analizando pantalla: {str(e)}"
    
    def get_last_screenshot(self) -> Optional[Image.Image]:
        """Retorna la última captura de pantalla"""
        return self.last_screenshot
