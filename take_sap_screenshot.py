#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para tomar capturas de pantalla de SAP
OrderLoader 2.0
"""

import sys
import os
import logging
from datetime import datetime

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.screenshot_manager import ScreenshotManager
from src.utils.logger import setup_logging

def main():
    """Función principal del script"""
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("=" * 60)
    print("📸 CAPTURADOR DE PANTALLA DE SAP - OrderLoader 2.0")
    print("=" * 60)
    print()
    
    try:
        # Crear instancia del gestor de capturas
        screenshot_manager = ScreenshotManager()
        
        print("🔄 Iniciando proceso de captura...")
        print("📋 Pasos que se realizarán:")
        print("   1. Buscar ventana del escritorio remoto")
        print("   2. Activar con Alt+Tab")
        print("   3. Maximizar la ventana")
        print("   4. Tomar captura de pantalla")
        print("   5. Guardar en assets/screenshots/")
        print()
        
        # Tomar la captura
        filepath = screenshot_manager.take_sap_screenshot()
        
        if filepath:
            print("✅ ¡Captura completada exitosamente!")
            print(f"📁 Archivo guardado: {filepath}")
            print()
            print("💡 Consejos:")
            print("   - Las capturas se guardan en 'assets/screenshots/'")
            print("   - Puedes usar este script para documentar el estado de SAP")
            print("   - Para múltiples capturas, modifica el script")
        else:
            print("❌ Error al tomar la captura de pantalla")
            print("🔍 Revisa el archivo 'orderloader.log' para más detalles")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido por el usuario")
        return 1
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        print(f"❌ Error inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
