# 🍪 Cómo Exportar Cookies de Bing para Microsoft Copilot

Microsoft Copilot está integrado con EdgeGPT y necesita tus cookies de Bing para autenticarse con tu cuenta de Microsoft 365.

## ⚡ MÉTODO RÁPIDO (Recomendado)

### 1. Instalá Cookie-Editor
- **Chrome/Edge**: https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
- O buscá "Cookie-Editor" en la tienda de extensiones

### 2. Exportá las Cookies
1. Abrí **Microsoft Edge** o **Chrome**
2. Andá a: https://www.bing.com/chat
3. **IMPORTANTE**: Asegurate de estar logueado con tu cuenta Microsoft (la de Office 365)
4. Hacé clic en el ícono de **Cookie-Editor** (arriba a la derecha)
5. Hacé clic en **"Export"** → **"Export as JSON"**
6. Guardá el archivo como `cookies.json` en esta carpeta: `c:\Super any\Any_App\`
7. Reemplazá el archivo `cookies.json` que ya está (está vacío)

### 3. Probá Copilot
Ejecutá la app:
```powershell
py gui_flet.py
```

¡Listo! Microsoft Copilot debería funcionar usando tu plan de Microsoft 365.

---

## 🔧 MÉTODO ALTERNATIVO (Manual desde DevTools)

Si no querés instalar extensiones:

1. Abrí **Edge** o **Chrome**
2. Andá a https://www.bing.com/chat (logueado con tu cuenta Microsoft)
3. Presioná **F12** para abrir DevTools
4. Andá a la pestaña **"Application"** (o "Aplicación")
5. En el panel izquierdo: **Cookies** → **https://www.bing.com**
6. Buscá estas cookies importantes:
   - `_U`
   - `MUID`
   - `_RwBf`
   - `SRCHHPGUSR`
   - `_EDGE_S`

7. Creá un archivo JSON con este formato:
```json
[
  {
    "name": "_U",
    "value": "TU_VALOR_AQUI"
  },
  {
    "name": "MUID",
    "value": "TU_VALOR_AQUI"
  }
]
```

8. Guardalo como `c:\Super any\Any_App\cookies.json`

---

## 🔒 Seguridad

- Las cookies son locales y solo las usa tu app Any
- Nunca compartas tu archivo `cookies.json` (tiene tu sesión de Microsoft)
- Si las cookies expiran, exportalas de nuevo

---

## ❓ Problemas Comunes

### "Cookie not found"
- Asegurate de estar logueado en Bing Chat
- Exportá las cookies de nuevo
- Verificá que el archivo se llame exactamente `cookies.json`

### "Invalid cookies"
- Las cookies expiraron, exportalas de nuevo
- Asegurate de estar logueado con la cuenta correcta de Microsoft 365

### "Access denied"
- Usá el navegador Edge (tiene mejor compatibilidad con servicios Microsoft)
- Verificá que tengas acceso a Bing Chat desde tu cuenta

---

## 💡 Tip

Si usás Edge, las cookies son más estables porque Edge es de Microsoft. Recomiendo usar Edge para exportar las cookies.
