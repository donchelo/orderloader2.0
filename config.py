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

# Configuración de imágenes de referencia
REQUIRED_IMAGES = [
    "remote_desktop.png",
    "sap_desktop.png", 
    "sap_modulos_menu.png",
    "sap_ventas_order_menu.png",
    "sap_ventas_order_button.png",
    "sap_orden_de_ventas_template.png"
]

# Configuración de atajos de teclado
KEYBOARD_SHORTCUTS = {
    'maximize_window': ['win', 'm'],
    'open_modules': ['alt', 'm'],
    'navigate_sales': 'v',
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

# Mensajes del sistema
MESSAGES = {
    'welcome': """
==================================================
OrderLoader 2.0 - Automatización de SAP
==================================================

Este sistema automatizará la navegación en SAP
hasta el formulario de órdenes de venta.

IMPORTANTE:
- Asegúrate de que el escritorio remoto esté abierto y conectado a SAP
- El sistema primero activará la ventana del escritorio remoto
- No muevas el mouse durante la automatización
- Para detener: mueve el mouse a la esquina superior izquierda
""",
    
    'success': "✅ Automatización completada exitosamente",
    'error': "❌ La automatización falló",
    'check_log': "Revisa el archivo 'orderloader.log' para más detalles",
    'ready': "El formulario de orden de venta está listo para uso"
}
