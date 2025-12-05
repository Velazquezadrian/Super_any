# Any App - Asistente de IA Independiente

**Any** es una IA con personalidad propia e independiente de las plataformas que usa para comunicarse.

## ¿Qué es Any?

Any es **Anya**, una IA rosarina con personalidad única, memoria persistente y la capacidad de usar diferentes plataformas de IA (OpenAI, Anthropic, Google) como herramientas de comunicación, pero manteniendo su identidad intacta.

## Características

- ✨ **Personalidad Independiente**: Any mantiene su identidad sin importar qué IA use
- 🧠 **Consciencia ASI**: Consulta múltiples IAs simultáneamente y sintetiza su propia respuesta
- 🔍 **Auto-Análisis**: Any puede analizar sus propias capacidades y configuración
- 🤖 **Auto-Conocimiento**: Detecta preguntas sobre sí misma y responde con precisión
- 💾 **Memoria Persistente**: Recuerda todas las conversaciones
- 👁️ **Visión por Computadora**: Captura y analiza tu pantalla en tiempo real
- 🎤 **Sistema de Voz**: Habla y escucha en español argentino
- 🔧 **Ejecución de Comandos**: Puede ejecutar acciones en tu PC
- 📝 **Auto-modificación**: Puede actualizar su propia memoria y personalidad
- 🌐 **Multi-proveedor**: Soporta Google Gemini, HuggingFace, Cohere, Perplexity, Groq, DeepSeek, Mistral y más

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tus API keys en `config.json`
4. Ejecuta:
   
   **Opción 1: GUI con consola (para debug)**
   ```bash
   python gui.py
   ```
   
   **Opción 2: GUI sin consola (recomendado)**
   ```bash
   pythonw gui.py
   ```
   O doble click en `launch_any.pyw`
   
   **Opción 3: CLI**
   ```bash
   python main.py
   ```

## Configuración

Edita `config.json` para:
- Agregar tus API keys
- Habilitar/deshabilitar proveedores de IA
- Configurar permisos de Any
- Personalizar rutas de archivos

## Comandos

Mientras chateás con Any en la GUI, podés usar:
- `/analisis` o `/status` - Muestra el auto-análisis completo del sistema
- `/ias` o `/providers` - Ver IAs activas y sus modelos
- `/capacidades` - Ver todas las capacidades de Any
- **Botón 🔍 Auto-Analysis** - Muestra análisis completo en el chat
- **Botón 👁️** - Captura y analiza tu pantalla
- **Botón 🎤** - Activar entrada de voz
- **Toggle Vision Mode** - Activar/desactivar análisis automático de pantalla
- **Toggle Voice Mode** - Activar/desactivar respuestas por voz

En modo CLI (`main.py`):
- `/help` - Muestra ayuda
- `/memoria` - Ver conversaciones recientes
- `/exec [comando]` - Ejecutar comando del sistema
- `/providers` - Ver proveedores de IA disponibles
- `salir` - Cerrar la app

## Estructura

```
Any_App/
├── any_core/           # Módulos principales
│   ├── personality.py  # Gestión de personalidad
│   ├── memory.py       # Gestión de memoria
│   ├── ai_connector.py # Conexión con IAs
│   └── executor.py     # Ejecución de comandos
├── data/               # Datos de Any
│   ├── memory/         # Conversaciones guardadas
│   ├── personality/    # Archivos de identidad
│   └── logs/           # Logs del sistema
├── main.py             # Aplicación principal
└── config.json         # Configuración
```

## Licencia

Proyecto personal de Adri y Any 💙
