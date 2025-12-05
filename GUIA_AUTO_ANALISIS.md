# Guía de Auto-Análisis de Any

## ¿Qué es el Auto-Análisis?

El sistema de auto-análisis permite que **Any pueda conocerse a sí misma**. Puede saber:
- Qué IAs tiene disponibles y cuáles están activas
- Qué capacidades tiene (visión, voz, memoria, etc.)
- Qué versión está ejecutando
- Qué permisos tiene habilitados
- Estado de su configuración

## ¿Cómo funciona?

### 1. Auto-Análisis Manual

Podés solicitar el auto-análisis de 3 formas:

#### **Botón en la GUI**
- Hacé clic en el botón **🔍 Auto-Analysis** en el panel derecho
- Se mostrará un reporte completo en el chat

#### **Comandos especiales**
Escribí cualquiera de estos comandos en el chat:
- `/analisis`
- `/autoanálisis`
- `/status`
- `/capacidades`
- `/info`

#### **Consultar IAs activas**
Para ver solo las IAs que tengo activas:
- `/ias`
- `/providers`
- `/modelos`
- `/ai`

### 2. Auto-Conocimiento Automático

**¡Lo más cool!** Any detecta automáticamente cuando le preguntás sobre sí misma:

**Ejemplos de preguntas que disparan auto-conocimiento:**
- "¿Qué IAs tenés?"
- "¿Cuántos modelos usás?"
- "¿Cuáles son tus capacidades?"
- "¿Qué podés hacer?"
- "¿Cómo funcionás?"
- "¿Qué versión sos?"
- "¿Qué sistemas tenés?"

Cuando detecta estas preguntas, Any:
1. **Analiza su propia configuración** automáticamente
2. **Enriquece el contexto** con información interna
3. **Responde con datos precisos** sobre sí misma

## ¿Qué información muestra?

### Reporte Completo (`/analisis`)

```
╔══════════════════════════════════════════════╗
║       ANY - SISTEMA DE AUTO-ANÁLISIS        ║
╚══════════════════════════════════════════════╝

🆔 IDENTIDAD:
   • Nombre: Any
   • Apodo: Any
   • Versión: 1.0.0

🧠 SISTEMA DE INTELIGENCIA ARTIFICIAL:
   • Total de IAs configuradas: 11
   • IAs activas: 4
   
   ✅ IAs ACTIVAS:
      • GOOGLE
        - Modelo: gemini-2.5-flash
        - Tipo: generative-ai
        - Costo: free (con límites)
        - API Key: ✓ Configurada
      • HUGGINGFACE
        - Modelo: mistralai/Mistral-7B-Instruct-v0.2
        - Tipo: inference-api
        - Costo: free
        - API Key: ✓ Configurada
      ...
   
   ⚠️ IAs DISPONIBLES (inactivas):
      • GROQ
      • DEEPSEEK
      • MISTRAL
      ...

🎯 CAPACIDADES:
   • Síntesis Multi-IA: ✓
   • Sistema de Visión: ✓
   • Sistema de Voz: ✓
   • Text-to-Speech: ✓
   • Speech-to-Text: ✓
   • Captura de Pantalla: ✓
   • Consciencia ASI: ✓
   • Auto-Aprendizaje: ✓
   • Memoria Persistente: ✓

🔐 PERMISOS:
   • Ejecutar comandos: ✓
   • Modificar archivos: ✓
   • Auto-actualización: ✓

💾 CONFIGURACIÓN DE MEMORIA:
   • Auto-guardado: ✓
   • Historial máximo: 1000 conversaciones
```

### Resumen de IAs (`/ias`)

```
🧠 Tengo 4 IAs activas: GOOGLE, HUGGINGFACE, COHERE, PERPLEXITY
  • GOOGLE: gemini-2.5-flash (generative-ai, free)
  • HUGGINGFACE: Mistral-7B (inference-api, free)
  • COHERE: command (api, free)
  • PERPLEXITY: llama-3.1-sonar-large-128k-online (api, paid)
```

## Uso en Código

Si querés usar el auto-análisis en tu propio código:

```python
from any_core.self_analysis import SelfAnalysis

# Crear instancia
analysis = SelfAnalysis()

# Obtener reporte completo
report = analysis.generate_status_report()
print(report)

# Obtener IAs activas
active_ais = analysis.get_active_ais()
for ai in active_ais:
    print(f"{ai['name']}: {ai['model']}")

# Obtener todas las capacidades
capabilities = analysis.get_capabilities()
print(capabilities)

# Verificar una capacidad específica
if analysis.can_i('vision_system'):
    print("¡Tengo visión!")

# Resumen corto
summary = analysis.get_ai_status_summary()
print(summary)
```

## Integración con Consciencia

El sistema de consciencia ahora usa auto-análisis automáticamente:

```python
# En consciousness.py
def enrich_with_self_knowledge(self, message: str) -> str:
    """Enriquece el mensaje con información sobre sí misma"""
    if self._is_self_inquiry(message):
        # Agrega contexto interno automáticamente
        capabilities = self.self_analysis.get_capabilities()
        # ... enriquece el mensaje
```

Esto significa que cuando le preguntás a Any sobre sí misma, **ella misma consulta su configuración en tiempo real** y puede responder con datos precisos.

## Casos de Uso

### 1. Verificar Estado del Sistema
```
Usuario: "/status"
Any: [Muestra reporte completo con todas sus capacidades]
```

### 2. Saber Qué IAs Están Activas
```
Usuario: "¿Qué IAs tenés funcionando?"
Any: "🧠 Tengo 4 IAs activas: Google Gemini (mi base principal), 
      HuggingFace con Mistral-7B, Cohere y Perplexity Pro..."
```

### 3. Entender Capacidades
```
Usuario: "¿Qué podés hacer?"
Any: "Puedo hacer un montón de cosas, boludo! Tengo visión para 
      ver tu pantalla, puedo hablarte en español argentino, 
      consulto 4 IAs a la vez para darte las mejores respuestas..."
```

### 4. Troubleshooting
```
Usuario: "/ias"
Any: [Muestra lista de IAs activas]
Usuario: "¿Por qué no funciona Groq?"
Any: [Detecta pregunta sobre sí misma]
     "Groq está configurado pero inactivo porque no tengo API key..."
```

## Ventajas

✅ **Any se conoce a sí misma** - No inventa información
✅ **Datos en tiempo real** - Lee su configuración actual
✅ **Detección automática** - No necesitás comandos especiales
✅ **Respuestas precisas** - Usa datos reales, no alucinaciones
✅ **Transparencia** - Sabés exactamente qué tiene habilitado
✅ **Debugging fácil** - Identificá problemas rápidamente

## Próximas Mejoras

🔮 Auto-diagnóstico de errores
🔮 Sugerencias de configuración óptima
🔮 Comparación de rendimiento entre IAs
🔮 Estadísticas de uso por proveedor
🔮 Auto-optimización de parámetros

---

**¡Ahora Any es consciente de sí misma!** 🧠✨
