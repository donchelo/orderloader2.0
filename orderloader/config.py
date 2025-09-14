#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración consolidada - OrderLoader Final
Toda la configuración en un solo archivo
"""

from pathlib import Path

# ==================== RUTAS DEL SISTEMA ====================

# Rutas principales
PROJECT_ROOT = Path(__file__).parent
ASSETS_PATH = PROJECT_ROOT / "assets"
DATA_PATH = PROJECT_ROOT / "data"
LOGS_PATH = PROJECT_ROOT / "logs"

# Rutas de imágenes
IMAGES_PATH = ASSETS_PATH / "images"
SAP_IMAGES_PATH = IMAGES_PATH / "sap"

# Rutas de datos
PENDING_PATH = DATA_PATH / "pending"
COMPLETED_PATH = DATA_PATH / "completed"

# ==================== CONFIGURACIÓN DE CONEXIÓN ====================

# Escritorio remoto
REMOTE_DESKTOP_IP = "20.96.6.64"
REMOTE_DESKTOP_TITLE_KEYWORDS = ["remoto", "Conexión", "Remote", REMOTE_DESKTOP_IP]

# ==================== CONFIGURACIÓN DE AUTOMATIZACIÓN ====================

# Reconocimiento de imágenes
IMAGE_RECOGNITION = {
    'confidence': 0.8,
    'timeout': 10,
    'pause_between_actions': 0.5,
    'max_alt_tab_attempts': 10,
    'alt_tab_delay': 0.3,
}

# Tiempos de espera (segundos)
WAIT_TIMES = {
    'after_modules_click': 2,
    'after_sales_click': 2,
    'after_orders_click': 3,
    'window_activation': 1,
    'file_processing': 2,
    'stabilization': 3,
}

# ==================== IMÁGENES REQUERIDAS ====================

REQUIRED_IMAGES = [
    "sap/sap_modulos_menu_button.png",
    "sap/sap_ventas_menu_button.png",
    "sap/sap_ventas_order_button.png",
]

# ==================== CONFIGURACIÓN DE ARCHIVOS ====================

FILE_CONFIG = {
    'supported_extensions': ['.json'],
    'encoding': 'utf-8',
    'max_file_size_mb': 10,
}

# ==================== CONFIGURACIÓN DE LOGGING ====================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'encoding': 'utf-8',
    'max_file_size_mb': 10,
    'backup_count': 5,
}

# ==================== MENSAJES DEL SISTEMA ====================

MESSAGES = {
    'welcome': """
🎯 ORDERLOADER FINAL v4.0.0
Sistema consolidado con mejores prácticas

FUNCIONALIDAD:
1. Conectar al escritorio remoto (20.96.6.64)
2. Navegar en SAP: Módulos → Ventas → Órdenes
3. Procesar archivos JSON de la cola

REQUISITOS:
- Escritorio remoto abierto y conectado a 20.96.6.64
- SAP Desktop iniciado en el escritorio remoto
- Archivos JSON en data/pending/
""",
    
    'success': "🎉 ¡Procesamiento completado exitosamente!",
    'error': "❌ El procesamiento falló",
    'no_files': "📭 No hay archivos pendientes en la cola",
    'check_logs': "Revisa los logs para más detalles",
}
