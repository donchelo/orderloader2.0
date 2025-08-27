#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del Estado Actual de SAP - OrderLoader 2.0
Verifica qué elementos están visibles en SAP actualmente
"""

import sys
import time
import pyautogui
from pathlib import Path

# Importar módulos del sistema
try:
    from src.core.remote_desktop_manager import RemoteDesktopManager
    from src.core.image_recognition import ImageRecognition
    from src.config import MESSAGES
    from src.utils.logger import setup_logging
except ImportError as e:
    print(f"Error: No se pudo importar módulos del sistema: {e}")
    sys.exit(1)

def test_sap_current_state():
    """Test del estado actual de SAP"""
    
    print("=" * 60)
    print("🔍 TEST DEL ESTADO ACTUAL DE SAP")
    print("=" * 60)
    
    # Configurar logging
    logger = setup_logging()
    
    # Crear instancias
    remote_manager = RemoteDesktopManager()
    image_recognition = ImageRecognition()
    
    print("\n📋 ELEMENTOS A VERIFICAR:")
    print("1. 🔍 Activar ventana del escritorio remoto")
    print("2. 📱 Maximizar ventana")
    print("3. 🔍 Verificar qué elementos de SAP están visibles")
    print("4. 🔍 Buscar elementos de navegación")
    print("5. 🔍 Identificar el estado actual de SAP")
    
    print("\n" + "=" * 60)
    
    # Paso 1: Activar ventana del escritorio remoto
    print("📍 PASO 1: Activando ventana del escritorio remoto...")
    window_info = remote_manager.find_remote_desktop_window()
    
    if not window_info:
        print("❌ ERROR: No se encontró la ventana del escritorio remoto")
        return False
    
    print(f"✅ Ventana encontrada: {window_info.get('MainWindowTitle', 'N/A')}")
    
    if not remote_manager.activate_window_advanced(window_info):
        print("❌ ERROR: No se pudo activar la ventana")
        return False
    
    print("✅ Ventana activada correctamente")
    
    # Paso 2: Maximizar ventana
    print("\n📍 PASO 2: Maximizando ventana...")
    if not remote_manager.maximize_window_advanced():
        print("⚠️ ADVERTENCIA: No se pudo maximizar")
    else:
        print("✅ Ventana maximizada")
    
    # Pausa para estabilizar
    print("⏳ Esperando 3 segundos para estabilizar...")
    time.sleep(3)
    
    # Paso 3: Verificar elementos visibles de SAP
    print("\n📍 PASO 3: Verificando elementos visibles de SAP...")
    
    sap_elements = [
        "core/sap_desktop.png",
        "sap/sap_icon.png",
        "sap/sap_main_interface.png",
        "sap/sap_modulos_menu_button.png",
        "sap/sap_ventas_menu_button.png",
        "sap/sap_archivo_menu_button.png"
    ]
    
    found_elements = []
    for element in sap_elements:
        print(f"   🔍 Verificando: {element}")
        if image_recognition.find_image_robust(element, [0.7, 0.6, 0.5]):
            print(f"   ✅ Encontrado: {element}")
            found_elements.append(element)
        else:
            print(f"   ❌ No encontrado: {element}")
    
    # Paso 4: Buscar elementos de navegación
    print("\n📍 PASO 4: Buscando elementos de navegación...")
    
    navigation_elements = [
        "sap/sap_modulos_menu.png",
        "sap/sap_ventas_order_menu.png",
        "sap/sap_ventas_clientes_menu.png",
        "sap/sap_ventas_order_button.png"
    ]
    
    found_navigation = []
    for element in navigation_elements:
        print(f"   🔍 Verificando navegación: {element}")
        if image_recognition.find_image_robust(element, [0.7, 0.6, 0.5]):
            print(f"   ✅ Encontrado: {element}")
            found_navigation.append(element)
        else:
            print(f"   ❌ No encontrado: {element}")
    
    # Paso 5: Identificar el estado actual
    print("\n📍 PASO 5: Identificando el estado actual de SAP...")
    
    if found_elements:
        print("✅ SAP está visible y funcionando")
        print(f"   Elementos encontrados: {len(found_elements)}")
        for element in found_elements:
            print(f"   - {element}")
    else:
        print("❌ SAP no está visible o no se puede detectar")
    
    if found_navigation:
        print("✅ Elementos de navegación disponibles")
        print(f"   Elementos de navegación: {len(found_navigation)}")
        for element in found_navigation:
            print(f"   - {element}")
    else:
        print("❌ No se encontraron elementos de navegación")
        print("💡 Posible problema: SAP no está en el estado correcto para navegación")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL ESTADO DE SAP")
    print("=" * 60)
    
    if found_elements and found_navigation:
        print("✅ SAP está funcionando correctamente")
        print("✅ Elementos de navegación disponibles")
        print("✅ El sistema puede proceder con la automatización")
        return True
    elif found_elements and not found_navigation:
        print("⚠️ SAP está visible pero no en estado de navegación")
        print("💡 Necesitamos navegar manualmente o usar diferentes comandos")
        return False
    else:
        print("❌ SAP no está funcionando correctamente")
        print("💡 Verifica que SAP esté iniciado y visible")
        return False

def main():
    """Función principal"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🔍 TEST DEL ESTADO ACTUAL DE SAP")
    print("=" * 60)
    print("Este test verifica qué elementos de SAP están")
    print("actualmente visibles en la pantalla")
    
    # Confirmar inicio
    input("\nPresiona Enter para verificar el estado actual de SAP...")
    print()
    
    # Ejecutar test
    success = test_sap_current_state()
    
    if success:
        print("\n🎯 RESULTADO: SAP FUNCIONANDO")
        print("SAP está en estado correcto para automatización")
    else:
        print("\n❌ RESULTADO: SAP NO LISTO")
        print("SAP necesita estar en un estado diferente")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
