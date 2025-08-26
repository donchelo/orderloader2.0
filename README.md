# OrderLoader 2.0 - Automatización de SAP para Órdenes de Venta

Sistema automatizado especializado para navegación en SAP hasta el formulario de órdenes de venta, con capacidades avanzadas de gestión de escritorio remoto.

## 🚀 Características Principales

- **Gestión Avanzada de Escritorio Remoto**: Múltiples estrategias de activación y maximización de ventanas
- **Reconocimiento de Imágenes**: Detección robusta de elementos en pantalla usando OpenCV
- **Sistema de Recuperación**: Manejo automático de errores con reintentos inteligentes
- **Logging Detallado**: Registro completo de todas las operaciones para debugging
- **Arquitectura Modular**: Código organizado siguiendo las mejores prácticas

## 📁 Estructura del Proyecto

```
orderLoader2.0/
├── src/                          # Código fuente principal
│   ├── core/                     # Funcionalidades principales
│   │   ├── remote_desktop_manager.py  # Gestión de escritorio remoto
│   │   ├── image_recognition.py       # Reconocimiento de imágenes
│   │   └── sap_automation.py          # Automatización de SAP
│   ├── utils/                    # Utilidades
│   │   └── logger.py             # Configuración de logging
│   └── config.py                 # Configuración centralizada
├── tests/                        # Tests del sistema
│   └── test_remote_desktop.py    # Test unificado
├── assets/                       # 🎨 Recursos del proyecto
│   └── images/                   # Imágenes de referencia para Computer Vision
│       ├── core/                 # Imágenes principales
│       └── sap/                  # Imágenes de SAP
├── main.py                       # Punto de entrada principal
├── install.bat                   # Script de instalación
└── README.md                     # Este archivo
```

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8 o superior
- Windows 10/11
- Acceso a escritorio remoto con SAP

### Instalación Automática
1. Ejecuta `install.bat` como administrador
2. El script instalará todas las dependencias automáticamente
3. Verifica que la instalación fue exitosa

### Instalación Manual
```bash
pip install pyautogui==0.9.54
pip install opencv-python==4.8.1.78
pip install pillow==10.0.1
pip install numpy==1.24.3
pip install psutil==5.9.5
pip install pywin32==306
```

## 🎯 Uso

### Ejecución Principal
```bash
python main.py
```

### Ejecución de Tests
```bash
python tests/test_remote_desktop.py
```

## 🔧 Configuración

El archivo `src/config.py` contiene todas las configuraciones del sistema:

- **RECOGNITION_CONFIG**: Configuración de reconocimiento de imágenes
- **REMOTE_DESKTOP_CONFIG**: Configuración del escritorio remoto
- **ACTIVATION_STRATEGIES**: Estrategias de activación de ventanas
- **KEYBOARD_SHORTCUTS**: Atajos de teclado
- **LOGGING_CONFIG**: Configuración de logging

## 📋 Funcionalidades

### 1. Gestión de Escritorio Remoto
- Detección automática de ventanas de escritorio remoto
- Múltiples estrategias de activación (Alt+Tab, PowerShell, Win+Tab)
- Maximización automática de ventanas
- Verificación visual de estado

### 2. Automatización de SAP
- Navegación automática a módulos
- Apertura de menús de ventas
- Acceso a formularios de órdenes de venta
- Verificación de estados de la aplicación

### 3. Sistema de Recuperación
- Reintentos automáticos en caso de fallo
- Múltiples estrategias de activación
- Logging detallado para debugging
- Manejo robusto de errores

## 🧪 Testing

El sistema incluye un test unificado que verifica:

1. **RemoteDesktopManager**: Detección y activación de ventanas
2. **Automatización Completa**: Flujo completo de SAP
3. **Activación Rápida**: Pruebas de rendimiento

## 📝 Logs

Los logs se guardan en `orderloader.log` e incluyen:
- Información detallada de cada operación
- Errores y advertencias
- Tiempos de ejecución
- Estados de verificación

## 🔒 Seguridad

- **Failsafe**: Mueve el mouse a la esquina superior izquierda para detener
- **Pausas**: Delays entre acciones para estabilidad
- **Verificación**: Múltiples niveles de verificación antes de continuar

## 🐛 Troubleshooting

### Problemas Comunes

1. **Error de dependencias**: Ejecuta `install.bat` nuevamente
2. **No encuentra ventana**: Verifica que el escritorio remoto esté abierto
3. **Error de imágenes**: Verifica que las imágenes estén en `reference_images/`
4. **Problemas de encoding**: Los errores de Unicode son cosméticos, no afectan funcionalidad

### Logs de Debug
Revisa `orderloader.log` para información detallada de errores.

## 📈 Mejoras en la Versión 2.0

- ✅ Arquitectura modular y escalable
- ✅ Separación de responsabilidades
- ✅ Sistema de logging mejorado
- ✅ Tests organizados
- ✅ Configuración centralizada
- ✅ Manejo robusto de errores
- ✅ Múltiples estrategias de activación
- ✅ Verificación visual mejorada

## 🤝 Contribución

1. Mantén la estructura modular
2. Agrega tests para nuevas funcionalidades
3. Documenta cambios en el README
4. Sigue las convenciones de código existentes

## 📄 Licencia

Este proyecto es para uso interno de la empresa.

---

**OrderLoader 2.0** - Automatización inteligente para SAP
