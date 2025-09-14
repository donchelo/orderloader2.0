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

# Configuración de archivos
SUPPORTED_EXTENSIONS = ['.json']
FILE_ENCODING = 'utf-8'

# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_ENCODING = 'utf-8'