# 📸 Imágenes de Referencia para SAP Automation

Este directorio contiene las imágenes de referencia que `SAPAutomation` utiliza para detectar elementos en pantalla.

## 📁 Estructura de Directorios

```
sap/
├── navegacion/          # Imágenes de menús y navegación
├── formulario/          # Imágenes de campos del formulario
├── items/               # Imágenes de la sección de items
├── acciones/            # Imágenes de botones de acción
└── README.md            # Este archivo
```

## 🎯 Imágenes Requeridas

### **navegacion/** - Elementos de Navegación
- `menu_modulos.png` - Botón menú "Módulos"
- `menu_ventas.png` - Opción "Ventas" en el menú
- `boton_orden_venta.png` - Botón "Orden de Venta"

### **formulario/** - Campos del Formulario
- `campo_cliente.png` - Campo de NIT/Cliente
- `campo_fecha_documento.png` - Campo fecha de documento
- `campo_fecha_entrega.png` - Campo fecha de entrega
- `boton_buscar_cliente.png` - Botón de búsqueda (lupa)

### **items/** - Sección de Items
- `campo_codigo.png` - Campo código de artículo
- `campo_cantidad.png` - Campo cantidad
- `campo_precio.png` - Campo precio unitario
- `boton_agregar.png` - Botón agregar item

### **acciones/** - Botones de Acción
- `boton_guardar.png` - Botón Guardar/Actualizar
- `boton_agregar_y_cerrar.png` - Botón Agregar y Cerrar
- `confirmacion_exito.png` - Mensaje de confirmación exitosa

## 📝 Notas Importantes

1. **Formato**: Las imágenes deben ser PNG
2. **Tamaño**: Capturar solo el elemento específico (no toda la pantalla)
3. **Claridad**: Las imágenes deben ser nítidas y con buen contraste
4. **Contexto**: Incluir un poco de contexto alrededor del elemento

## 🔧 Cómo Capturar Imágenes

Ver la guía completa en: `CAPTURA_IMAGENES.md`

## ⚙️ Configuración

El nivel de confianza de detección se configura en `config.py`:
```python
SAP_AUTOMATION_CONFIG = {
    'confidence': 0.8,  # Ajustar si hay problemas de detección
    ...
}
```

## 🎭 Modo Simulación

Mientras no tengas todas las imágenes, el sistema funciona en **modo simulación**.
Para activar modo real, edita `config.py`:
```python
SAP_AUTOMATION_CONFIG = {
    'simulation_mode': False,  # Cambiar a False
    ...
}
```
