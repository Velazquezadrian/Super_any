"""
Módulo de Conexión a IAs
Conecta a diferentes proveedores de IA (OpenAI, Anthropic, Google, Ollama, etc.)
"""

import json
from pathlib import Path
from typing import Optional
import requests


class AIConnector:
    """Conecta con diferentes proveedores de IA"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.providers = self.config.get('ai_providers', {})
    
    def _load_config(self, config_path: str) -> dict:
        """Carga la configuración"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def send_message(self, message: str, system_prompt: str, provider: str = None) -> Optional[str]:
        """
        Envía un mensaje a la IA seleccionada
        
        Args:
            message: Mensaje del usuario
            system_prompt: Prompt del sistema (personalidad de Any)
            provider: Proveedor de IA a usar (None = usar default)
        
        Returns:
            Respuesta de la IA o None si hay error
        """
        if provider is None:
            provider = self.config.get('default_provider', 'ollama')
        
        if provider not in self.providers:
            return f"Error: Proveedor '{provider}' no configurado"
        
        if not self.providers[provider].get('enabled', False):
            return f"Error: Proveedor '{provider}' no está habilitado"
        
        # Routing a cada proveedor
        try:
            if provider == "ollama":
                return self._connect_ollama(message, system_prompt)
            elif provider == "openai":
                return self._connect_openai(message, system_prompt)
            elif provider == "anthropic":
                return self._connect_anthropic(message, system_prompt)
            elif provider == "google":
                return self._connect_google(message, system_prompt)
            elif provider == "huggingface":
                return self._connect_huggingface(message, system_prompt)
            elif provider == "cohere":
                return self._connect_cohere(message, system_prompt)
            elif provider == "together":
                return self._connect_together(message, system_prompt)
            elif provider == "groq":
                return self._connect_groq(message, system_prompt)
            elif provider == "perplexity":
                return self._connect_perplexity(message, system_prompt)
            elif provider == "deepseek":
                return self._connect_deepseek(message, system_prompt)
            elif provider == "mistral":
                return self._connect_mistral(message, system_prompt)
            else:
                return f"Error: Proveedor '{provider}' no implementado"
        except Exception as e:
            return f"Error al conectar con {provider}: {str(e)}"
    
    def _connect_ollama(self, message: str, system_prompt: str) -> str:
        """Conecta con Ollama (local)"""
        config = self.providers['ollama']
        url = f"{config['api_url']}/api/generate"
        
        payload = {
            "model": config['model'],
            "prompt": f"{system_prompt}\n\nUsuario: {message}\n\nAsistente:",
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get('response', 'Sin respuesta')
        except requests.exceptions.ConnectionError:
            return "❌ Error: Ollama no está corriendo. Ejecutá 'ollama serve' en otra terminal."
        except Exception as e:
            return f"❌ Error con Ollama: {str(e)}"
    
    def _connect_openai(self, message: str, system_prompt: str) -> str:
        """Conecta con OpenAI API"""
        config = self.providers['openai']
        api_key = config.get('api_key', '')
        
        if not api_key:
            return "❌ OpenAI no configurado. Agregá tu API key en config.json"
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model=config['model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error con OpenAI: {str(e)}"
    
    def _connect_anthropic(self, message: str, system_prompt: str) -> str:
        """Conecta con Anthropic API"""
        config = self.providers['anthropic']
        api_key = config.get('api_key', '')
        
        if not api_key:
            return "❌ Anthropic no configurado. Agregá tu API key en config.json"
        
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model=config['model'],
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"❌ Error con Anthropic: {str(e)}"
    
    def _connect_google(self, message: str, system_prompt: str) -> str:
        """Conecta con Google Gemini API"""
        config = self.providers['google']
        api_key = config.get('api_key', '')
        
        if not api_key:
            return "❌ Google Gemini no configurado. Agregá tu API key en config.json"
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Listar modelos disponibles y usar el primero que funcione
            try:
                available_models = genai.list_models()
                for model_info in available_models:
                    if 'generateContent' in model_info.supported_generation_methods:
                        model = genai.GenerativeModel(model_info.name)
                        full_prompt = f"{system_prompt}\n\nUsuario: {message}"
                        response = model.generate_content(full_prompt)
                        return response.text
            except:
                pass
            
            # Si lo anterior falla, intentar directamente con gemini-pro
            model = genai.GenerativeModel('gemini-pro')
            full_prompt = f"{system_prompt}\n\nUsuario: {message}"
            response = model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Error con Google Gemini: {str(e)}"
    
    def _connect_huggingface(self, message: str, system_prompt: str) -> str:
        """Conecta con Hugging Face API"""
        config = self.providers['huggingface']
        api_key = config.get('api_key', '')
        
        if not api_key:
            return "❌ Hugging Face no configurado. Agregá tu API key en config.json"
        
        url = f"https://api-inference.huggingface.co/models/{config['model']}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        payload = {
            "inputs": f"{system_prompt}\n\nUsuario: {message}\n\nAsistente:",
            "parameters": {"max_new_tokens": 500}
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result[0].get('generated_text', 'Sin respuesta')
        except Exception as e:
            return f"❌ Error con Hugging Face: {str(e)}"
    
    def _connect_cohere(self, message: str, system_prompt: str) -> str:
        """Conecta con Cohere API"""
        config = self.providers['cohere']
        api_key = config.get('api_key', '')
        
        if not api_key:
            return "❌ Cohere no configurado. Agregá tu API key en config.json"
        
        try:
            import cohere
            co = cohere.Client(api_key)
            
            full_prompt = f"{system_prompt}\n\nUsuario: {message}\n\nAsistente:"
            response = co.generate(
                model=config['model'],
                prompt=full_prompt,
                max_tokens=500,
                temperature=0.7
            )
            return response.generations[0].text.strip()
        except Exception as e:
            return f"❌ Error con Cohere: {str(e)}"
    
    def _connect_together(self, message: str, system_prompt: str) -> str:
        """Conecta con Together AI API"""
        config = self.providers['together']
        api_key = config.get('api_key', '')
        
        if not api_key:
            return "❌ Together AI no configurado. Agregá tu API key en config.json"
        
        # TODO: Implementar Together AI cuando tengas API key
        return "❌ Together AI: Implementación pendiente"
    
    def _connect_groq(self, message: str, system_prompt: str) -> str:
        """Conecta con Groq (ultra rápido, gratis)"""
        try:
            from groq import Groq
            config = self.providers['groq']
            client = Groq(api_key=config['api_key'])
            
            response = client.chat.completions.create(
                model=config.get('model', 'llama-3.1-70b-versatile'),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error en Groq: {str(e)}"
    
    def _connect_perplexity(self, message: str, system_prompt: str) -> str:
        """Conecta con Perplexity (búsqueda en tiempo real)"""
        try:
            import requests
            config = self.providers['perplexity']
            
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers={
                    'Authorization': f'Bearer {config["api_key"]}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': config.get('model', 'llama-3.1-sonar-small-128k-online'),
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': message}
                    ]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"❌ Error Perplexity: {response.status_code}"
        except Exception as e:
            return f"❌ Error en Perplexity: {str(e)}"
    
    def _connect_deepseek(self, message: str, system_prompt: str) -> str:
        """Conecta con DeepSeek (modelo chino gratis)"""
        try:
            import requests
            config = self.providers['deepseek']
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {config["api_key"]}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': config.get('model', 'deepseek-chat'),
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': message}
                    ],
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"❌ Error DeepSeek: {response.status_code}"
        except Exception as e:
            return f"❌ Error en DeepSeek: {str(e)}"
    
    def _connect_mistral(self, message: str, system_prompt: str) -> str:
        """Conecta con Mistral AI (modelos europeos)"""
        try:
            from mistralai.client import MistralClient
            from mistralai.models.chat_completion import ChatMessage
            
            config = self.providers['mistral']
            client = MistralClient(api_key=config['api_key'])
            
            messages = [
                ChatMessage(role='system', content=system_prompt),
                ChatMessage(role='user', content=message)
            ]
            
            response = client.chat(
                model=config.get('model', 'mistral-small-latest'),
                messages=messages
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error en Mistral: {str(e)}"
    
    def send_audio(self, audio_file_path: str, system_prompt: str, provider: str = "google") -> str:
        """
        Envía un archivo de audio directamente a la IA para análisis
        (Sin transcripción - la IA analiza el audio)
        
        Args:
            audio_file_path: Ruta al archivo de audio
            system_prompt: Instrucciones para la IA
            provider: Proveedor (solo Google Gemini soporta audio nativo)
        
        Returns:
            Análisis del audio por la IA
        """
        if provider != "google":
            return "❌ Solo Google Gemini soporta análisis de audio nativo"
        
        config = self.providers['google']
        api_key = config.get('api_key', '')
        
        if not api_key:
            return "❌ Google Gemini no configurado"
        
        try:
            import google.generativeai as genai
            from pathlib import Path
            
            genai.configure(api_key=api_key)
            
            # Probar diferentes modelos en orden de preferencia
            models_to_try = [
                'gemini-1.5-flash',
                'gemini-1.5-pro', 
                'gemini-pro',
                'models/gemini-pro'
            ]
            
            last_error = None
            for model_name in models_to_try:
                try:
                    print(f"🔄 Intentando con modelo: {model_name}")
                    
                    # Subir el archivo de audio
                    audio_file = genai.upload_file(path=audio_file_path)
                    
                    model = genai.GenerativeModel(model_name)
                    
                    prompt = f"""{system_prompt}

Instrucciones especiales:
🎤 Te estoy enviando un AUDIO de voz. Analiza:
1. El TONO emocional (¿suena feliz, triste, enojado, nervioso, calmado?)
2. La INTENCIÓN (¿qué quiere decir/pedir/expresar?)
3. El CONTEXTO (¿de qué está hablando?)
4. Cualquier EMOCIÓN o SENTIMIENTO que detectes

Respondé naturalmente basándote en lo que escuchaste, como si fuera un mensaje de voz de WhatsApp.
"""
                    
                    response = model.generate_content([prompt, audio_file])
                    
                    # Eliminar el archivo temporal de Google
                    try:
                        audio_file.delete()
                    except:
                        pass
                    
                    print(f"✅ Éxito con modelo: {model_name}")
                    return response.text
                    
                except Exception as e:
                    last_error = e
                    error_str = str(e)
                    
                    # Si es error de cuota, informar y probar siguiente
                    if "quota" in error_str.lower() or "429" in error_str:
                        print(f"⚠️ Cuota excedida en {model_name}, probando siguiente...")
                        continue
                    # Si es error de modelo no encontrado, probar siguiente
                    elif "not found" in error_str.lower() or "404" in error_str:
                        print(f"⚠️ Modelo {model_name} no disponible, probando siguiente...")
                        continue
                    else:
                        # Otro error, probar siguiente de todas formas
                        print(f"⚠️ Error en {model_name}: {error_str[:100]}")
                        continue
            
            # Si ningún modelo funcionó, retornar error
            return f"❌ No pude analizar el audio con ningún modelo de Gemini. Último error: {str(last_error)[:200]}"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"❌ Error analizando audio: {str(e)}"
    
    def list_available_providers(self) -> list:
        """Lista los proveedores disponibles y habilitados"""
        return [
            name for name, config in self.providers.items()
            if config.get('enabled', False)
        ]
    
    def list_all_providers(self) -> dict:
        """Lista TODOS los proveedores con su estado"""
        result = {}
        for name, config in self.providers.items():
            result[name] = {
                'enabled': config.get('enabled', False),
                'cost': config.get('cost', 'unknown'),
                'type': config.get('type', 'unknown'),
                'model': config.get('model', 'unknown')
            }
        return result
