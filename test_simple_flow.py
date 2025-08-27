#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simplificado - OrderLoader 2.0
Asume que el escritorio remoto ya está abierto y SAP ya está iniciado
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

def test_simple_sap_navigation():
    """Test simplificado de navegación en SAP"""
    
    print("=" * 60)
    print("🚀 TEST SIMPLIFICADO - SAP YA ABIERTO")
    print("=" * 60)
    
    # Configurar logging
    logger = setup_logging()
    
    # Crear instancias
    remote_manager = RemoteDesktopManager()
    image_recognition = ImageRecognition()
    
    print("\n📋 FLUJO SIMPLIFICADO:")
    print("1. 🔍 Activar ventana del escritorio remoto (ya abierta)")
    print("2. 📱 Maximizar ventana")
    print("3. ⌨️ Alt+M (menú de módulos)")
    print("4. ⌨️ V (navegar a ventas)")
    print("5. 🔍 Buscar botón de órdenes de venta")
    print("6. ✅ Verificar formulario de órdenes")
    
    print("\n" + "=" * 60)
    
    # Paso 1: Activar ventana del escritorio remoto
    print("📍 PASO 1: Activando ventana del escritorio remoto...")
    window_info = remote_manager.find_remote_desktop_window()
    
    if not window_info:
        print("❌ ERROR: No se encontró la ventana del escritorio remoto")
        print("   Verifica que esté abierta y conectada a 20.96.6.64")
        return False
    
    print(f"✅ Ventana encontrada: {window_info.get('MainWindowTitle', 'N/A')}")
    
    # Activar la ventana
    if not remote_manager.activate_window_advanced(window_info):
        print("❌ ERROR: No se pudo activar la ventana del escritorio remoto")
        return False
    
    print("✅ Ventana del escritorio remoto activada")
    
    # Paso 2: Maximizar ventana
    print("\n📍 PASO 2: Maximizando ventana...")
    if not remote_manager.maximize_window_advanced():
        print("⚠️ ADVERTENCIA: No se pudo maximizar, pero continuando...")
    else:
        print("✅ Ventana maximizada")
    
    # Pequeña pausa para que se estabilice
    time.sleep(2)
    
    # Paso 3: Alt+M para abrir menú de módulos
    print("\n📍 PASO 3: Abriendo menú de módulos (Alt+M)...")
    try:
        pyautogui.hotkey(*KEYBOARD_SHORTCUTS['open_modules'])
        time.sleep(1)
        print("✅ Alt+M ejecutado")
    except Exception as e:
        print(f"❌ ERROR ejecutando Alt+M: {e}")
        return False
    
    # Paso 4: V para navegar a ventas
    print("\n📍 PASO 4: Navegando a ventas (V)...")
    try:
        pyautogui.press(KEYBOARD_SHORTCUTS['navigate_sales'])
        time.sleep(1)
        print("✅ V ejecutado")
    except Exception as e:
        print(f"❌ ERROR ejecutando V: {e}")
        return False
    
    # Paso 5: Buscar botón de órdenes de venta
    print("\n📍 PASO 5: Buscando botón de órdenes de venta...")
    if image_recognition.click_image("sap/sap_ventas_order_button.png"):
        time.sleep(2)
        print("✅ Botón de órdenes de venta encontrado y clickeado")
    else:
        print("❌ ERROR: No se pudo encontrar el botón de órdenes de venta")
        return False
    
    # Paso 6: Verificar formulario
    print("\n📍 PASO 6: Verificando formulario de orden de venta...")
    if image_recognition.wait_for_image("sap/sap_orden_de_ventas_template.png", timeout=10):
        print("✅ Formulario de orden de venta verificado")
    else:
        print("❌ ERROR: No se pudo verificar el formulario de orden de venta")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡TEST SIMPLIFICADO COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print("✅ Navegación a órdenes de venta completada")
    print("✅ El sistema está listo para procesar órdenes")
    
    return True

def main():
    """Función principal"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🚀 INICIANDO TEST SIMPLIFICADO")
    print("=" * 60)
    print("ASUMIENDO:")
    print("- El escritorio remoto ya está abierto")
    print("- SAP Desktop ya está iniciado")
    print("- Solo necesitamos navegar hasta órdenes de venta")
    
    # Confirmar inicio
    input("\nPresiona Enter para iniciar el test simplificado...")
    print()
    
    # Ejecutar test
    success = test_simple_sap_navigation()
    
    if success:
        print("\n🎯 RESULTADO: TEST EXITOSO")
        print("El sistema puede navegar correctamente en SAP")
    else:
        print("\n❌ RESULTADO: TEST FALLIDO")
        print("Revisa los logs para más detalles")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
