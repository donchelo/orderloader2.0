# 🎯 OrderLoader 2.0 - Sistema de Automatización SAP

## 📋 **Descripción**

Sistema de automatización SAP simplificado y optimizado. **Versión 2.0 enfocada en procesamiento de cola con navegación automática por Alt+Tab.**

## 🚀 **Instalación y Uso**

### **Instalación**
```bash
cd orderloader
pip install -r requirements.txt
```

### **Uso**
```bash
python main.py
```

### **Testing**
```bash
python test.py
```

## 🏗️ **Estructura del Proyecto**

```
orderLoader2.0/
├── 📁 orderloader/               # 🎯 SISTEMA PRINCIPAL
│   ├── 📄 main.py                # Código principal (400 líneas)
│   ├── 📄 config.py              # Configuración centralizada
│   ├── 📄 test.py                # Test único y completo
│   ├── 📄 requirements.txt       # Solo 2 dependencias (pyautogui, psutil)
│   ├── 📁 assets/images/sap/     # 3 imágenes esenciales para navegación
│   │   ├── sap_modulos_menu_button.png
│   │   ├── sap_ventas_menu_button.png
│   │   └── sap_ventas_order_button.png
│   └── 📁 data/                  # Datos del sistema
│       ├── pending/              # Archivos JSON pendientes
│       └── completed/            # Archivos procesados
├── 📁 assets/                    # 📚 Imágenes de referencia (legacy)
│   └── 📁 images/                # Imágenes originales para Computer Vision
│       ├── core/                 # Imágenes principales
│       └── sap/                  # Imágenes específicas de SAP
├── 📁 queues/                    # 📦 Datos existentes (legacy)
│   ├── pending/                  # Archivos pendientes (legacy)
│   └── completed/                # Archivos completados (legacy)
├── 📁 Comparar/                  # 📊 Archivos de comparación
│   └── Validados/                # Archivos validados
├── 📄 claude.md                  # Documentación técnica original
└── 📄 README.md                  # Esta documentación
```

## 🎯 **Características**

- ✅ **Navegación por Alt+Tab** - Activación automática de ventanas
- ✅ **Procesamiento de cola** - Gestión automática de archivos JSON
- ✅ **Validación robusta** - Verificación completa de datos
- ✅ **Logging detallado** - Seguimiento completo de operaciones
- ✅ **Recuperación de errores** - Manejo inteligente de fallos
- ✅ **Estructura modular** - Separación clara de responsabilidades

## 🔧 **Funcionalidad**

1. **Activar ventana SAP** - Usando Alt+Tab para cambiar a Chrome
2. **Verificar SAP** - Confirmar que la aplicación está visible
3. **Maximizar ventana** - Optimizar la visualización
4. **Procesar archivos JSON** - Validar y procesar datos de órdenes
5. **Gestión de colas** - Mover archivos procesados automáticamente
6. **Sistema de logging** - Registro detallado en `logs/`

## 📊 **Métricas del Sistema**

- **Archivos principales**: 8 archivos en orderloader/
- **Líneas de código**: ~400 líneas en main.py
- **Dependencias**: 2 librerías (pyautogui, psutil)
- **Imágenes de navegación**: 3 imágenes esenciales
- **Complejidad**: Media (navegación + procesamiento)

## 🚀 **Uso Detallado**

### **Preparación**
1. Coloca archivos JSON en `orderloader/data/pending/`
2. Asegúrate de que SAP esté abierto en Chrome
3. La ventana de SAP debe ser accesible con Alt+Tab

### **Ejecución**
```bash
cd orderloader
python main.py
```

### **Workflow Automático**
1. **Activación**: Presiona Alt+Tab para activar ventana SAP
2. **Verificación**: Confirma que SAP esté visible
3. **Maximización**: Optimiza la ventana para mejor visualización
4. **Procesamiento**: Procesa archivos JSON de la cola
5. **Finalización**: Mueve archivos procesados a `completed/`

### **Logs y Debugging**
- Logs detallados en `orderloader/logs/orderloader_YYYYMMDD.log`
- Información de cada operación
- Errores y advertencias

## 🔒 **Seguridad y Failsafe**

- **Failsafe**: Mover mouse a esquina superior izquierda para detener
- **Pausas**: Delays entre acciones para estabilidad
- **Verificación**: Múltiples niveles de verificación

## 🧪 **Testing**

```bash
cd orderloader
python test.py
```

Verifica:
- Inicialización del sistema
- Estructura de directorios
- Procesamiento de JSON
- Gestión de colas

## 📁 **Directorios del Proyecto**

### **🎯 Sistema Principal (`orderloader/`)**
- **Archivos activos**: main.py, config.py, test.py
- **Datos**: data/pending/, data/completed/
- **Imágenes**: assets/images/sap/ (3 imágenes activas)
- **Logs**: logs/ (se crea automáticamente)

### **📚 Recursos Legacy (`assets/`, `queues/`)**
- **assets/**: Imágenes de referencia (no se usan activamente)
- **queues/**: Datos legacy (migrar a orderloader/data/)
- **Comparar/**: Archivos de comparación y validación

## ⚠️ **Notas Importantes**

1. **Sistema Principal**: Usa `orderloader/` para todo el funcionamiento
2. **Imágenes Activas**: Solo 3 imágenes en `orderloader/assets/images/sap/`
3. **Datos Actuales**: Usa `orderloader/data/` para archivos JSON
4. **Legacy**: Las carpetas `assets/` y `queues/` son solo para referencia
5. **Navegación**: El sistema usa Alt+Tab, no Computer Vision

## 🎯 **Recomendaciones**

- **Para uso diario**: Solo interactúa con `orderloader/`
- **Para desarrollo**: Revisa `claude.md` para documentación técnica
- **Para migración**: Mueve datos de `queues/` a `orderloader/data/`
- **Para imágenes**: Actualiza solo las 3 imágenes en `orderloader/assets/images/sap/`

---

**¡Sistema simplificado y listo para usar!** 🚀