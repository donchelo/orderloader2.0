#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para las mejoras del escritorio remoto en OrderLoader 2.0
"""

import sys
import time
import logging
from pathlib import Path

# Importar la clase mejorada
try:
    from main import SAPAutomation, RemoteDesktopManager
    from config import REMOTE_DESKTOP_CONFIG, ACTIVATION_STRATEGIES, MESSAGES
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_remote_desktop.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_remote_desktop_manager():
    """Prueba el gestor de escritorio remoto"""
    print("=" * 60)
    print("PRUEBA DEL GESTOR DE ESCRITORIO REMOTO")
    print("=" * 60)
    
    manager = RemoteDesktopManager()
    
    # Prueba 1: Buscar ventana
    print("\n🔍 Prueba 1: Búsqueda de ventana del escritorio remoto")
    window_info = manager.find_remote_desktop_window()
    
    if window_info:
        print(f"✅ Ventana encontrada:")
        print(f"   Título: {window_info.get('MainWindowTitle', 'N/A')}")
        print(f"   Proceso: {window_info.get('ProcessName', 'N/A')}")
        print(f"   ID: {window_info.get('Id', 'N/A')}")
        
        # Prueba 2: Obtener ventana activa
        print("\n🔍 Prueba 2: Obtener ventana activa actual")
        active_title = manager.get_active_window_title()
        print(f"Ventana activa actual: {active_title}")
        
        # Prueba 3: Activar ventana
        print("\n🔍 Prueba 3: Activación de ventana")
        print("¿Deseas intentar activar la ventana del escritorio remoto? (s/n): ", end="")
        response = input().lower().strip()
        
        if response == 's':
            success = manager.activate_window_advanced(window_info)
            if success:
                print("✅ Ventana activada exitosamente")
                
                # Prueba 4: Maximizar ventana
                print("\n🔍 Prueba 4: Maximización de ventana")
                maximize_success = manager.maximize_window_advanced()
                if maximize_success:
                    print("✅ Ventana maximizada exitosamente")
                else:
                    print("⚠️ No se pudo maximizar la ventana")
            else:
                print("❌ No se pudo activar la ventana")
        else:
            print("Prueba de activación omitida")
    else:
        print("❌ No se encontró ventana del escritorio remoto")
        print("Asegúrate de que el escritorio remoto esté abierto")

def test_sap_automation():
    """Prueba la automatización completa de SAP"""
    print("\n" + "=" * 60)
    print("PRUEBA DE AUTOMATIZACIÓN COMPLETA DE SAP")
    print("=" * 60)
    
    automation = SAPAutomation()
    
    # Verificar imágenes de referencia
    print("\n🔍 Verificando imágenes de referencia...")
    missing_images = []
    for image in ["remote_desktop.png", "sap_desktop.png"]:
        if not (automation.reference_path / image).exists():
            missing_images.append(image)
    
    if missing_images:
        print(f"❌ Faltan imágenes: {missing_images}")
        return False
    
    print("✅ Todas las imágenes de referencia están disponibles")
    
    # Prueba de conexión al escritorio remoto
    print("\n🔍 Prueba de conexión al escritorio remoto...")
    print("¿Deseas ejecutar la prueba completa de conexión? (s/n): ", end="")
    response = input().lower().strip()
    
    if response == 's':
        success = automation.get_remote_desktop()
        if success:
            print("✅ Conexión al escritorio remoto exitosa")
            
            # Prueba de verificación visual
            print("\n🔍 Prueba de verificación visual...")
            visual_success = automation.verify_remote_desktop_visual()
            if visual_success:
                print("✅ Verificación visual exitosa")
            else:
                print("⚠️ Verificación visual falló")
            
            return True
        else:
            print("❌ Conexión al escritorio remoto falló")
            return False
    else:
        print("Prueba de conexión omitida")
        return False

def test_configuration():
    """Prueba la configuración del sistema"""
    print("\n" + "=" * 60)
    print("PRUEBA DE CONFIGURACIÓN")
    print("=" * 60)
    
    print("Configuración del escritorio remoto:")
    for key, value in REMOTE_DESKTOP_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\nEstrategias de activación:")
    for key, value in ACTIVATION_STRATEGIES.items():
        print(f"  {key}: {value}")
    
    print("\nMensajes del sistema:")
    for key, value in MESSAGES.items():
        if key in ['remote_desktop_success', 'remote_desktop_error']:
            print(f"  {key}: {value}")

def main():
    """Función principal de prueba"""
    print(MESSAGES['welcome'])
    
    print("\nEste script probará las mejoras implementadas en el manejo")
    print("del escritorio remoto para OrderLoader 2.0")
    
    print("\nPresiona Enter para comenzar las pruebas...")
    input()
    
    try:
        # Ejecutar pruebas
        test_configuration()
        test_remote_desktop_manager()
        test_sap_automation()
        
        print("\n" + "=" * 60)
        print("PRUEBAS COMPLETADAS")
        print("=" * 60)
        print("\nRevisa los logs en 'test_remote_desktop.log' para más detalles")
        
    except KeyboardInterrupt:
        print("\n\n❌ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante las pruebas: {e}")
        logger.error(f"Error en pruebas: {e}", exc_info=True)
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
