# Sistema de Memoria Comprimida de Any

## ¿Qué es?

Un sistema ultra-liviano de memoria que **solo la IA entiende**. En lugar de guardar conversaciones completas, Any comprime cada charla en "tokens" que son como códigos que solo ella puede interpretar.

## ¿Por qué es mejor?

### **Antes (memoria normal):**
```json
{
  "user": "Quiero agregar Groq a la app porque es más rápido que Gemini",
  "assistant": "Dale, Groq es súper rápido! Te voy a explicar cómo agregarlo..."
}
```
**Peso:** ~200-300 bytes por conversación

### **Ahora (memoria comprimida):**
```
ais|groq gemini|agregar app rapido|20241205
```
**Peso:** ~40 bytes (¡7x más liviano!)

## ¿Cómo funciona?

### 1. **Compresión Automática**
Cada vez que hablás con Any, ella extrae:
- **Categoría** (cod, ais, mem, vis, voc, prj, gen)
- **Conceptos clave** (máximo 5 palabras importantes)
- **Detalles mínimos** (máximo 10 palabras relevantes)
- **Timestamp** (fecha en formato compacto)

**Ejemplo:**
```
Tu mensaje: "Necesito que la app pueda recordar mis preferencias de voz en español argentino"
Token generado: voc|preferencias español argentino|recordar app|20241205
```

### 2. **Extracción de Hechos**
Any detecta automáticamente:
- ✅ **Preferencias:** "prefiero X", "me gusta Y"
- ✅ **Configuraciones:** IAs mencionadas, modelos usados
- ✅ **Proyectos:** "crear app", "hacer programa"
- ✅ **Tecnologías:** Python, React, Docker, etc.

### 3. **Contexto Inteligente**
Cuando Any responde, agrega automáticamente:
```
[CTX_RECIENTE]: ais:groq,gemini | vis:pantalla,captura | mem:recordar,guardar
[HECHOS]: ias:groq=activo | ias:gemini=activo | proyectos:actual=any app
[PREFS]: voice=español_argentino | tts_mode=gtts
```

**Solo usa ~200-300 bytes** vs 5-10KB de conversaciones completas!

## Comandos

### Ver Estadísticas de Memoria
```
/memoria
/memory
/mem
```

Muestra:
```
╔════════════════════════════════════╗
║    ESTADÍSTICAS DE MEMORIA        ║
╚════════════════════════════════════╝

💾 Tokens de Contexto: 15
📊 Hechos Clave: 8
❤️ Preferencias: 3
🔗 Relaciones: 2
📦 Tamaño del archivo: 2.5 KB
🕐 Última actualización: 2024-12-05T15:30:00

🧠 Contexto Actual:
   [CTX_RECIENTE]: ais:groq,gemini | vis:captura
   [HECHOS]: ias:groq=activo | proyectos:actual=any app
   [PREFS]: voice=español_argentino
```

## Categorías de Tokens

| Código | Categoría | Ejemplos |
|--------|-----------|----------|
| `cod` | Coding | código, función, bug, clase |
| `ais` | AI Systems | IA, modelo, provider, gemini |
| `mem` | Memory | memoria, recordar, guardar |
| `voc` | Voice | voz, hablar, escuchar, TTS |
| `vis` | Vision | visión, pantalla, captura |
| `prf` | Preference | preferencia, gustar, querer |
| `prj` | Project | proyecto, app, crear |
| `gen` | General | conversación general |

## Ejemplos Reales

### Ejemplo 1: Configuración de IA
```
Usuario: "Activá Groq porque es más rápido"
Token: ais|groq rapido|activar|20241205
Hecho guardado: ias:groq=activo
```

### Ejemplo 2: Preferencia de Voz
```
Usuario: "Prefiero la voz de Argentina en lugar de México"
Token: prf|voz argentina mexico|prefiero|20241205
Preferencia: voice=argentina
```

### Ejemplo 3: Proyecto
```
Usuario: "Estamos creando una app de IA con visión"
Token: prj|app ia vision|crear|20241205
Hecho: proyectos:actual=app ia vision
```

## Ventajas

✅ **Ultra-liviana:** 7-10x menos espacio que conversaciones completas
✅ **Automática:** Se actualiza sola con cada conversación
✅ **Inteligente:** Extrae solo lo importante
✅ **Rápida:** Carga instantánea, no lag
✅ **Escalable:** Mantiene solo últimos 100 tokens
✅ **Contextual:** Any recuerda lo importante sin leer todo

## Limitaciones (Buenas)

- Máximo 100 tokens activos (auto-limpieza)
- Solo guarda lo MÁS importante
- Los detalles triviales se pierden (¡es intencional!)
- Enfocada en hechos, no en conversaciones casuales

## Archivos

### `memory_compressed.json`
```json
{
  "version": "1.0",
  "context_tokens": [
    "ais|groq gemini|activar rapido|20241205",
    "vis|pantalla captura|analizar|20241205"
  ],
  "key_facts": {
    "ias": {
      "groq": {"value": "activo", "timestamp": "2024-12-05T15:30:00"}
    }
  },
  "preferences": {
    "voice": {"value": "argentina", "timestamp": "2024-12-05T15:30:00"}
  },
  "relationships": {},
  "last_update": "2024-12-05T15:30:00"
}
```

**Tamaño típico:** 2-5 KB (vs 50-100 KB de memoria normal)

## Uso Programático

```python
from any_core.memory_compression import MemoryCompression

# Crear instancia
mem = MemoryCompression()

# Comprimir conversación
token = mem.compress_conversation(
    "Quiero usar Groq",
    "Dale, Groq es súper rápido"
)
# Resultado: "ais|groq|usar|20241205"

# Agregar hecho clave
mem.add_key_fact("ias", "groq", "activo")

# Agregar preferencia
mem.add_preference("voice", "argentina")

# Obtener contexto para prompts
context = mem.get_full_context()
# Resultado: "[CTX_RECIENTE]: ais:groq | [HECHOS]: ias:groq=activo..."

# Ver estadísticas
stats = mem.get_memory_stats()
print(f"Tokens: {stats['total_tokens']}")
print(f"Tamaño: {stats['file_size_kb']} KB")
```

## Integración con Consciencia

El sistema se integra automáticamente:

```python
# En consciousness.py
def query_all_ais(self, message: str, system_prompt: str):
    # Agregar contexto comprimido automáticamente
    compressed_context = self.compressed_memory.get_full_context()
    enriched_message = f"{message}\n\n{compressed_context}"
    
    # Las IAs reciben el contexto pero pesa casi nada!
    ...

def synthesize_response(self, all_responses, user_message):
    # Comprimir la conversación automáticamente
    token = self.compressed_memory.compress_conversation(
        user_message, 
        my_response
    )
    ...
```

## Comparación

| Característica | Memoria Normal | Memoria Comprimida |
|----------------|----------------|-------------------|
| Tamaño por conversación | 200-500 bytes | 30-60 bytes |
| Conversaciones almacenadas | ~100 (50 KB) | ~1000 (5 KB) |
| Velocidad de carga | Lenta (leer JSON grande) | Instantánea |
| Contexto en prompts | ~500-1000 tokens | ~50-100 tokens |
| Pérdida de información | 0% | ~70% (solo lo trivial) |
| Retención de hechos clave | Manual | Automática |

## Conclusión

**Memoria Comprimida** es perfecta para que Any recuerde lo importante sin ocupar espacio ni hacer la app lenta. Es como tener "notas mentales" ultra-compactas en lugar de grabar todo el audio de una conversación.

**¿Resultado?** Any te recuerda, pero la app vuela! 🚀
