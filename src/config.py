#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de OrderLoader 2.0
"""

# Configuración de reconocimiento de imágenes
RECOGNITION_CONFIG = {
    'confidence': 0.8,  # Nivel de confianza para reconocimiento (0.0 - 1.0)
    'timeout': 10,      # Tiempo máximo de espera en segundos
    'pause': 0.5,       # Pausa entre acciones
}

# Configuración específica del escritorio remoto
REMOTE_DESKTOP_CONFIG = {
    'window_title': "20.96.6.64 - Conexión a Escritorio remoto",
    'ip_address': "20.96.6.64",
    'max_attempts': 3,
    'retry_delay': 5,
    'activation_timeout': 10,
    'maximization_timeout': 3,
    'visual_verification_timeout': 5,
}

# Configuración de estrategias de activación
ACTIVATION_STRATEGIES = {
    'alt_tab_attempts': 10,
    'alt_tab_delay': 0.3,
    'powershell_timeout': 2,
    'win_tab_delay': 1,
    'click_delay': 0.5,
    'new_connection_timeout': 3,
}

# Configuración de imágenes de referencia
REQUIRED_IMAGES = [
    "core/remote_desktop.png",
    "core/sap_desktop.png", 
    "sap/sap_modulos_menu.png",
    "sap/sap_ventas_order_menu.png",
    "sap/sap_ventas_order_button.png",
    "sap/sap_orden_de_ventas_template.png"
]

# Configuración de atajos de teclado
KEYBOARD_SHORTCUTS = {
    'maximize_window': ['win', 'up'],
    'maximize_alt_space': ['alt', 'space'],
    'maximize_x': 'x',
    'open_modules': ['alt', 'm'],
    'navigate_sales': 'v',
    'alt_tab': ['alt', 'tab'],
    'win_tab': ['win', 'tab'],
}

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'orderloader.log'
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'failsafe': True,  # Activar failsafe de pyautogui
    'pause_between_actions': 0.5,
}

# Configuración de recuperación de errores
ERROR_RECOVERY_CONFIG = {
    'max_retries': 3,
    'retry_delay': 5,
    'exponential_backoff': True,
    'backoff_multiplier': 2,
}

# Configuración de colas
QUEUE_CONFIG = {
    'supported_formats': ['.pdf', '.png', '.jpg', '.jpeg', '.txt'],
    'auto_process': True,  # Procesar automáticamente al iniciar
    'show_status': True,   # Mostrar estado de colas
}

# Mensajes del sistema
MESSAGES = {
    'welcome': """
==================================================
OrderLoader 2.0 - Automatización de SAP para Órdenes de Venta
==================================================

Este sistema automatizará la navegación en SAP
hasta el formulario de órdenes de venta.

SISTEMA DE COLAS:
- Coloca archivos en 'queues/pending/' para procesamiento
- Los archivos se procesan en orden FIFO (primero en llegar, primero en procesar)
- Los archivos procesados se mueven a 'queues/completed/'

IMPORTANTE:
- Asegúrate de que el escritorio remoto esté abierto y conectado a SAP
- El sistema procesará automáticamente todos los archivos en la cola
- No muevas el mouse durante la automatización
- Para detener: mueve el mouse a la esquina superior izquierda

MEJORAS EN ESTA VERSIÓN:
- Sistema de colas simple y eficiente
- Procesamiento secuencial automático
- Múltiples estrategias de activación del escritorio remoto
- Sistema de recuperación automática de errores
- Verificación visual mejorada
- Logs detallados para debugging
- Enfoque especializado en módulo de ventas
""",
    
    'success': "✅ Procesamiento completado exitosamente",
    'error': "❌ El procesamiento falló",
    'check_log': "Revisa el archivo 'orderloader.log' para más detalles",
    'ready': "El formulario de orden de venta está listo para uso",
    'remote_desktop_success': "✅ Escritorio remoto activado correctamente",
    'remote_desktop_error': "❌ Error al activar el escritorio remoto",
}
