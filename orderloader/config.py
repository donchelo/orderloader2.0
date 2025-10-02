#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración Simple - OrderLoader
Solo lo esencial
"""

from pathlib import Path

# Rutas principales
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data"
PENDING_PATH = DATA_PATH / "pending"
COMPLETED_PATH = DATA_PATH / "completed"
LOGS_PATH = PROJECT_ROOT / "logs"

# Configuración de Chrome/SAP
ALT_TAB_DELAY = 1.0  # Tiempo de espera después de Alt+Tab
CHROME_STABILIZATION_WAIT = 3  # Tiempo de estabilización para Chrome
CHROME_KEYWORDS = ["chrome", "google chrome", "autosky", "sap business one"]
SAP_APP_KEYWORDS = ["auto.sky", "web access", "sap business one"]

# Configuración simple
PAUSE_BETWEEN_ACTIONS = 0.5
MAX_ALT_TAB_ATTEMPTS = 10
ALT_TAB_DELAY = 0.3
STABILIZATION_WAIT = 3
FILE_PROCESSING_WAIT = 2

# Configuración de pyautogui
PYAUTOGUI_PAUSE = 0.5
PYAUTOGUI_FAILSAFE = True

# Configuración de timeouts y delays
WINDOW_ACTIVATION_DELAY = 1.0
WINDOW_MAXIMIZE_DELAY = 1.0
SAP_VERIFICATION_DELAY = 1.0
FILE_PROCESSING_SIMULATION_DELAY = 2.0
SYSTEM_STABILIZATION_DELAY = 3.0

# Configuración de PowerShell
POWERSHELL_TIMEOUT = 5

# Configuración de archivos
SUPPORTED_EXTENSIONS = ['.json']
FILE_ENCODING = 'utf-8'

# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_ENCODING = 'utf-8'

# Configuración de retry logic
RETRY_CONFIG = {
    'max_attempts': 3,
    'base_delay': 1.0,  # segundos
    'max_delay': 10.0,  # segundos
    'backoff_multiplier': 2.0,
    'retryable_errors': [
        'WINDOW_ACTIVATION_FAILED',
        'WINDOW_MAXIMIZE_FAILED', 
        'SAP_NOT_DETECTED',
        'POWERSHELL_TIMEOUT',
        'SUBPROCESS_FAILED'
    ]
}

# Configuración de backup
BACKUP_CONFIG = {
    'enabled': True,
    'backup_path': 'backups',
    'max_backups': 10,
    'compress_backups': True
}

# Configuración de métricas
METRICS_CONFIG = {
    'enabled': True,
    'track_performance': True,
    'track_success_rate': True,
    'metrics_file': 'metrics.json'
}

# Configuración de automatización SAP
SAP_AUTOMATION_CONFIG = {
    'simulation_mode': True,  # True = simular, False = automatización real
    'confidence': 0.8,  # Nivel de confianza para detección de imágenes (0.0 - 1.0)
    'search_timeout': 10,  # Timeout de búsqueda de imágenes en segundos
    'type_interval': 0.05,  # Intervalo entre teclas al escribir
    'action_delay': 0.5,  # Delay entre acciones en segundos
}

# Códigos de error específicos
class ErrorCodes:
    """Códigos de error específicos del sistema"""
    # Errores de sistema
    SYSTEM_VALIDATION_FAILED = "SYS001"
    PERMISSION_DENIED = "SYS002"
    DIRECTORY_CREATION_FAILED = "SYS003"
    
    # Errores de ventana
    WINDOW_ACTIVATION_FAILED = "WIN001"
    WINDOW_MAXIMIZE_FAILED = "WIN002"
    SAP_NOT_DETECTED = "WIN003"
    
    # Errores de archivos
    FILE_NOT_FOUND = "FILE001"
    JSON_VALIDATION_FAILED = "FILE002"
    JSON_PROCESSING_FAILED = "FILE003"
    FILE_MOVE_FAILED = "FILE004"
    
    # Errores de red/sistema
    POWERSHELL_TIMEOUT = "NET001"
    SUBPROCESS_FAILED = "NET002"