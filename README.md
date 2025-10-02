# OrderLoader 2.0

Sistema de automatización para crear órdenes de venta en SAP Business One usando Computer Vision.

---

## Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/donchelo/orderloader2.0.git
cd orderloader2.0

# 2. Crear entorno virtual
py -3 -m venv venv
.\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r orderloader/requirements.txt
```

---

## Uso

### Ejecutar Tests
```bash
cd orderloader
py test.py
```
**Resultado esperado:** `7 ✅ | 0 ❌`

### Ejecutar Sistema
```bash
cd orderloader
py main.py
```

**Requisitos:**
- SAP Business One abierto en Chrome
- Archivos JSON en `orderloader/data/pending/`

---

## Estructura del Proyecto

```
orderloader2.0/
├── orderloader/
│   ├── main.py                  # Sistema principal
│   ├── config.py                # Configuración
│   ├── sap_automation.py        # Computer Vision
│   ├── test.py                  # Tests
│   ├── requirements.txt
│   │
│   ├── data/
│   │   ├── pending/             # JSON a procesar
│   │   └── completed/           # JSON procesados
│   │
│   └── assets/images/sap/
│       └── navegacion/          # Imágenes de referencia (3)
│
└── venv/                        # Entorno virtual (ignorado en Git)
```

---

## Formato JSON de Órdenes

```json
{
  "orden_compra": "TEST001",
  "fecha_documento": "01/10/2025",
  "fecha_entrega": "15/10/2025",
  "comprador": {
    "nit": "900123456",
    "nombre": "EMPRESA DE PRUEBA S.A.S."
  },
  "items": [
    {
      "codigo": "PROD001",
      "descripcion": "PRODUCTO DE PRUEBA 1",
      "cantidad": 100,
      "precio_unitario": 1500,
      "precio_total": 150000,
      "fecha_entrega": "15/10/2025"
    }
  ],
  "valor_total": 150000,
  "total_items_unicos": 1,
  "numero_items_totales": 100
}
```

Coloca los JSON en `orderloader/data/pending/` y el sistema los procesará automáticamente.

---

## Configuración

Edita `orderloader/config.py`:

```python
# Modo simulación (True = simular, False = real)
SAP_AUTOMATION_CONFIG = {
    'simulation_mode': True,
    'confidence': 0.8,
    'search_timeout': 10,
}
```

---

## Flujo del Sistema

1. **Inicio** - Valida permisos y directorios
2. **Alt+Tab** - Activa ventana Chrome/SAP
3. **Win+Up** - Maximiza ventana
4. **Procesa JSON** - Lee pending/, crea backup, procesa orden
5. **Mueve a completed/** - Archivos procesados exitosamente
6. **Reporta métricas** - Éxito/fallos, tiempos

---

## Arquitectura

```python
OrderLoader (Orquestador)
├── WindowManager      # Alt+Tab, maximizar
├── FileProcessor      # JSON, validación, backup
├── QueueManager       # pending → completed
├── MetricsCollector   # Métricas de rendimiento
└── SAPAutomation      # Computer Vision (pyautogui)
```

---

## Computer Vision

### Imágenes de Navegación (Capturadas)
- `navegacion/menu_modulos.png` - Botón "Módulos"
- `navegacion/menu_ventas.png` - Menú "Ventas"
- `navegacion/boton_orden_venta.png` - "Orden de Venta"

### Capturar Nuevas Imágenes
1. Abre SAP maximizado
2. Win+Shift+S para capturar
3. Recorta solo el botón/campo (incluye 5-10px alrededor)
4. Guarda en `orderloader/assets/images/sap/[carpeta]/`

**Carpetas:**
- `navegacion/` - Menús
- `formulario/` - Campos del formulario
- `items/` - Tabla de items
- `acciones/` - Botones (guardar, agregar)

---

## Prueba de Navegación Real

```bash
cd orderloader
py test_navegacion_real.py
```

Este script:
1. Hace Alt+Tab automático (PowerShell → Chrome)
2. Busca y hace click en "Módulos" (Computer Vision)
3. Busca y hace click en "Ventas"
4. Busca y hace click en "Orden de Venta"
5. Guarda screenshots de debug si falla

**Si falla la detección:**
- Revisar `debug_*.png` para ver qué está detectando
- Re-capturar imagen con más contexto
- Reducir `confidence` en config.py (0.8 → 0.7)

---

## Tests Unitarios

7 tests implementados:

1. **Inicialización** - Sistema se crea correctamente
2. **Directorios** - pending/, completed/, backups/ existen
3. **Procesamiento JSON** - Valida y procesa correctamente
4. **Gestión de colas** - Estado de pending/completed
5. **Validación sistema** - Permisos correctos
6. **Entorno SAP** - WindowManager funcional
7. **Manejo de errores** - Códigos de error específicos

---

## Importante: Flujo PowerShell

El sistema se ejecuta desde PowerShell, por lo tanto:
- PowerShell está activo al inicio
- **Alt+Tab automático** cambia a Chrome/SAP
- **No tocar** teclado/mouse durante ejecución

Esto está implementado en `WindowManager.activate_sap_chrome_window()`.

---

## Logs y Debug

```
orderloader/logs/orderloader_YYYYMMDD.log    # Logs detallados
orderloader/backups/                         # Backups automáticos
orderloader/metrics.json                     # Métricas de rendimiento
debug_*.png                                  # Screenshots de debug (si falla CV)
```

---

## Próximos Pasos

### Actual: Modo Simulación ✅
- ✅ Tests pasando (7/7)
- ✅ Arquitectura modular
- ✅ Sistema de backup y métricas
- ✅ 3 imágenes de navegación capturadas

### Siguiente: Computer Vision Real 🔄
1. Ejecutar `test_navegacion_real.py`
2. Si exitoso: Capturar imágenes de formulario
3. Si falla: Ajustar imágenes o confidence

### Futuro: Producción 📋
1. Desactivar modo simulación (`simulation_mode: False`)
2. Capturar todas las imágenes necesarias
3. Probar con órdenes reales
4. Monitorear métricas

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| SYS001 | Error de validación del sistema |
| WIN001 | Error activando ventana |
| WIN002 | Error maximizando ventana |
| WIN003 | SAP no detectado |
| FILE001 | Archivo no encontrado |
| FILE002 | Error validando JSON |
| FILE003 | Error procesando JSON |

---

## Estado del Proyecto

**Versión:** 2.0.1
**Puntuación:** 8.5/10 ⭐
**Estado:** Listo para prueba de Computer Vision

---

## Changelog

### 2.0.1 (2025-10-01)
- Reestructuración completa
- Limpieza de legacy (20MB → 4.8MB)
- Documentación consolidada
- venv en raíz del proyecto

### 2.0.0 (2024-01-15)
- Arquitectura modular
- Sistema de retry automático
- Backup automático
- Métricas de rendimiento

---

## Licencia

Proyecto privado - OrderLoader System © 2024-2025
