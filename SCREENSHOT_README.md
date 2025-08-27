# 📸 Capturador de Pantalla de SAP - OrderLoader 2.0

Este módulo permite tomar capturas de pantalla automáticas de SAP a través del escritorio remoto.

## 🚀 Scripts Disponibles

### 1. `take_sap_screenshot.py` - Captura Simple
Toma una sola captura de pantalla de SAP.

```bash
python take_sap_screenshot.py
```

**Características:**
- ✅ Busca automáticamente la ventana del escritorio remoto
- ✅ Activa la ventana con Alt+Tab
- ✅ Maximiza la ventana
- ✅ Toma la captura de pantalla
- ✅ Guarda en `assets/screenshots/` con timestamp

### 2. `take_multiple_screenshots.py` - Capturas Múltiples
Toma múltiples capturas de pantalla con opciones configurables.

```bash
# 3 capturas por defecto (delay de 2 segundos)
python take_multiple_screenshots.py

# 5 capturas
python take_multiple_screenshots.py -c 5

# 10 capturas con 5 segundos de delay
python take_multiple_screenshots.py -c 10 -d 5

# Solo una captura (equivalente al script simple)
python take_multiple_screenshots.py --single
```

**Opciones disponibles:**
- `-c, --count`: Número de capturas (por defecto: 3)
- `-d, --delay`: Delay en segundos entre capturas (por defecto: 2.0)
- `--single`: Tomar solo una captura

## 📁 Estructura de Archivos

```
orderLoader2.0/
├── take_sap_screenshot.py          # Script de captura simple
├── take_multiple_screenshots.py    # Script de capturas múltiples
├── assets/
│   └── screenshots/                # Directorio donde se guardan las capturas
│       ├── sap_screenshot_20241201_143022.png
│       ├── sap_screenshot_batch_20241201_143022_1.png
│       └── ...
└── src/
    └── core/
        └── screenshot_manager.py   # Módulo principal de capturas
```

## 🔧 Cómo Funciona

### Proceso Automático:

1. **🔍 Búsqueda de Ventana**: El script busca la ventana del escritorio remoto usando PowerShell
2. **🔄 Activación**: Usa Alt+Tab para activar la ventana del escritorio remoto
3. **📏 Maximización**: Maximiza la ventana para obtener la mejor vista
4. **📸 Captura**: Toma la captura de pantalla completa
5. **💾 Guardado**: Guarda la imagen en `assets/screenshots/` con timestamp

### Estrategias de Recuperación:

Si Alt+Tab no funciona, el sistema intenta:
- PowerShell con SetForegroundWindow
- Win+Tab y clic en la ventana
- Nueva conexión RDP si es necesario

## 📋 Requisitos

- ✅ Python 3.7+
- ✅ Dependencias instaladas (`pip install -r requirements.txt`)
- ✅ Escritorio remoto abierto y conectado a SAP
- ✅ Ventana de escritorio remoto visible

## 🎯 Casos de Uso

### Documentación de Estados
```bash
# Tomar captura antes de iniciar proceso
python take_sap_screenshot.py

# Realizar acciones en SAP...

# Tomar captura después del proceso
python take_sap_screenshot.py
```

### Monitoreo Continuo
```bash
# Tomar 10 capturas cada 30 segundos
python take_multiple_screenshots.py -c 10 -d 30
```

### Debugging
```bash
# Tomar múltiples capturas rápidas para debugging
python take_multiple_screenshots.py -c 5 -d 1
```

## 🔍 Troubleshooting

### Error: "No se encontró la ventana del escritorio remoto"
- ✅ Verifica que el escritorio remoto esté abierto
- ✅ Asegúrate de que la ventana tenga el título correcto
- ✅ Revisa el archivo `orderloader.log` para más detalles

### Error: "No se pudo activar el escritorio remoto"
- ✅ Asegúrate de que la ventana no esté minimizada
- ✅ Verifica que no haya otras ventanas bloqueando
- ✅ Intenta activar manualmente la ventana antes de ejecutar

### Error: "Error al tomar captura de pantalla"
- ✅ Verifica permisos de escritura en `assets/screenshots/`
- ✅ Asegúrate de que pyautogui esté instalado correctamente
- ✅ Revisa que no haya software de seguridad bloqueando

## 📝 Logs

Todos los eventos se registran en:
- **Consola**: Información en tiempo real
- **Archivo**: `orderloader.log` (logs detallados)

## 🚨 Notas Importantes

- ⚠️ **No muevas el mouse** durante la captura
- ⚠️ **Para detener**: Mueve el mouse a la esquina superior izquierda o Ctrl+C
- ⚠️ **Asegúrate** de que SAP esté visible en el escritorio remoto
- ⚠️ **Verifica** que la ventana del escritorio remoto esté activa

## 🔄 Integración con OrderLoader

Estos scripts están diseñados para integrarse con el sistema OrderLoader 2.0:

- ✅ Usan la misma configuración (`src/config.py`)
- ✅ Comparten el sistema de logging
- ✅ Utilizan el mismo gestor de escritorio remoto
- ✅ Mantienen la estructura de archivos consistente

## 📞 Soporte

Si encuentras problemas:
1. Revisa el archivo `orderloader.log`
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que el escritorio remoto esté funcionando correctamente
4. Consulta la documentación principal de OrderLoader 2.0
