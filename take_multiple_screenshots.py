#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para tomar múltiples capturas de pantalla de SAP
OrderLoader 2.0
"""

import sys
import os
import logging
import argparse
from datetime import datetime

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.screenshot_manager import ScreenshotManager
from src.utils.logger import setup_logging

def main():
    """Función principal del script"""
    
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Toma múltiples capturas de pantalla de SAP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python take_multiple_screenshots.py                    # 3 capturas por defecto
  python take_multiple_screenshots.py -c 5              # 5 capturas
  python take_multiple_screenshots.py -c 10 -d 5        # 10 capturas con 5 segundos de delay
  python take_multiple_screenshots.py --count 1         # Solo 1 captura
        """
    )
    
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=3,
        help='Número de capturas a tomar (por defecto: 3)'
    )
    
    parser.add_argument(
        '-d', '--delay',
        type=float,
        default=2.0,
        help='Delay en segundos entre capturas (por defecto: 2.0)'
    )
    
    parser.add_argument(
        '--single',
        action='store_true',
        help='Tomar solo una captura (ignora --count)'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("=" * 60)
    print("📸 CAPTURADOR MÚLTIPLE DE PANTALLA DE SAP - OrderLoader 2.0")
    print("=" * 60)
    print()
    
    try:
        # Crear instancia del gestor de capturas
        screenshot_manager = ScreenshotManager()
        
        if args.single:
            print("📸 Tomando una sola captura de pantalla...")
            print()
            
            filepath = screenshot_manager.take_sap_screenshot()
            
            if filepath:
                print("✅ ¡Captura completada exitosamente!")
                print(f"📁 Archivo guardado: {filepath}")
            else:
                print("❌ Error al tomar la captura de pantalla")
                return 1
        else:
            print(f"📸 Tomando {args.count} capturas de pantalla...")
            print(f"⏱️ Delay entre capturas: {args.delay} segundos")
            print()
            print("📋 Proceso:")
            print("   1. Buscar y activar escritorio remoto")
            print("   2. Maximizar ventana")
            print(f"   3. Tomar {args.count} capturas con {args.delay}s de delay")
            print("   4. Guardar en assets/screenshots/")
            print()
            
            # Tomar múltiples capturas
            saved_files = screenshot_manager.take_multiple_screenshots(
                count=args.count,
                delay=args.delay
            )
            
            if saved_files:
                print("✅ ¡Proceso completado exitosamente!")
                print(f"📁 Archivos guardados ({len(saved_files)}/{args.count}):")
                for i, filepath in enumerate(saved_files, 1):
                    print(f"   {i}. {filepath}")
            else:
                print("❌ No se pudo tomar ninguna captura")
                return 1
        
        print()
        print("💡 Consejos:")
        print("   - Las capturas se guardan en 'assets/screenshots/'")
        print("   - Usa --single para una sola captura rápida")
        print("   - Ajusta el delay con -d si necesitas más tiempo entre capturas")
        print("   - Para detener: Ctrl+C")
            
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
