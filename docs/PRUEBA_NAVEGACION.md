# 🧪 Guía de Prueba de Navegación Real - OrderLoader

## 📋 Objetivo
Probar que el sistema puede navegar desde PowerShell hasta el formulario de Orden de Venta en SAP usando Computer Vision (pyautogui).

---

## ⚠️ Consideraciones Importantes

### **Flujo PowerShell → Chrome/SAP**
El sistema SIEMPRE se ejecuta desde PowerShell, por lo que:
1. **PowerShell está activo** al inicio (ventana actual)
2. **Alt+Tab** cambia a Chrome/SAP automáticamente
3. **NO tocar** el teclado/mouse durante la ejecución

### **Imágenes de Referencia**
El sistema ya tiene 3 imágenes capturadas:
- `navegacion/menu_modulos.png` - Botón "Módulos"
- `navegacion/menu_ventas.png` - Opción "Ventas"
- `navegacion/boton_orden_venta.png` - Botón "Orden de Venta"

---

## 🚀 Preparación

### **1. Requisitos Previos**
```bash
✅ SAP Business One abierto en Chrome
✅ Ventana de SAP visible (no minimizada)
✅ PowerShell abierto en el directorio del proyecto
✅ No hay popups o mensajes bloqueando SAP
```

### **2. Posición Inicial**
```
[PowerShell] ← Ventana activa
[Chrome - SAP] ← Ventana en segundo plano (visible con Alt+Tab)
```

---

## 🧪 Ejecutar la Prueba

### **Paso 1: Abrir PowerShell**
```bash
cd C:\Users\EQUIPO\Documents\Software\orderloader2.0\orderloader
```

### **Paso 2: Ejecutar Script de Prueba**
```bash
py test_navegacion_real.py
```

### **Paso 3: Seguir Instrucciones**
El script mostrará:
```
🧪 TEST DE NAVEGACIÓN REAL - OrderLoader Computer Vision

⚠️  IMPORTANTE:
   • Este script se ejecuta desde PowerShell
   • SAP debe estar abierto en Chrome (pero NO activo)
   • El script hará Alt+Tab automáticamente
   • NO toques el teclado/mouse durante la ejecución

Presiona Enter cuando estés listo para iniciar...
```

### **Paso 4: NO Tocar Nada**
Una vez presiones Enter:
- Countdown 5 segundos
- Alt+Tab automático
- Maximización automática
- Navegación con Computer Vision

---

## 📊 Resultados Esperados

### **✅ ÉXITO**
```
🎉 ¡ÉXITO! Formulario de Orden de Venta abierto

✅ El sistema detectó correctamente:
   • Botón 'Módulos'
   • Menú 'Ventas'
   • Botón 'Orden de Venta'

📸 Screenshots guardados para referencia
```

**Archivos generados:**
- `debug_inicial_YYYYMMDD_HHMMSS.png` - Pantalla antes de navegar
- `debug_formulario_abierto_YYYYMMDD_HHMMSS.png` - Formulario abierto

### **❌ FALLO**
```
❌ FALLO: No se pudo completar la navegación

🔍 Posibles causas:
   • Imágenes de referencia no coinciden
   • SAP no estaba visible
   • Confidence demasiado alto

📋 Acciones recomendadas:
   1. Revisar screenshots en debug_*.png
   2. Comparar con imágenes de referencia
   3. Re-capturar imágenes si es necesario
   4. Reducir confidence a 0.6
```

**Archivos generados:**
- `debug_error_YYYYMMDD_HHMMSS.png` - Pantalla al momento del error

---

## 🔧 Diagnóstico de Problemas

### **Problema 1: Alt+Tab no activa Chrome**
**Síntoma:** El sistema se queda en PowerShell

**Solución:**
1. Verificar que Chrome está realmente abierto
2. Verificar que SAP está cargado en Chrome
3. Probar Alt+Tab manual para verificar el orden de ventanas

### **Problema 2: No detecta "Módulos"**
**Síntoma:** Timeout buscando menu_modulos.png

**Solución:**
1. Revisar `debug_inicial_YYYYMMDD_HHMMSS.png`
2. Comparar con `navegacion/menu_modulos.png`
3. Si no coinciden → re-capturar la imagen
4. Si es similar → reducir confidence:
   ```python
   # En test_navegacion_real.py línea ~145
   sap_automation.confidence = 0.6  # Cambiar de 0.7 a 0.6
   ```

### **Problema 3: No detecta "Ventas" o "Orden de Venta"**
**Síntoma:** Detecta Módulos pero falla en pasos siguientes

**Solución:**
1. Puede ser timing - menús se cierran antes de detectar
2. Aumentar delays en `sap_automation.py`:
   ```python
   time.sleep(1.5)  # Ya está actualizado a 1.5s
   ```
3. Re-capturar imágenes con menú abierto y visible

### **Problema 4: Ventana no maximiza**
**Síntoma:** Win+Up no funciona

**Solución:**
1. Verificar que la ventana no está bloqueada
2. Hacer clic manual en Chrome antes de ejecutar
3. Aumentar delay después de maximizar

---

## 📸 Re-captura de Imágenes

Si las imágenes no detectan correctamente:

### **Método 1: Recortes de Windows**
```
1. Win + Shift + S
2. Seleccionar elemento específico (incluir contexto)
3. Pegar en Paint
4. Guardar como PNG en assets/images/sap/navegacion/
```

### **Método 2: Durante la Prueba**
```
1. Pausar ejecución (Ctrl+C)
2. Ir a SAP manualmente
3. Capturar elemento visible
4. Guardar con mismo nombre
5. Re-ejecutar prueba
```

### **Consejos:**
- ✅ Incluir 5-10 píxeles de contexto alrededor
- ✅ Asegurarse de que el texto sea nítido
- ✅ Capturar con ventana maximizada
- ✅ Sin popups o tooltips en la captura

---

## 🎯 Próximos Pasos (Si la Prueba es Exitosa)

### **1. Capturar Imágenes del Formulario**
Una vez dentro del formulario:
```bash
📸 Capturar:
   • Campo "Cliente" → formulario/campo_cliente.png
   • Primera celda de items → items/campo_codigo.png
   • Botón "Guardar" → acciones/boton_guardar.png
```

### **2. Actualizar Configuración**
Editar `config.py`:
```python
SAP_AUTOMATION_CONFIG = {
    'simulation_mode': False,  # ← Cambiar a False
    'confidence': 0.7,  # Usar el valor que funcionó
    'search_timeout': 15,
    ...
}
```

### **3. Prueba Completa**
```bash
py main.py
```

---

## 📝 Notas Técnicas

### **Configuración de Prueba**
```python
# test_navegacion_real.py
simulation_mode = False  # Modo real
confidence = 0.7  # Más permisivo que 0.8 default
search_timeout = 15  # Más tiempo que 10s default
```

### **Delays Configurados**
```python
WINDOW_ACTIVATION_DELAY = 1.0s  # Después de Alt+Tab
SYSTEM_STABILIZATION_DELAY = 3.0s  # Antes de navegar
WINDOW_MAXIMIZE_DELAY = 1.0s  # Después de Win+Up
Entre clicks = 1.5s  # En navegación
```

### **Archivos Involucrados**
```
test_navegacion_real.py  ← Script de prueba
sap_automation.py        ← Lógica de Computer Vision
config.py                ← Configuración
assets/images/sap/       ← Imágenes de referencia
  └── navegacion/
      ├── menu_modulos.png
      ├── menu_ventas.png
      └── boton_orden_venta.png
```

---

## ✅ Checklist de Validación

Antes de ejecutar la prueba:
- [ ] SAP abierto en Chrome
- [ ] Chrome no minimizado
- [ ] PowerShell en directorio correcto
- [ ] No hay popups en SAP
- [ ] Imágenes de referencia existen en navegacion/

Durante la prueba:
- [ ] Alt+Tab activa Chrome
- [ ] Ventana se maximiza
- [ ] Detecta botón "Módulos"
- [ ] Hace click en "Módulos"
- [ ] Detecta "Ventas"
- [ ] Hace click en "Ventas"
- [ ] Detecta "Orden de Venta"
- [ ] Hace click en "Orden de Venta"
- [ ] Formulario se abre

Si todos los checks pasan: ✅ **Sistema funcionando correctamente**

---

**¡Buena suerte con la prueba!** 🚀
