# 📚 Documentación OrderLoader 2.0

Índice completo de la documentación del proyecto.

---

## 🚀 Inicio Rápido

**¿Primera vez aquí?** Lee primero:
1. [README.md principal](../README.md) - Descripción general del proyecto
2. [INSTALACION_Y_USO.md](INSTALACION_Y_USO.md) - Cómo instalar y ejecutar

---

## 📖 Guías de Usuario

### **Instalación y Uso**
- **[INSTALACION_Y_USO.md](INSTALACION_Y_USO.md)**
  - Instalación de dependencias
  - Configuración inicial
  - Cómo ejecutar el sistema
  - Estructura de archivos JSON

### **Computer Vision y SAP**
- **[COMPUTER_VISION.md](COMPUTER_VISION.md)**
  - Cómo capturar imágenes de referencia
  - Guía de configuración de pyautogui
  - Troubleshooting de detección de imágenes

- **[PRUEBA_NAVEGACION.md](PRUEBA_NAVEGACION.md)**
  - Prueba de navegación real en SAP
  - Validación de Computer Vision
  - Diagnóstico de problemas

---

## 🔧 Documentación Técnica

### **Arquitectura**
- **[ANALISIS_ARQUITECTURA.md](ANALISIS_ARQUITECTURA.md)**
  - Análisis completo de la arquitectura
  - Evaluación de buenas prácticas
  - Recomendaciones de mejora

### **Changelog**
- **[../CHANGELOG.md](../CHANGELOG.md)**
  - Historial completo de cambios
  - Versiones y mejoras

### **Buenas Prácticas**
- **[../claude.md](../claude.md)**
  - Principios de desarrollo
  - Estándares del proyecto

---

## 📂 Estructura de Archivos

```
orderloader2.0/
├── README.md                    ← Inicio: descripción del proyecto
├── CHANGELOG.md                 ← Historial de cambios
├── claude.md                    ← Buenas prácticas de desarrollo
│
├── docs/                        ← 📚 TODA LA DOCUMENTACIÓN
│   ├── README.md                ← Este archivo (índice)
│   ├── INSTALACION_Y_USO.md     ← Guía de instalación y uso
│   ├── COMPUTER_VISION.md       ← Guía de captura de imágenes
│   ├── PRUEBA_NAVEGACION.md     ← Guía de prueba de navegación
│   └── ANALISIS_ARQUITECTURA.md ← Análisis técnico del proyecto
│
├── venv/                        ← Entorno virtual Python
│
└── orderloader/                 ← 🎯 CÓDIGO FUENTE
    ├── main.py                  ← Código principal
    ├── config.py                ← Configuración
    ├── sap_automation.py        ← Computer Vision para SAP
    ├── test.py                  ← Tests unitarios
    ├── test_navegacion_real.py  ← Test de navegación real
    ├── requirements.txt         ← Dependencias
    │
    ├── data/                    ← Colas de procesamiento
    │   ├── pending/             ← JSON pendientes
    │   └── completed/           ← JSON procesados
    │
    ├── assets/images/sap/       ← Imágenes de referencia CV
    │   ├── navegacion/          ← Imágenes de menús
    │   ├── formulario/          ← Imágenes de formulario
    │   ├── items/               ← Imágenes de items
    │   └── acciones/            ← Imágenes de botones
    │
    ├── backups/                 ← Backups automáticos
    └── logs/                    ← Logs del sistema
```

---

## 🎯 Rutas Comunes

### **Por Tarea**

| Quiero... | Leer... |
|-----------|---------|
| Instalar el sistema | [INSTALACION_Y_USO.md](INSTALACION_Y_USO.md) |
| Capturar imágenes SAP | [COMPUTER_VISION.md](COMPUTER_VISION.md) |
| Probar navegación | [PRUEBA_NAVEGACION.md](PRUEBA_NAVEGACION.md) |
| Entender la arquitectura | [ANALISIS_ARQUITECTURA.md](ANALISIS_ARQUITECTURA.md) |
| Ver cambios recientes | [../CHANGELOG.md](../CHANGELOG.md) |

### **Por Nivel**

- **🟢 Principiante:** README.md → INSTALACION_Y_USO.md
- **🟡 Intermedio:** COMPUTER_VISION.md → PRUEBA_NAVEGACION.md
- **🔴 Avanzado:** ANALISIS_ARQUITECTURA.md → Código fuente

---

## 🆘 Ayuda

### **Problemas Comunes**

1. **"No detecta imágenes en SAP"**
   → Ver [COMPUTER_VISION.md](COMPUTER_VISION.md) sección Troubleshooting

2. **"Alt+Tab no activa Chrome"**
   → Ver [PRUEBA_NAVEGACION.md](PRUEBA_NAVEGACION.md) sección Diagnóstico

3. **"Error al ejecutar test.py"**
   → Ver [INSTALACION_Y_USO.md](INSTALACION_Y_USO.md) sección Testing

### **Contacto**

Para reportar bugs o sugerir mejoras:
- GitHub Issues: https://github.com/donchelo/orderloader2.0/issues

---

## 📝 Convenciones

### **Formato de Documentación**
- 📚 = Documentación
- 🎯 = Código fuente
- ⚙️ = Configuración
- 🧪 = Testing
- 🐛 = Debugging
- ⚠️ = Importante/Advertencia
- ✅ = Completado/Correcto
- ❌ = Error/Incorrecto

### **Niveles de Prioridad**
- 🔥 ALTA - Hacer inmediatamente
- ⚠️ MEDIA - Hacer pronto
- ✨ BAJA - Mejora futura

---

**Última actualización:** 2025-10-01
**Versión:** 2.0.1
