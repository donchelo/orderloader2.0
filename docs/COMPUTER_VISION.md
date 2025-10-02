# 📸 Guía de Captura de Imágenes para SAP Automation

Esta guía te ayudará a capturar las imágenes necesarias para que OrderLoader detecte automáticamente elementos en SAP Business One.

---

## 🎯 **¿Por qué necesitas capturar imágenes?**

OrderLoader utiliza **Computer Vision** (pyautogui) para detectar elementos visuales en pantalla. Para que funcione, necesita imágenes de referencia de cada botón, campo y menú que debe detectar.

---

## 🛠️ **Herramientas de Captura**

### **Opción 1: Recortes de Windows (Recomendada)**

1. **Abrir herramienta de recortes**:
   - Presiona `Win + Shift + S`
   - O busca "Recortes" en el menú inicio

2. **Seleccionar modo rectangular**

3. **Capturar el elemento específico**
   - Incluye solo el elemento (botón, campo, texto)
   - Incluye un poco de contexto alrededor (5-10 px)

4. **Guardar como PNG**
   - Pega en Paint: `Ctrl + V`
   - Guarda como PNG en la ubicación correcta

### **Opción 2: Script de Python**

Crea este archivo: `captura_helper.py`

```python
import pyautogui
import time

print("Posiciona el mouse sobre el elemento a capturar...")
print("Capturando en 5 segundos...")
time.sleep(5)

# Capturar pantalla completa
screenshot = pyautogui.screenshot()
screenshot.save("captura_completa.png")
print("✅ Captura guardada: captura_completa.png")

# Obtener posición del mouse
x, y = pyautogui.position()
print(f"📍 Posición del mouse: ({x}, {y})")
```

Luego recorta manualmente el elemento que necesitas.

---

## 📋 **Lista de Imágenes a Capturar**

### **PRIORIDAD ALTA (Esenciales para funcionalidad básica)**

#### **1. Navegación** → `assets/images/sap/navegacion/`

| Imagen | Descripción | Ejemplo |
|--------|-------------|---------|
| `menu_modulos.png` | Botón "Módulos" en menú principal | ![Módulos](ejemplo) |
| `menu_ventas.png` | Opción "Ventas" en el menú desplegable | ![Ventas](ejemplo) |
| `boton_orden_venta.png` | Botón "Orden de Venta" en submenú | ![Orden](ejemplo) |

**Ubicación en SAP**: Menú principal → Módulos → Ventas → Orden de Venta

#### **2. Formulario** → `assets/images/sap/formulario/`

| Imagen | Descripción | Notas |
|--------|-------------|-------|
| `campo_cliente.png` | Campo NIT/Cliente (label + input) | Captura el label "Cliente:" y parte del campo |
| `campo_fecha_documento.png` | Campo Fecha de Documento | Solo si necesitas modificarlo |
| `campo_fecha_entrega.png` | Campo Fecha de Entrega | Solo si necesitas modificarlo |

#### **3. Items** → `assets/images/sap/items/`

| Imagen | Descripción | Notas |
|--------|-------------|-------|
| `campo_codigo.png` | Primera celda de la tabla de items (Código) | Captura el header de columna |
| `campo_cantidad.png` | Columna Cantidad | Captura el header |
| `boton_agregar.png` | Botón "Agregar" o "+" | Después de llenar un item |

#### **4. Acciones** → `assets/images/sap/acciones/`

| Imagen | Descripción | Notas |
|--------|-------------|-------|
| `boton_guardar.png` | Botón "Actualizar" o "Guardar" | Generalmente en la barra inferior |
| `boton_agregar_y_cerrar.png` | Botón "Agregar y Cerrar" | Si existe en tu SAP |

---

## 📸 **Proceso de Captura Paso a Paso**

### **Paso 1: Preparar SAP**
1. Abre SAP Business One en Chrome
2. Maximiza la ventana
3. Asegúrate de que esté en el estado normal (sin popups ni mensajes)

### **Paso 2: Capturar Navegación**

1. **menu_modulos.png**:
   ```
   1. Ve al menú principal de SAP
   2. Presiona Win + Shift + S
   3. Selecciona solo el botón "Módulos"
   4. Pega en Paint y guarda como PNG en:
      orderloader/assets/images/sap/navegacion/menu_modulos.png
   ```

2. **menu_ventas.png**:
   ```
   1. Click en Módulos para abrir menú
   2. Captura la opción "Ventas"
   3. Guarda en: navegacion/menu_ventas.png
   ```

3. **boton_orden_venta.png**:
   ```
   1. Hover sobre "Ventas" para ver submenú
   2. Captura "Orden de Venta"
   3. Guarda en: navegacion/boton_orden_venta.png
   ```

### **Paso 3: Capturar Formulario**

1. **Abrir Orden de Venta**: Navega manualmente a Ventas → Orden de Venta

2. **campo_cliente.png**:
   ```
   1. Captura el label "Cliente:" y el campo de texto
   2. Incluye contexto alrededor (unos 10px)
   3. Guarda en: formulario/campo_cliente.png
   ```

### **Paso 4: Capturar Items**

1. **campo_codigo.png**:
   ```
   1. Captura el header de columna "Código de Artículo"
   2. O captura la primera celda vacía
   3. Guarda en: items/campo_codigo.png
   ```

2. **campo_cantidad.png**:
   ```
   1. Captura el header "Cantidad"
   2. Guarda en: items/campo_cantidad.png
   ```

### **Paso 5: Capturar Acciones**

1. **boton_guardar.png**:
   ```
   1. Captura el botón "Actualizar" o "Guardar"
   2. Generalmente está en la parte inferior
   3. Guarda en: acciones/boton_guardar.png
   ```

---

## ✅ **Verificación de Calidad**

Revisa que cada imagen capturada cumpla:

- ✅ **Formato PNG** (no JPG)
- ✅ **Tamaño adecuado**: ni muy pequeña ni muy grande
  - Recomendado: 50-200 píxeles de ancho
- ✅ **Nítida**: sin borrosidad
- ✅ **Buen contraste**: el elemento debe destacar
- ✅ **Sin cortes**: el elemento debe estar completo
- ✅ **Contexto mínimo**: incluye 5-10px alrededor

---

## 🧪 **Probar las Capturas**

Después de capturar las imágenes, prueba que sean detectables:

### **Script de Prueba**

Crea `test_imagenes.py`:

```python
import pyautogui
from pathlib import Path

assets_path = Path("assets/images/sap")

imagenes_prueba = [
    "navegacion/menu_modulos.png",
    "navegacion/menu_ventas.png",
    "navegacion/boton_orden_venta.png",
]

print("🔍 Probando detección de imágenes...\n")
print("IMPORTANTE: Asegúrate de que SAP esté abierto y visible\n")

input("Presiona Enter cuando SAP esté listo...")

for imagen in imagenes_prueba:
    ruta = assets_path / imagen

    if not ruta.exists():
        print(f"⚠️ {imagen} - NO EXISTE")
        continue

    try:
        location = pyautogui.locateOnScreen(str(ruta), confidence=0.8)
        if location:
            print(f"✅ {imagen} - DETECTADA en {location}")
        else:
            print(f"❌ {imagen} - NO DETECTADA (prueba recapturarla)")
    except Exception as e:
        print(f"❌ {imagen} - ERROR: {e}")

print("\n✅ Prueba completada")
```

Ejecuta:
```bash
cd orderloader
py test_imagenes.py
```

---

## 🎯 **Mínimo Viable**

Para empezar a probar, necesitas **mínimo estas 3 imágenes**:

1. ✅ `navegacion/menu_modulos.png`
2. ✅ `navegacion/menu_ventas.png`
3. ✅ `navegacion/boton_orden_venta.png`

Con estas 3, el sistema podrá al menos navegar al formulario de Orden de Venta.

---

## 💡 **Tips y Mejores Prácticas**

### **Si la detección falla:**

1. **Recaptura con más contexto**: Incluye más espacio alrededor
2. **Ajusta confidence**: En `config.py`, reduce `confidence` de 0.8 a 0.7
3. **Captura en diferentes momentos**: A veces SAP cambia ligeramente los colores
4. **Usa regiones**: Especifica región de búsqueda (ej: solo parte superior de pantalla)

### **Optimización:**

- **Imágenes pequeñas** se detectan más rápido
- **Alto contraste** mejora la detección
- **Elementos únicos** son más fáciles de detectar (evita texto genérico)

---

## 🚀 **Activar Modo Real**

Una vez tengas todas las imágenes:

1. **Edita `config.py`**:
   ```python
   SAP_AUTOMATION_CONFIG = {
       'simulation_mode': False,  # Cambiar a False
       'confidence': 0.8,
       ...
   }
   ```

2. **Ejecuta prueba**:
   ```bash
   py main.py
   ```

3. **Monitorea logs**:
   - Verifica que detecte correctamente cada elemento
   - Ajusta según sea necesario

---

## 📞 **Soporte**

Si tienes problemas:

1. **Revisa logs**: `logs/orderloader_YYYYMMDD.log`
2. **Activa screenshots de debug**: El sistema guarda capturas cuando no encuentra elementos
3. **Ajusta configuración**: Modifica `confidence` y `search_timeout` en `config.py`

---

**¡Éxito capturando las imágenes!** 📸✨
