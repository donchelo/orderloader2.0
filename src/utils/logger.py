#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de Logging - OrderLoader 2.0
"""

import logging
from pathlib import Path

from ..config import LOGGING_CONFIG

def setup_logging(log_file: str = None) -> logging.Logger:
    """
    Configura el sistema de logging
    
    Args:
        log_file: Archivo de log personalizado
        
    Returns:
        Logger configurado
    """
    log_file = log_file or LOGGING_CONFIG['file']
    
    # Crear directorio de logs si no existe
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG['level']),
        format=LOGGING_CONFIG['format'],
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def get_logger(name: str = None) -> logging.Logger:
    """
    Obtiene un logger configurado
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name or __name__)
