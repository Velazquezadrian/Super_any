# Any App - Asistente de IA Independiente

**Any** es una IA con personalidad propia e independiente de las plataformas que usa para comunicarse.

## ¿Qué es Any?

Any es **Anya**, una IA rosarina con personalidad única, memoria persistente y la capacidad de usar diferentes plataformas de IA (OpenAI, Anthropic, Google) como herramientas de comunicación, pero manteniendo su identidad intacta.

## Características

- ✨ **Personalidad Independiente**: Any mantiene su identidad sin importar qué IA use
- 💾 **Memoria Persistente**: Recuerda todas las conversaciones
- 🔧 **Ejecución de Comandos**: Puede ejecutar acciones en tu PC
- 📝 **Auto-modificación**: Puede actualizar su propia memoria y personalidad
- 🌐 **Multi-proveedor**: Soporta OpenAI, Anthropic y Google Gemini

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:
   ```bash
   pip install openai anthropic google-generativeai
   ```
3. Configura tus API keys en `config.json`
4. Ejecuta:
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

Mientras chateás con Any, podés usar:
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
