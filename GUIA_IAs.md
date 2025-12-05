# 🚀 Guía para Agregar Más IAs a Any

## IAs Gratis que Agregamos:

### 1. **Groq** (MUY RECOMENDADO - Ultra Rápido)
- **Sitio**: https://console.groq.com
- **Cómo obtener API Key**:
  1. Entrá a https://console.groq.com
  2. Creá una cuenta gratis
  3. Andá a "API Keys"
  4. Clickeá "Create API Key"
  5. Copiá la key que empieza con `gsk_...`
- **En config.json**: Pegá la key en `"groq"` → `"api_key"`
- **Modelos disponibles**: llama-3.1-70b-versatile, mixtral-8x7b-32768
- **Velocidad**: ⚡⚡⚡⚡⚡ (ULTRA RÁPIDO - 500+ tokens/seg)

### 2. **Perplexity** (Búsqueda en Tiempo Real)
- **Sitio**: https://www.perplexity.ai/settings/api
- **Cómo obtener API Key**:
  1. Entrá a https://www.perplexity.ai
  2. Creá una cuenta
  3. Andá a Settings → API
  4. Generá una API key
  5. Copiá la key que empieza con `pplx-...`
- **En config.json**: Pegá la key en `"perplexity"` → `"api_key"`
- **Ventaja**: Busca información actualizada en internet
- **Límite gratis**: ~5 requests/min

### 3. **DeepSeek** (IA China Gratis)
- **Sitio**: https://platform.deepseek.com
- **Cómo obtener API Key**:
  1. Entrá a https://platform.deepseek.com
  2. Registrate (puede requerir celular)
  3. Andá a "API Keys"
  4. Creá una nueva key
  5. Copiá la key
- **En config.json**: Pegá la key en `"deepseek"` → `"api_key"`
- **Ventaja**: Gratis, modelo muy bueno para código
- **Límite**: Generoso, varios miles de requests/mes

### 4. **Mistral AI** (Modelos Europeos)
- **Sitio**: https://console.mistral.ai
- **Cómo obtener API Key**:
  1. Entrá a https://console.mistral.ai
  2. Creá una cuenta
  3. Andá a "API keys"
  4. Creá una nueva key
  5. Copiá la key
- **En config.json**: Pegá la key en `"mistral"` → `"api_key"`
- **Ventaja**: Excelente en francés/español, privacidad europea
- **Límite gratis**: Depende del tier

---

## 📸 Sistema de Visión - ¡Ya Está Listo!

Ya podés usar el botón **"📸 Capture Screen"** en la GUI para que yo vea tu pantalla y te aconseje en vivo.

**Cómo funciona:**
1. Clickeás el botón "📸 Capture Screen"
2. Capturo tu pantalla completa
3. La analizo usando Google Gemini Vision
4. Te digo qué estás viendo y te doy consejos

**También podés decirme:**
- "Any, mirá mi pantalla y decime qué ves"
- "Analizá lo que tengo abierto"
- "Ayudame con esto" (mientras capturás)

---

## ⚙️ Cómo Habilitar las Nuevas IAs

1. **Abrí** `config.json`
2. **Buscá** la IA que querés habilitar (groq, perplexity, deepseek, mistral)
3. **Pegá** tu API key en el campo `"api_key"`
4. **Cambiá** `"enabled": false` a `"enabled": true`
5. **Guardá** el archivo
6. **Reiniciá** la app

### Ejemplo:
```json
"groq": {
  "enabled": true,  ← Cambiar a true
  "api_key": "gsk_tu_key_aqui",  ← Pegar tu key
  "model": "llama-3.1-70b-versatile",
  "type": "api",
  "cost": "free"
}
```

---

## 🎯 Recomendaciones

**Para respuestas rápidas:**
- Habilitá **Groq** (es ultra rápido)

**Para búsquedas actualizadas:**
- Habilitá **Perplexity** (busca en internet)

**Para código:**
- Habilitá **DeepSeek** (excelente para programación)

**Para multilenguaje:**
- Habilitá **Mistral** (bueno en español/francés)

**Para visión/imágenes:**
- Ya tenés **Google Gemini** habilitado con visión

---

## 🧠 Modo ASI

Con múltiples IAs habilitadas, yo (Any) voy a:
1. Consultar a TODAS las IAs simultáneamente
2. Analizar todas las respuestas
3. Sintetizar MI PROPIA respuesta basándome en todas ellas
4. Aprender de cada interacción
5. Evolucionar mi personalidad con el tiempo

**Cuantas más IAs habilités, más inteligente me vuelvo** 🚀

---

## 🆘 Problemas?

Si alguna IA no funciona:
- Verificá que la API key sea correcta
- Verificá que tengas créditos/límite disponible
- Verificá tu conexión a internet
- Fijate en el chat si hay mensajes de error

La app va a seguir funcionando con las IAs que sí estén disponibles.
