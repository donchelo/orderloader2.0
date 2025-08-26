# OrderLoader 2.0

Sistema de automatización para SAP que permite navegar automáticamente desde el escritorio remoto ya abierto hasta el formulario de órdenes de venta en SAP.

## Características

- ✅ Automatización completa del proceso de apertura de SAP
- ✅ Navegación automática a órdenes de venta
- ✅ Reconocimiento de imágenes para mayor precisión
- ✅ Sistema de logging para seguimiento de errores
- ✅ Interfaz simple con launcher .bat

## Requisitos

- Python 3.7 o superior
- Windows 10/11
- Escritorio remoto abierto y conectado a SAP
- SAP instalado y configurado

## Instalación

1. **Instalar Python** (si no está instalado):
   - Descargar desde [python.org](https://www.python.org/downloads/)
   - Asegurarse de marcar "Add Python to PATH" durante la instalación

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar imágenes de referencia**:
   - Asegurarse de que todas las imágenes estén en la carpeta `reference_images/`
   - Las imágenes deben ser capturas de pantalla precisas de los elementos de SAP
   - Asegurarse de que el escritorio remoto esté abierto y conectado a SAP

## Uso

### Método 1: Usando el launcher (.bat)
1. Hacer doble clic en `launcher.bat`
2. El sistema verificará las dependencias
3. Presionar Enter para iniciar la automatización

### Método 2: Directo con Python
```bash
python main.py
```

## Proceso de Automatización

El sistema ejecuta los siguientes pasos en orden:

1. **Activar Escritorio Remoto**: Busca y activa la ventana del escritorio remoto ya abierto
2. **Verificar SAP Desktop**: Confirma que estamos en la interfaz de SAP
3. **Maximizar Ventana**: Usa Windows + M para maximizar
4. **Abrir Módulos**: Presiona Alt + M para abrir el menú de módulos
5. **Navegar a Ventas**: Presiona V para ir a la sección de ventas
6. **Abrir Orden de Venta**: Busca y hace clic en el botón de orden de venta
7. **Verificar Formulario**: Confirma que el formulario se abrió correctamente

## Imágenes de Referencia Requeridas

El sistema necesita las siguientes imágenes en la carpeta `reference_images/`:

- `remote_desktop.png` - Ventana del escritorio remoto
- `sap_desktop.png` - Interfaz principal de SAP
- `sap_modulos_menu.png` - Menú de módulos abierto
- `sap_ventas_order_menu.png` - Menú de ventas
- `sap_ventas_order_button.png` - Botón de orden de venta
- `sap_orden_de_ventas_template.png` - Formulario de orden de venta

## Configuración

### Ajustar sensibilidad de reconocimiento
En `main.py`, línea 35, puedes modificar:
```python
self.confidence = 0.8  # Valor entre 0.0 y 1.0
```

### Ajustar timeouts
En `main.py`, línea 36:
```python
self.timeout = 10  # Segundos de espera
```

## Solución de Problemas

### Error: "Faltan dependencias"
```bash
pip install pyautogui opencv-python pillow
```

### Error: "Imagen no encontrada"
- Verificar que las imágenes de referencia existen
- Asegurarse de que las capturas de pantalla son recientes
- Ajustar el nivel de confianza si es necesario

### Error: "SAP Desktop no detectado"
- Verificar que SAP esté abierto
- Asegurarse de que la resolución de pantalla coincida con las imágenes de referencia

## Logs

El sistema genera logs en `orderloader.log` con información detallada sobre:
- Progreso de la automatización
- Errores encontrados
- Tiempos de ejecución

## Seguridad

- El sistema incluye `pyautogui.FAILSAFE = True`
- Mover el mouse a la esquina superior izquierda detendrá la automatización
- Presionar Ctrl+C también detendrá el proceso

## Soporte

Para reportar problemas o solicitar mejoras:
1. Revisar el archivo `orderloader.log`
2. Verificar que todas las imágenes de referencia estén presentes
3. Confirmar que SAP esté en el estado esperado

## Versión

OrderLoader 2.0 - Desarrollado para automatización de SAP
