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

# Configuración de conexión
REMOTE_DESKTOP_IP = "20.96.6.64"
REMOTE_DESKTOP_KEYWORDS = ["remoto", "Conexión", "Remote", REMOTE_DESKTOP_IP]

# Configuración simple
PAUSE_BETWEEN_ACTIONS = 0.5
MAX_ALT_TAB_ATTEMPTS = 10
ALT_TAB_DELAY = 0.3
STABILIZATION_WAIT = 3
FILE_PROCESSING_WAIT = 2

# Configuración de archivos
SUPPORTED_EXTENSIONS = ['.json']
FILE_ENCODING = 'utf-8'

# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_ENCODING = 'utf-8'