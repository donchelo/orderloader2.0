# Sistema de Colas - OrderLoader 2.0

## 📁 Estructura de Carpetas

```
queues/
├── pending/           # Archivos sin procesar (FIFO)
│   └── .gitkeep
└── completed/         # Archivos procesados exitosamente
    └── .gitkeep
```

## 🎯 Cómo Usar

### 1. **Preparar Archivos**
- Coloca los archivos a procesar en `queues/pending/`
- Los archivos se procesarán en orden de llegada (FIFO)
- Formatos soportados: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.txt`

### 2. **Ejecutar Sistema**
```bash
python main.py
```

### 3. **Procesamiento Automático**
- El sistema detectará automáticamente archivos en `pending/`
- Procesará cada archivo secuencialmente
- Moverá archivos completados a `completed/`
- Mostrará progreso en tiempo real

### 4. **Resultado**
- Archivos procesados: `queues/completed/`
- Logs detallados: `orderloader.log`
- Estado de colas mostrado al inicio y fin

## 📊 Flujo de Procesamiento

```
📁 pending/ → 🔄 Procesamiento → 📁 completed/ ✅
```

## ⚠️ Notas Importantes

- **Orden FIFO**: Los archivos se procesan en orden de llegada
- **Archivos Fallidos**: Si un archivo falla, permanece en `pending/` para revisión manual
- **Nombres Únicos**: Los archivos en `completed/` se renombran automáticamente si hay conflictos
- **Logs**: Cada operación se registra en `orderloader.log`

## 🔧 Configuración

El sistema está configurado en `src/config.py`:

```python
QUEUE_CONFIG = {
    'supported_formats': ['.pdf', '.png', '.jpg', '.jpeg', '.txt'],
    'auto_process': True,  # Procesar automáticamente al iniciar
    'show_status': True,   # Mostrar estado de colas
}
```
