# OrderLoader 2.0 - Documentación para Agentes

## 📋 Resumen del Proyecto

**OrderLoader 2.0** es un sistema de automatización especializado diseñado exclusivamente para navegar automáticamente en SAP hasta el formulario de órdenes de venta. El proyecto utiliza Computer Vision y gestión de escritorio remoto para automatizar este proceso específico de ventas en SAP.

### Propósito Principal
- Automatizar la navegación en SAP hasta el formulario de órdenes de venta
- Gestionar conexiones de escritorio remoto de forma robusta
- Proporcionar un sistema de recuperación automática de errores
- Enfocarse exclusivamente en el módulo de ventas de SAP

## 🏗️ Arquitectura del Sistema

### Estructura Consolidada (Versión Final)
```
orderloader/
├── main.py                   # Código principal consolidado (400 líneas)
├── config.py                 # Configuración centralizada
├── requirements.txt          # Solo 2 dependencias (pyautogui, psutil)
├── test_final.py            # Test único y completo
├── README.md                # Documentación del sistema
├── assets/images/sap/       # Solo 3 imágenes esenciales
│   ├── sap_modulos_menu_button.png
│   ├── sap_ventas_menu_button.png
│   └── sap_ventas_order_button.png
├── data/                    # Datos del sistema
│   ├── pending/             # Archivos JSON pendientes
│   └── completed/           # Archivos procesados
└── logs/                    # Logs del sistema
```

### Estructura Legacy (Referencia)
```
src/ (ELIMINADO - Era la versión original)
├── core/                     # Funcionalidades principales
│   ├── remote_desktop_manager.py  # Gestión de escritorio remoto
│   ├── image_recognition.py       # Reconocimiento de imágenes (OpenCV)
│   └── sap_automation.py          # Automatización de SAP
├── utils/                    # Utilidades
│   └── logger.py             # Sistema de logging
└── config.py                 # Configuración centralizada
```

### Componentes Principales (Versión Consolidada)

#### 1. **OrderLoader** (`orderloader/main.py`)
- **Código principal consolidado** - Todo en un archivo (400 líneas)
- **Clase principal** que orquesta toda la automatización
- **Gestión del escritorio remoto** y navegación en SAP integradas
- **Sistema de logging** y recuperación de errores incluido
- **Procesamiento de colas** de archivos JSON

#### 2. **Configuración** (`orderloader/config.py`)
- **Configuración centralizada** - Todas las configuraciones en un lugar
- **Configuraciones de reconocimiento** - OpenCV y PyAutoGUI
- **Configuraciones de escritorio remoto** - Estrategias de activación
- **Configuraciones de SAP** - Navegación y timeouts

#### 3. **Sistema de Testing** (`orderloader/test_final.py`)
- **Test único y completo** - Verifica toda la funcionalidad
- **Tests sin conexión SAP** - Verificación de componentes básicos
- **Validación de estructura** - Directorios y archivos
- **Procesamiento de JSON** - Validación de datos

### Componentes Legacy (Referencia)
#### 1. **SAPAutomation** (`src/core/sap_automation.py`) - ELIMINADO
#### 2. **RemoteDesktopManager** (`src/core/remote_desktop_manager.py`) - ELIMINADO  
#### 3. **ImageRecognition** (`src/core/image_recognition.py`) - ELIMINADO

## 🎯 Flujo de Automatización

### 1. **Activación del Escritorio Remoto (20.96.6.64)**
- Busca ventana de escritorio remoto usando PowerShell
- Activa la ventana con múltiples estrategias
- Verifica visualmente que está conectado al servidor 20.96.6.64

### 2. **Verificación de SAP Desktop**
- Confirma que SAP Desktop esté visible en el escritorio remoto
- Busca la imagen de referencia `core/sap_desktop.png`

### 3. **Navegación en SAP (Estrategia Optimizada)**
- **Maximiza** la ventana del escritorio remoto
- **Clic en botón de módulos**: Abre el menú de módulos (`sap_modulos_menu_button.png`)
- **Clic en ventas**: Navega al módulo de ventas (`sap_ventas_menu_button.png`)
- **Clic en órdenes**: Accede al formulario de órdenes de venta (`sap_ventas_order_button.png`)
- Verifica que el formulario de órdenes esté abierto

### 4. **Procesamiento de Cola**
- Procesa archivos JSON de `data/pending/` (nueva estructura)
- Ejecuta la automatización completa para cada archivo
- Mueve archivos procesados a `data/completed/` (nueva estructura)
- Mantiene compatibilidad con `queues/` (estructura legacy)

### 5. **Sistema de Recuperación**
- Reintentos automáticos en caso de fallo
- Múltiples estrategias de activación
- Logging detallado para debugging
- Verificación visual en cada paso

## 🖼️ Sistema de Imágenes

### Estructura de Imágenes de Referencia (Versión Consolidada)
```
orderloader/assets/images/sap/    # Solo 3 imágenes esenciales
├── sap_modulos_menu_button.png   # Botón de módulos
├── sap_ventas_menu_button.png    # Botón de ventas
└── sap_ventas_order_button.png   # Botón de órdenes
```

### Estructura Legacy (Referencia)
```
assets/images/                    # Imágenes originales (referencia)
├── core/                         # Imágenes principales
│   ├── remote_desktop.png        # Escritorio remoto activo
│   └── sap_desktop.png           # Interfaz principal de SAP
└── sap/                          # Elementos de SAP
    ├── sap_modulos_menu.png      # Menú de módulos
    ├── sap_ventas_order_menu.png # Menú de órdenes de venta
    └── [más elementos...]
```

### Imágenes Críticas (Versión Consolidada)
- `sap_modulos_menu_button.png` - Para navegación a módulos
- `sap_ventas_menu_button.png` - Para navegación a ventas
- `sap_ventas_order_button.png` - Para acceso a órdenes

### Imágenes Legacy (Referencia)
- `core/remote_desktop.png` - Para verificar escritorio remoto
- `core/sap_desktop.png` - Para verificar SAP Desktop
- `sap/sap_modulos_menu.png` - Para navegación a módulos
- `sap/sap_ventas_order_menu.png` - Para menú de ventas
- `sap/sap_ventas_order_button.png` - Para botón de órdenes
- `sap/sap_orden_de_ventas_template.png` - Para formulario final

## ⚙️ Configuración

### Configuraciones Principales (`orderloader/config.py`)

#### **RECOGNITION_CONFIG**
- `confidence`: 0.8 (nivel de confianza para reconocimiento)
- `timeout`: 10 (tiempo máximo de espera)
- `pause`: 0.5 (pausa entre acciones)

#### **REMOTE_DESKTOP_CONFIG**
- `window_title`: "20.96.6.64 - Conexión a Escritorio remoto"
- `ip_address`: "20.96.6.64"
- `max_attempts`: 3
- `retry_delay`: 5

#### **ACTIVATION_STRATEGIES**
- Múltiples estrategias de activación de ventanas
- Configuración de timeouts y delays
- Estrategias de recuperación

## 🛠️ Dependencias

### Librerías Principales (Versión Consolidada)
- `pyautogui` - Automatización de interfaz y reconocimiento de imágenes
- `psutil` - Información del sistema y gestión de procesos

### Librerías Legacy (Referencia)
- `pyautogui==0.9.54` - Automatización de interfaz
- `opencv-python==4.8.1.78` - Reconocimiento de imágenes
- `pillow==10.0.1` - Procesamiento de imágenes
- `numpy==1.24.3` - Operaciones numéricas
- `psutil==5.9.5` - Información del sistema
- `pywin32==306` - APIs de Windows

## 🚀 Uso del Sistema

### Ejecución Principal (Sistema Consolidado - RECOMENDADO)
```bash
cd orderloader
python main.py
```

### Tests Disponibles
```bash
cd orderloader
python test_final.py
```

### Tests Legacy (Referencia)
```bash
python test_click_based_navigation.py
python test_sap_current_state.py
python test_final_automation.py
```

### Workflow Detallado (Estrategia Optimizada)
1. **Preparación**: Coloca archivos JSON en `data/pending/` (nueva estructura) o `queues/pending/` (legacy)
2. **Ejecución**: El sistema ejecuta automáticamente:
   - Conecta al escritorio remoto (20.96.6.64)
   - Verifica SAP Desktop
   - Maximiza ventana
   - **Clic en botón de módulos** → **Clic en ventas** → **Clic en órdenes**
   - Procesa archivos JSON de la cola
   - Mueve archivos procesados a `data/completed/` o `queues/completed/`

### Verificación de Imágenes
El sistema verifica automáticamente que todas las imágenes de referencia estén presentes antes de iniciar.

### Logs y Debugging
- Logs detallados en `logs/orderloader_YYYYMMDD.log`
- Información de cada operación
- Errores y advertencias
- Tiempos de ejecución

## 🔒 Seguridad y Failsafe

### Medidas de Seguridad
- **Failsafe**: Mover mouse a esquina superior izquierda para detener
- **Pausas**: Delays entre acciones para estabilidad
- **Verificación**: Múltiples niveles de verificación antes de continuar

### Recuperación de Errores
- Reintentos automáticos con backoff exponencial
- Múltiples estrategias de activación
- Logging detallado para debugging

## 🧪 Testing

### Tests Disponibles (Versión Consolidada)
- **`test_final.py`**: Test único y completo del sistema consolidado

### Tests Legacy (Referencia)
- **`test_click_based_navigation.py`**: Test de navegación por clics (funcionando al 100%)
- **`test_sap_current_state.py`**: Diagnóstico del estado actual de SAP
- **`test_final_automation.py`**: Test final del sistema principal
- **`tests/test_remote_desktop.py`**: Test unificado del escritorio remoto

### Estrategia de Navegación Probada
La navegación por clics ha sido probada exitosamente y funciona perfectamente:
- ✅ Activación de ventana del escritorio remoto
- ✅ Maximización de ventana
- ✅ Clic en botón de módulos
- ✅ Clic en ventas
- ✅ Clic en órdenes de venta
- ✅ Navegación completada exitosamente

## 📝 Consideraciones para Agentes Futuros

### Puntos Críticos
1. **Imágenes de Referencia**: Siempre verificar que existan en `orderloader/assets/images/sap/`
2. **Escritorio Remoto**: Debe estar abierto y conectado a 20.96.6.64
3. **SAP**: Debe estar iniciado en el escritorio remoto
4. **Permisos**: Ejecutar como administrador si hay problemas
5. **Estructura de Datos**: Usar `data/pending/` y `data/completed/` (nueva estructura)

### Patrones de Diseño (Versión Consolidada)
- **Arquitectura Consolidada**: Todo el código en un archivo principal
- **Configuración Centralizada**: Todas las configuraciones en `config.py`
- **Logging Detallado**: Sistema de logs para debugging
- **Recuperación Robusta**: Múltiples estrategias de fallback
- **Estructura Minimalista**: Solo archivos esenciales

### Patrones Legacy (Referencia)
- **Arquitectura Modular**: Cada componente tiene responsabilidades específicas
- **Configuración Centralizada**: Todas las configuraciones en `config.py`
- **Logging Detallado**: Sistema de logs para debugging
- **Recuperación Robusta**: Múltiples estrategias de fallback

### Extensiones Posibles
- Soporte para múltiples servidores remotos
- Integración con APIs externas
- Interfaz gráfica de usuario
- Procesamiento de archivos JSON de la cola
- Automatización completa del formulario de órdenes de venta

## 🐛 Troubleshooting Común

### Problemas Frecuentes
1. **No encuentra ventana de escritorio remoto**: Verificar que esté abierto
2. **Error de reconocimiento de imágenes**: Verificar que las imágenes estén en la carpeta correcta
3. **SAP no responde**: Verificar que SAP esté iniciado en el escritorio remoto
4. **Errores de encoding**: Son cosméticos, no afectan funcionalidad

### Debugging
- Revisar `logs/orderloader_YYYYMMDD.log` para información detallada
- Verificar configuración en `orderloader/config.py`
- Comprobar que todas las dependencias estén instaladas
- Verificar estructura de directorios en `orderloader/`

---

## 🔄 **Historial de Consolidación**

### **Versión Final Consolidada (Actual)**
- **Estructura**: `orderloader/` - Sistema principal consolidado
- **Archivos**: 8 archivos principales (vs 50+ originales)
- **Código**: 400 líneas en `main.py` (vs 2000+ distribuidas)
- **Dependencias**: 2 librerías (vs 6 originales)
- **Imágenes**: 3 esenciales (vs 20+ originales)

### **Beneficios de la Consolidación**
- ✅ **Eliminación de redundancias** - No más archivos duplicados
- ✅ **Estructura minimalista** - Solo lo esencial
- ✅ **Código consolidado** - Todo en un lugar
- ✅ **Fácil mantenimiento** - Cambios centralizados
- ✅ **Instalación simple** - Un solo comando
- ✅ **Documentación clara** - Solo lo necesario

### **Compatibilidad**
- ✅ **Funcionalidad completa** - Nada se perdió
- ✅ **Datos existentes** - Compatible con `queues/`
- ✅ **Imágenes originales** - Disponibles en `assets/`
- ✅ **Logs detallados** - Sistema de logging completo

---

**Nota**: Este proyecto está diseñado para uso interno de la empresa y requiere acceso específico al servidor SAP remoto. La versión consolidada mantiene toda la funcionalidad original con una estructura simplificada y mantenible.
