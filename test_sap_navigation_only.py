#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Navegación SAP - OrderLoader 2.0
Se enfoca específicamente en la navegación de SAP paso a paso
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

def test_sap_navigation_step_by_step():
    """Test paso a paso de la navegación en SAP"""
    
    print("=" * 60)
    print("🧭 TEST DE NAVEGACIÓN SAP - PASO A PASO")
    print("=" * 60)
    
    # Configurar logging
    logger = setup_logging()
    
    # Crear instancias
    remote_manager = RemoteDesktopManager()
    image_recognition = ImageRecognition()
    
    print("\n📋 NAVEGACIÓN PASO A PASO:")
    print("1. 🔍 Activar ventana del escritorio remoto")
    print("2. 📱 Maximizar ventana")
    print("3. ⌨️ Alt+M (abrir menú de módulos)")
    print("4. 🔍 Verificar que se abrió el menú")
    print("5. ⌨️ V (navegar a ventas)")
    print("6. 🔍 Verificar que estamos en ventas")
    print("7. 🔍 Buscar botón de órdenes")
    
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
    
    # Paso 3: Alt+M para abrir menú de módulos
    print("\n📍 PASO 3: Ejecutando Alt+M (abrir menú de módulos)...")
    try:
        print("   ⌨️ Presionando Alt+M...")
        pyautogui.hotkey(*KEYBOARD_SHORTCUTS['open_modules'])
        print("   ✅ Alt+M ejecutado")
        
        # Pausa para que aparezca el menú
        print("   ⏳ Esperando 2 segundos para que aparezca el menú...")
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ ERROR ejecutando Alt+M: {e}")
        return False
    
    # Paso 4: Verificar que se abrió el menú de módulos
    print("\n📍 PASO 4: Verificando que se abrió el menú de módulos...")
    if image_recognition.find_image_on_screen("sap/sap_modulos_menu.png"):
        print("   ✅ Menú de módulos detectado")
    else:
        print("   ⚠️ Menú de módulos no detectado, pero continuando...")
        print("   🔍 Probando con búsqueda robusta...")
        if image_recognition.find_image_robust("sap/sap_modulos_menu.png", [0.7, 0.6, 0.5]):
            print("   ✅ Menú de módulos detectado con búsqueda robusta")
        else:
            print("   ❌ Menú de módulos no detectado")
            print("   💡 Posible problema: Alt+M no funcionó correctamente")
    
    # Paso 5: V para navegar a ventas
    print("\n📍 PASO 5: Ejecutando V (navegar a ventas)...")
    try:
        print("   ⌨️ Presionando V...")
        pyautogui.press(KEYBOARD_SHORTCUTS['navigate_sales'])
        print("   ✅ V ejecutado")
        
        # Pausa para que aparezca el menú de ventas
        print("   ⏳ Esperando 2 segundos para que aparezca el menú de ventas...")
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ ERROR ejecutando V: {e}")
        return False
    
    # Paso 6: Verificar que estamos en ventas
    print("\n📍 PASO 6: Verificando que estamos en el menú de ventas...")
    if image_recognition.find_image_on_screen("sap/sap_ventas_order_menu.png"):
        print("   ✅ Menú de ventas detectado")
    else:
        print("   ⚠️ Menú de ventas no detectado, probando alternativas...")
        
        # Probar otros elementos de ventas
        ventas_elements = [
            "sap/sap_ventas_clientes_menu.png",
            "sap/sap_ventas_menu_button.png"
        ]
        
        found = False
        for element in ventas_elements:
            if image_recognition.find_image_robust(element, [0.7, 0.6]):
                print(f"   ✅ Elemento de ventas detectado: {element}")
                found = True
                break
        
        if not found:
            print("   ❌ No se detectó ningún elemento de ventas")
            print("   💡 Posible problema: V no funcionó correctamente")
    
    # Paso 7: Buscar botón de órdenes
    print("\n📍 PASO 7: Buscando botón de órdenes de venta...")
    print("   🔍 Probando búsqueda básica...")
    if image_recognition.find_image_on_screen("sap/sap_ventas_order_button.png"):
        print("   ✅ Botón de órdenes encontrado con búsqueda básica")
        return True
    
    print("   🔍 Probando búsqueda robusta...")
    if image_recognition.find_image_robust("sap/sap_ventas_order_button.png", [0.8, 0.7, 0.6, 0.5]):
        print("   ✅ Botón de órdenes encontrado con búsqueda robusta")
        return True
    
    print("   🔍 Probando template matching...")
    if image_recognition.find_image_with_template_matching("sap/sap_ventas_order_button.png", threshold=0.6):
        print("   ✅ Botón de órdenes encontrado con template matching")
        return True
    
    print("   ❌ Botón de órdenes no encontrado con ninguna técnica")
    return False

def main():
    """Función principal"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🧭 TEST DE NAVEGACIÓN SAP")
    print("=" * 60)
    print("Este test verifica paso a paso la navegación en SAP")
    print("para identificar exactamente dónde falla el proceso")
    
    # Confirmar inicio
    input("\nPresiona Enter para iniciar el test de navegación...")
    print()
    
    # Ejecutar test
    success = test_sap_navigation_step_by_step()
    
    if success:
        print("\n🎯 RESULTADO: NAVEGACIÓN EXITOSA")
        print("El sistema puede navegar correctamente en SAP")
    else:
        print("\n❌ RESULTADO: NAVEGACIÓN FALLIDA")
        print("Revisa los pasos anteriores para identificar el problema")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
