# OrderLoader 2.0 - Documentación para Agentes

## 📋 Resumen del Proyecto

**OrderLoader 2.0** es un sistema de automatización especializado diseñado exclusivamente para navegar automáticamente en SAP hasta el formulario de órdenes de venta. El proyecto utiliza Computer Vision y gestión de escritorio remoto para automatizar este proceso específico de ventas en SAP.

### Propósito Principal
- Automatizar la navegación en SAP hasta el formulario de órdenes de venta
- Gestionar conexiones de escritorio remoto de forma robusta
- Proporcionar un sistema de recuperación automática de errores
- Enfocarse exclusivamente en el módulo de ventas de SAP

## 🏗️ Arquitectura del Sistema

### Estructura Modular
```
src/
├── core/                     # Funcionalidades principales
│   ├── remote_desktop_manager.py  # Gestión de escritorio remoto
│   ├── image_recognition.py       # Reconocimiento de imágenes (OpenCV)
│   └── sap_automation.py          # Automatización de SAP
├── utils/                    # Utilidades
│   └── logger.py             # Sistema de logging
└── config.py                 # Configuración centralizada
```

### Componentes Principales

#### 1. **SAPAutomation** (`src/core/sap_automation.py`)
- Clase principal que orquesta toda la automatización
- Coordina la gestión del escritorio remoto y la navegación en SAP
- Implementa verificación visual y recuperación de errores

#### 2. **RemoteDesktopManager** (`src/core/remote_desktop_manager.py`)
- Gestiona la detección, activación y maximización de ventanas de escritorio remoto
- Implementa múltiples estrategias de activación (Alt+Tab, PowerShell, Win+Tab)
- Maneja la conexión al servidor remoto (20.96.6.64)

#### 3. **ImageRecognition** (`src/core/image_recognition.py`)
- Utiliza OpenCV para reconocimiento de imágenes en pantalla
- Busca elementos específicos de SAP usando imágenes de referencia
- Configurable con niveles de confianza y timeouts

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
- Procesa archivos JSON de `queues/pending/`
- Ejecuta la automatización completa para cada archivo
- Mueve archivos procesados a `queues/completed/`

### 5. **Sistema de Recuperación**
- Reintentos automáticos en caso de fallo
- Múltiples estrategias de activación
- Logging detallado para debugging
- Verificación visual en cada paso

## 🖼️ Sistema de Imágenes

### Estructura de Imágenes de Referencia
```
assets/images/
├── core/                     # Imágenes principales
│   ├── remote_desktop.png    # Escritorio remoto activo
│   └── sap_desktop.png       # Interfaz principal de SAP
└── sap/                      # Elementos de SAP
    ├── sap_modulos_menu.png  # Menú de módulos
    ├── sap_ventas_order_menu.png  # Menú de órdenes de venta
    └── [más elementos...]
```

### Imágenes Críticas (REQUIRED_IMAGES)
- `core/remote_desktop.png` - Para verificar escritorio remoto
- `core/sap_desktop.png` - Para verificar SAP Desktop
- `sap/sap_modulos_menu.png` - Para navegación a módulos
- `sap/sap_ventas_order_menu.png` - Para menú de ventas
- `sap/sap_ventas_order_button.png` - Para botón de órdenes
- `sap/sap_orden_de_ventas_template.png` - Para formulario final

## ⚙️ Configuración

### Configuraciones Principales (`src/config.py`)

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

### Librerías Principales
- `pyautogui==0.9.54` - Automatización de interfaz
- `opencv-python==4.8.1.78` - Reconocimiento de imágenes
- `pillow==10.0.1` - Procesamiento de imágenes
- `numpy==1.24.3` - Operaciones numéricas
- `psutil==5.9.5` - Información del sistema
- `pywin32==306` - APIs de Windows

## 🚀 Uso del Sistema

### Ejecución Principal (Sistema Simplificado - RECOMENDADO)
```bash
python main_simplified.py
```

### Ejecución del Sistema Completo
```bash
python main.py
```

### Tests Disponibles
```bash
python test_click_based_navigation.py
python test_sap_current_state.py
python test_final_automation.py
```

### Workflow Detallado (Estrategia Optimizada)
1. **Preparación**: Coloca archivos JSON en `queues/pending/`
2. **Ejecución**: El sistema ejecuta automáticamente:
   - Conecta al escritorio remoto (20.96.6.64)
   - Verifica SAP Desktop
   - Maximiza ventana
   - **Clic en botón de módulos** → **Clic en ventas** → **Clic en órdenes**
   - Procesa archivos JSON de la cola

### Verificación de Imágenes
El sistema verifica automáticamente que todas las imágenes de referencia estén presentes antes de iniciar.

### Logs y Debugging
- Logs detallados en `orderloader.log`
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

### Tests Disponibles
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
1. **Imágenes de Referencia**: Siempre verificar que existan en `assets/images/`
2. **Escritorio Remoto**: Debe estar abierto y conectado a 20.96.6.64
3. **SAP**: Debe estar iniciado en el escritorio remoto
4. **Permisos**: Ejecutar como administrador si hay problemas

### Patrones de Diseño
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
- Revisar `orderloader.log` para información detallada
- Verificar configuración en `src/config.py`
- Comprobar que todas las dependencias estén instaladas

---

**Nota**: Este proyecto está diseñado para uso interno de la empresa y requiere acceso específico al servidor SAP remoto.
