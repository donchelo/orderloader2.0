# 📘 Guía de Ejecución - OrderLoader 2.0

## ✅ **Estado del Sistema**
- **Fecha de preparación**: 01/10/2025
- **Versión**: 2.0
- **Estado**: ✅ LISTO PARA PRUEBAS

---

## 🎯 **¿Qué hace OrderLoader?**

Sistema de automatización que lee archivos JSON con órdenes de compra y las carga automáticamente en SAP Business One usando Computer Vision (pyautogui).

---

## 📋 **Pre-requisitos**

### **1. Software Instalado**
- ✅ Python 3.13.7
- ✅ pyautogui 0.9.54
- ✅ psutil 5.9.5

### **2. Estructura de Directorios**
```
orderloader/
├── data/
│   ├── pending/       ✅ (2 archivos JSON listos)
│   └── completed/     ✅ (vacío)
├── assets/images/sap/ ✅ (3 imágenes)
├── backups/           ✅ (vacío)
├── logs/              ✅ (vacío)
├── main.py            ✅
├── config.py          ✅
└── test.py            ✅
```

### **3. Archivos JSON Pendientes**
- ✅ `4500225929.PDF.json` - Orden real de COMODIN S.A.S.
- ✅ `test_orden_simple.json` - Orden de prueba

---

## 🚀 **Cómo Ejecutar**

### **Opción 1: Ejecución Completa (Recomendada para producción)**

1. **Abrir SAP Business One en Chrome**
   - Asegúrate de que SAP está abierto
   - La ventana debe estar accesible con Alt+Tab

2. **Ejecutar el sistema**
   ```bash
   cd "C:\Users\EQUIPO\Documents\Software\orderloader2.0\orderloader"
   py main.py
   ```

3. **Confirmar inicio**
   - El sistema mostrará el estado de archivos pendientes
   - Presiona Enter para iniciar

4. **Observar el proceso**
   - El sistema activará la ventana SAP (Alt+Tab)
   - Maximizará la ventana (Win+Up)
   - Procesará cada archivo JSON secuencialmente
   - Moverá archivos completados a `data/completed/`

### **Opción 2: Ejecutar Tests (Recomendada antes de producción)**

```bash
cd "C:\Users\EQUIPO\Documents\Software\orderloader2.0\orderloader"
py test.py
```

**Resultado esperado**: `7 ✅ | 0 ❌` - TODOS LOS TESTS PASARON

---

## 📊 **Flujo de Ejecución**

```
1. Inicio del Sistema
   ↓
2. Validación de permisos y directorios
   ↓
3. Activación de ventana SAP (Alt+Tab)
   ↓
4. Maximización de ventana (Win+Up)
   ↓
5. Estabilización del sistema (3 segundos)
   ↓
6. Procesamiento de archivos JSON:
   - Crear backup automático
   - Validar estructura JSON
   - Procesar orden (SIMULADO por ahora)
   - Mover a completed/
   ↓
7. Limpieza de backups antiguos
   ↓
8. Reporte de métricas finales
```

---

## ⚠️ **IMPORTANTE - Estado Actual**

### **✅ Funcionalidad Implementada**
1. ✅ Arquitectura modular completa
2. ✅ Sistema de backup automático
3. ✅ Métricas y logging
4. ✅ Validación de JSON
5. ✅ Gestión de colas
6. ✅ Recuperación de errores (retry)

### **⚠️ Funcionalidad PENDIENTE (Fase 3)**
1. ⚠️ **Lógica de Computer Vision completa**
   - Actualmente solo SIMULA el procesamiento
   - Necesita implementar:
     - Detección de imágenes con `pyautogui.locateOnScreen()`
     - Navegación por menús SAP
     - Rellenado de formularios
     - Carga de items

---

## 🔧 **Próximos Pasos para Completar el Sistema**

### **Fase 3: Implementar Computer Vision**

1. **Capturar Screenshots de SAP**
   - Ejecutar SAP y capturar imágenes de:
     - Menú "Módulos"
     - Menú "Ventas"
     - Botón "Orden de Venta"
     - Campos de formulario (Cliente, Fecha, etc.)
     - Botón "Agregar"

2. **Implementar funciones de navegación**
   ```python
   def navigate_to_sales_order():
       # Detectar y hacer clic en "Módulos"
       # Detectar y hacer clic en "Ventas"
       # Detectar y hacer clic en "Orden de Venta"
       pass

   def fill_order_form(order_data):
       # Rellenar campos del formulario
       # NIT del cliente
       # Fecha de documento
       # etc.
       pass

   def add_items(items):
       # Para cada item:
       # - Rellenar código
       # - Rellenar cantidad
       # - Rellenar precio
       # - Hacer clic en "Agregar"
       pass
   ```

3. **Probar con 1 archivo**
   - Ejecutar con `test_orden_simple.json`
   - Ajustar tiempos de espera
   - Validar en SAP

4. **Escalar a múltiples archivos**

---

## 📁 **Archivos Importantes**

### **Logs**
- Ubicación: `logs/orderloader_YYYYMMDD.log`
- Contiene: Información detallada de cada ejecución

### **Métricas**
- Ubicación: `metrics.json`
- Contiene: Estadísticas de rendimiento, tasa de éxito, errores

### **Backups**
- Ubicación: `backups/`
- Contiene: Respaldos automáticos de archivos procesados

---

## 🆘 **Solución de Problemas**

### **Error: "SAP no detectado"**
- Asegúrate de que SAP está abierto en Chrome
- Verifica que la ventana sea accesible con Alt+Tab

### **Error: "No module named pip"**
Ya resuelto. Si reaparece:
```bash
py -m ensurepip --default-pip
py -m pip install -r requirements.txt
```

### **Error de encoding (emojis no se muestran)**
Ya resuelto en test.py. El sistema funciona correctamente en Windows.

### **Tests fallan**
Ejecutar:
```bash
py test.py
```
Si falla algún test, revisar los logs para más detalles.

---

## 📈 **Métricas del Sistema**

Después de cada ejecución, revisa:
- **Tasa de éxito**: % de archivos procesados correctamente
- **Tiempo de procesamiento**: Segundos por archivo
- **Intentos de retry**: Número de reintentos automáticos
- **Archivos procesados**: Total en la sesión

---

## ✨ **Características Avanzadas**

### **Retry Automático**
- 3 intentos por operación crítica
- Backoff exponencial (1s → 2s → 4s)
- Recuperación automática de errores transitorios

### **Backup Automático**
- Backup antes de procesar cada archivo
- Compresión gzip opcional
- Limpieza automática (mantiene últimos 10)

### **Métricas en Tiempo Real**
- Tracking de cada archivo
- Registro de errores con timestamps
- Persistencia en JSON

---

**✅ Sistema listo para pruebas con SAP abierto**

*Última actualización: 01/10/2025*
