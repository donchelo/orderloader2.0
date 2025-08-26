#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrderLoader 2.0 - Automatización de SAP para Órdenes de Venta
Autor: Sistema Automatizado
Versión: 2.0
"""

import sys
from pathlib import Path

# Importar módulos de automatización
try:
    import pyautogui
    import cv2
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(f"Error: Faltan dependencias. Ejecuta: pip install pyautogui opencv-python pillow")
    print(f"Error específico: {e}")
    sys.exit(1)

# Importar módulos del sistema
try:
    from src.core.sap_automation import SAPAutomation
    from src.config import MESSAGES, REQUIRED_IMAGES
    from src.utils.logger import setup_logging
except ImportError as e:
    print(f"Error: No se pudo importar módulos del sistema: {e}")
    sys.exit(1)

def main():
    """Función principal"""
    # Configurar logging
    logger = setup_logging()
    
    print(MESSAGES['welcome'])
    
    # Crear instancia de automatización
    automation = SAPAutomation()
    
    # Verificar que las imágenes de referencia existen
    missing_images = automation.verify_required_images()
    
    if missing_images:
        print("Error: Faltan las siguientes imágenes de referencia:")
        for image in missing_images:
            print(f"  - {image}")
        print("\nAsegúrate de que todas las imágenes estén en la carpeta 'assets/images'")
        return
    
    print("Imágenes de referencia verificadas correctamente")
    print()
    
    # Mostrar estado de colas
    automation.queue_manager.print_queue_status()
    
    # Confirmar inicio
    input("Presiona Enter para iniciar el procesamiento de la cola...")
    print()
    
    # Procesar cola completa
    success = automation.process_queue()
    
    if success:
        print(f"\n{MESSAGES['success']}")
        print("🎉 Procesamiento de cola completado")
    else:
        print(f"\n{MESSAGES['error']}")
        print(MESSAGES['check_log'])
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
