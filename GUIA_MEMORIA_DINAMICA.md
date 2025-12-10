# 🧠 Sistema de Memoria Dinámica de Any

Any ahora tiene un sistema de memoria en tiempo real que le permite guardar, leer, modificar y eliminar información importante.

## 🎯 Características

### Automático
- Any detecta automáticamente información importante durante las conversaciones
- Guarda memorias en categorías: facts, preferences, events, learning, personal, tech, ideas
- Asigna niveles de importancia (1-10)

### Manual
Any puede usar comandos explícitos para gestionar memorias:
- `save_memory()` - Guardar info importante
- `recall_memory()` - Buscar memorias
- `update_memory()` - Actualizar una memoria
- `forget_memory()` - Eliminar una memoria

## 📂 Categorías de Memorias

### 1. **facts** (Hechos)
Información factual general
```python
memory.write_memory("La capital de Argentina es Buenos Aires", category="facts")
```

### 2. **preferences** (Preferencias)
Gustos y preferencias del usuario
```python
memory.write_memory("Adri prefiere usar Groq para análisis", category="preferences")
```

### 3. **events** (Eventos)
Eventos importantes, fechas, recordatorios
```python
memory.write_memory("Cumpleaños de Adri: 15 de marzo", category="events", importance=10)
```

### 4. **learning** (Aprendizajes)
Cosas nuevas aprendidas
```python
memory.write_memory("Aprendí que EdgeGPT usa cookies de Bing", category="learning")
```

### 5. **personal** (Personal)
Información personal del usuario
```python
memory.write_memory("Adri vive en Rosario, Argentina", category="personal", importance=9)
```

### 6. **tech** (Técnico)
Configuraciones, códigos, soluciones técnicas
```python
memory.write_memory("API key de Groq configurada correctamente", category="tech")
```

### 7. **ideas** (Ideas/Planes)
Ideas futuras, proyectos, planes
```python
memory.write_memory("Plan: agregar Ollama local", category="ideas", importance=7)
```

## 🔢 Niveles de Importancia

- **1-3**: Información trivial
- **4-6**: Información moderada
- **7-8**: Información importante
- **9-10**: Información crítica (siempre recordar)

## 🏷️ Tags

Usa tags para organizar y buscar memorias:
```python
memory.write_memory(
    "Groq es rápido para análisis",
    category="learning",
    importance=8,
    tags=["groq", "ia", "performance"]
)
```

## 🔍 Búsqueda de Memorias

### Por texto
```python
results = memory.search_memories(query="Adri")
```

### Por categoría
```python
results = memory.search_memories(category="preferences")
```

### Por tags
```python
results = memory.search_memories(tags=["groq", "ia"])
```

### Por importancia
```python
important = memory.search_memories(min_importance=8)
```

## ✏️ Actualizar Memorias

```python
memory.update_memory(
    memory_id="abc123",
    new_content="Contenido actualizado",
    new_importance=9
)
```

## 🗑️ Eliminar Memorias

```python
memory.delete_memory(memory_id="abc123")
```

## 📊 Estadísticas

Ver estadísticas de memorias:
```python
stats = memory.get_memory_stats()
# Retorna: total, por categoría, por importancia, última actualización
```

## 💾 Export/Import

### Exportar
```python
memory.export_memories("backup.json")
```

### Importar
```python
memory.import_memories("backup.json")
```

## 🔄 Auto-Guardado

Any detecta automáticamente keywords importantes:

### Preferencias
- "me gusta", "prefiero", "no me gusta", "favorito"

### Personal
- "mi nombre", "me llamo", "vivo en", "trabajo en"

### Eventos
- "recordá", "acordate", "importante", "aniversario"

### Aprendizajes
- "aprendí", "descubrí", "entendí", "nueva forma"

### Técnico
- "configuré", "instalé", "api key", "token"

### Ideas
- "plan", "proyecto", "idea", "quiero hacer"

## 📁 Ubicación de Archivos

- **Memorias**: `data/memory/dynamic_memory.json`
- **Exports**: `data/memory/export_memories_TIMESTAMP.json`

## 🎮 Uso en la GUI

1. **Ver memorias**: Botón "🧠 Memorias Guardadas"
2. **Auto-guardado**: Any guarda automáticamente durante conversaciones
3. **Contexto**: Any usa las memorias importantes en sus respuestas

## 💡 Ejemplos de Uso

### Ejemplo 1: Guardar preferencia
**Usuario**: "Prefiero que uses Perplexity para buscar noticias"
**Any detecta**: categoria=preferences, importance=8, tags=["perplexity", "noticias"]

### Ejemplo 2: Guardar info personal
**Usuario**: "Mi cumpleaños es el 20 de mayo"
**Any detecta**: categoria=events, importance=10, tags=["cumpleaños", "adri"]

### Ejemplo 3: Guardar aprendizaje
**Usuario**: "Acabamos de configurar EdgeGPT con cookies"
**Any detecta**: categoria=learning, importance=8, tags=["edgegpt", "configuración"]

## 🔐 Seguridad

- Las memorias se guardan localmente en JSON
- No se envían a ningún servidor externo
- Puedes eliminar memorias en cualquier momento
- Usa tags para organizar información sensible

## 🚀 Próximas Mejoras

- [ ] Búsqueda semántica con embeddings
- [ ] Relaciones entre memorias
- [ ] Priorización automática por frecuencia de acceso
- [ ] Compresión de memorias antiguas
- [ ] Interfaz visual para gestionar memorias
- [ ] Exportar a diferentes formatos (Markdown, CSV)

---

**Nota**: Este sistema complementa la memoria comprimida existente. La memoria dinámica es para información específica y importante, mientras que la memoria comprimida es para contexto general de conversaciones.
