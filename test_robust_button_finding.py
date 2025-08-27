#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Búsqueda Robusta del Botón - OrderLoader 2.0
Usa técnicas robustas para encontrar el botón de órdenes de venta
"""

import sys
import time
import pyautogui
from pathlib import Path

# Importar módulos del sistema
try:
    from src.core.remote_desktop_manager import RemoteDesktopManager
    from src.core.image_recognition import ImageRecognition
    from src.config import MESSAGES, KEYBOARD_SHORTCUTS
    from src.utils.logger import setup_logging
except ImportError as e:
    print(f"Error: No se pudo importar módulos del sistema: {e}")
    sys.exit(1)

def test_robust_button_finding():
    """Test de búsqueda robusta del botón de órdenes de venta"""
    
    print("=" * 60)
    print("🔍 TEST DE BÚSQUEDA ROBUSTA DEL BOTÓN")
    print("=" * 60)
    
    # Configurar logging
    logger = setup_logging()
    
    # Crear instancias
    remote_manager = RemoteDesktopManager()
    image_recognition = ImageRecognition()
    
    print("\n📋 TÉCNICAS A PROBAR:")
    print("1. 🔍 Búsqueda básica del botón")
    print("2. 🎯 Búsqueda robusta con múltiples niveles")
    print("3. 🔧 Template matching con OpenCV")
    print("4. 🔍 Búsqueda de elementos alternativos")
    
    print("\n" + "=" * 60)
    
    # Activar ventana del escritorio remoto
    print("📍 Activando ventana del escritorio remoto...")
    window_info = remote_manager.find_remote_desktop_window()
    
    if not window_info:
        print("❌ ERROR: No se encontró la ventana del escritorio remoto")
        return False
    
    if not remote_manager.activate_window_advanced(window_info):
        print("❌ ERROR: No se pudo activar la ventana")
        return False
    
    print("✅ Ventana activada")
    
    # Maximizar ventana
    if not remote_manager.maximize_window_advanced():
        print("⚠️ ADVERTENCIA: No se pudo maximizar")
    
    time.sleep(2)
    
    # Navegar a SAP (Alt+M, V)
    print("\n📍 Navegando en SAP (Alt+M, V)...")
    try:
        pyautogui.hotkey(*KEYBOARD_SHORTCUTS['open_modules'])
        time.sleep(1)
        pyautogui.press(KEYBOARD_SHORTCUTS['navigate_sales'])
        time.sleep(2)
        print("✅ Navegación completada")
    except Exception as e:
        print(f"❌ ERROR en navegación: {e}")
        return False
    
    # Test 1: Búsqueda básica
    print("\n📍 TEST 1: Búsqueda básica del botón...")
    result = image_recognition.find_image_on_screen("sap/sap_ventas_order_button.png")
    if result:
        print(f"✅ Botón encontrado con búsqueda básica en: {result}")
        return True
    else:
        print("❌ No encontrado con búsqueda básica")
    
    # Test 2: Búsqueda robusta
    print("\n📍 TEST 2: Búsqueda robusta con múltiples niveles...")
    result = image_recognition.find_image_robust("sap/sap_ventas_order_button.png", [0.8, 0.7, 0.6, 0.5, 0.4])
    if result:
        print(f"✅ Botón encontrado con búsqueda robusta en: {result}")
        return True
    else:
        print("❌ No encontrado con búsqueda robusta")
    
    # Test 3: Template matching
    print("\n📍 TEST 3: Template matching con OpenCV...")
    result = image_recognition.find_image_with_template_matching("sap/sap_ventas_order_button.png", threshold=0.6)
    if result:
        print(f"✅ Botón encontrado con template matching en: {result}")
        return True
    else:
        print("❌ No encontrado con template matching")
    
    # Test 4: Buscar elementos alternativos
    print("\n📍 TEST 4: Buscando elementos alternativos...")
    alternative_buttons = [
        "sap/sap_ventas_order_menu.png",
        "sap/sap_ventas_menu_button.png",
        "sap/sap_modulos_menu_button.png"
    ]
    
    for button in alternative_buttons:
        print(f"   🔍 Probando: {button}")
        result = image_recognition.find_image_robust(button, [0.7, 0.6, 0.5])
        if result:
            print(f"   ✅ Elemento encontrado: {button} en {result}")
            return True
        else:
            print(f"   ❌ No encontrado: {button}")
    
    print("\n❌ No se pudo encontrar ningún botón o elemento relacionado")
    return False

def main():
    """Función principal"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🔍 TEST DE BÚSQUEDA ROBUSTA")
    print("=" * 60)
    print("Este test usará técnicas robustas para encontrar")
    print("el botón de órdenes de venta en SAP")
    
    # Confirmar inicio
    input("\nPresiona Enter para iniciar el test de búsqueda robusta...")
    print()
    
    # Ejecutar test
    success = test_robust_button_finding()
    
    if success:
        print("\n🎯 RESULTADO: BOTÓN ENCONTRADO")
        print("Las técnicas robustas funcionan correctamente")
    else:
        print("\n❌ RESULTADO: BOTÓN NO ENCONTRADO")
        print("Posibles causas:")
        print("- La imagen de referencia no coincide con la pantalla actual")
        print("- El botón tiene una apariencia diferente")
        print("- Necesitamos actualizar la imagen de referencia")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
