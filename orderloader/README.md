# 🎯 OrderLoader - Sistema Simple y Funcional

## 📋 **Descripción**

Sistema de automatización SAP simple y optimizado. **Una sola clase, una sola forma de ejecutar.**

## 🚀 **Instalación y Uso**

### **Instalación**
```bash
cd orderloader
pip install -r requirements.txt
```

### **Uso - UNA SOLA FORMA**
```bash
python main.py
```

### **Testing**
```bash
python test.py
```

## 🏗️ **Estructura del Proyecto**

```
orderloader/
├── 📄 main.py                    # Código principal (300 líneas)
├── 📄 config.py                  # Configuración simple
├── 📄 test.py                    # Test único y completo
├── 📄 requirements.txt           # Solo 2 dependencias
├── 📄 README.md                  # Esta documentación
├── 📁 data/                      # Datos del sistema
│   ├── pending/                  # Archivos JSON pendientes
│   └── completed/                # Archivos procesados
└── 📁 logs/                      # Logs del sistema
```

## 🎯 **Características**

- ✅ **Sistema simple** - Una sola clase, todo en un archivo
- ✅ **Sin redundancias** - Código limpio y directo
- ✅ **Una sola forma de ejecutar** - `python main.py`
- ✅ **Fácil mantenimiento** - Estructura clara y simple
- ✅ **Funcional** - Cumple todos los objetivos

## 🔧 **Funcionalidad**

1. **Conectar al escritorio remoto** (20.96.6.64)
2. **Verificar que SAP esté abierto** (opcional)
3. **Procesar archivos JSON** de la cola (`data/pending/`)
4. **Mover archivos completados** automáticamente (`data/completed/`)
5. **Sistema de logging** detallado (`logs/`)

## 📊 **Métricas de Simplicidad**

- **Archivos totales**: 8 archivos principales
- **Líneas de código**: ~300 líneas en main.py
- **Dependencias**: 2 librerías (pyautogui, psutil)
- **Complejidad**: Mínima
- **Formas de ejecutar**: 1 sola (`python main.py`)

## 🚀 **Uso**

### **Ejecución Principal**
```bash
cd orderloader
python main.py
```

### **Workflow**
1. **Preparación**: Coloca archivos JSON en `data/pending/`
2. **Ejecución**: El sistema ejecuta automáticamente:
   - Conecta al escritorio remoto (20.96.6.64)
   - Verifica SAP Desktop
   - Maximiza ventana
   - Procesa archivos JSON de la cola
   - Mueve archivos procesados a `data/completed/`

### **Logs y Debugging**
- Logs detallados en `logs/orderloader_YYYYMMDD.log`
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

---

**¡Sistema simple, funcional y listo para usar!** 🚀