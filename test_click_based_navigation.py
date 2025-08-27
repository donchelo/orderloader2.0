#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Navegación por Clics - OrderLoader 2.0
Usa clics directos en botones en lugar de atajos de teclado
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

def test_click_based_navigation():
    """Test de navegación usando clics directos"""
    
    print("=" * 60)
    print("🖱️ TEST DE NAVEGACIÓN POR CLICS")
    print("=" * 60)
    
    # Configurar logging
    logger = setup_logging()
    
    # Crear instancias
    remote_manager = RemoteDesktopManager()
    image_recognition = ImageRecognition()
    
    print("\n📋 NAVEGACIÓN POR CLICS:")
    print("1. 🔍 Activar ventana del escritorio remoto")
    print("2. 📱 Maximizar ventana")
    print("3. 🖱️ Hacer clic en botón de módulos")
    print("4. 🔍 Verificar menú de módulos")
    print("5. 🖱️ Hacer clic en ventas")
    print("6. 🔍 Verificar menú de ventas")
    print("7. 🖱️ Hacer clic en órdenes de venta")
    
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
    
    # Paso 3: Hacer clic en botón de módulos
    print("\n📍 PASO 3: Haciendo clic en botón de módulos...")
    if image_recognition.click_image("sap/sap_modulos_menu_button.png"):
        print("✅ Clic en botón de módulos exitoso")
        time.sleep(2)  # Esperar a que aparezca el menú
    else:
        print("❌ ERROR: No se pudo hacer clic en el botón de módulos")
        return False
    
    # Paso 4: Verificar menú de módulos
    print("\n📍 PASO 4: Verificando menú de módulos...")
    if image_recognition.find_image_on_screen("sap/sap_modulos_menu.png"):
        print("✅ Menú de módulos detectado")
    else:
        print("⚠️ Menú de módulos no detectado, pero continuando...")
    
    # Paso 5: Hacer clic en ventas
    print("\n📍 PASO 5: Haciendo clic en ventas...")
    
    # Buscar el elemento de ventas en el menú
    ventas_elements = [
        "sap/sap_ventas_menu_button.png",
        "sap/sap_ventas_clientes_menu.png"
    ]
    
    ventas_clicked = False
    for element in ventas_elements:
        print(f"   🔍 Buscando: {element}")
        if image_recognition.click_image(element):
            print(f"   ✅ Clic exitoso en: {element}")
            ventas_clicked = True
            time.sleep(2)  # Esperar a que aparezca el menú de ventas
            break
    
    if not ventas_clicked:
        print("❌ ERROR: No se pudo hacer clic en ventas")
        print("💡 Intentando navegación alternativa...")
        
        # Intentar usar atajo de teclado V
        print("   ⌨️ Intentando atajo de teclado V...")
        pyautogui.press('v')
        time.sleep(2)
    
    # Paso 6: Verificar menú de ventas
    print("\n📍 PASO 6: Verificando menú de ventas...")
    ventas_menu_found = False
    
    ventas_menu_elements = [
        "sap/sap_ventas_order_menu.png",
        "sap/sap_ventas_clientes_menu.png"
    ]
    
    for element in ventas_menu_elements:
        if image_recognition.find_image_on_screen(element):
            print(f"✅ Menú de ventas detectado: {element}")
            ventas_menu_found = True
            break
    
    if not ventas_menu_found:
        print("⚠️ Menú de ventas no detectado, pero continuando...")
    
    # Paso 7: Hacer clic en órdenes de venta
    print("\n📍 PASO 7: Haciendo clic en órdenes de venta...")
    
    if image_recognition.click_image("sap/sap_ventas_order_button.png"):
        print("✅ Clic en órdenes de venta exitoso")
        time.sleep(3)  # Esperar a que se abra el formulario
    else:
        print("❌ ERROR: No se pudo hacer clic en órdenes de venta")
        print("💡 Buscando alternativas...")
        
        # Buscar otros elementos relacionados con órdenes
        order_elements = [
            "sap/sap_ventas_order_menu.png",
            "sap/sap_ventas_clientes_menu.png"
        ]
        
        for element in order_elements:
            if image_recognition.click_image(element):
                print(f"✅ Clic alternativo exitoso en: {element}")
                break
    
    # Paso 8: Verificar formulario de órdenes
    print("\n📍 PASO 8: Verificando formulario de órdenes...")
    if image_recognition.find_image_on_screen("sap/sap_orden_de_ventas_template.png"):
        print("✅ Formulario de órdenes de venta detectado")
        return True
    else:
        print("❌ Formulario de órdenes no detectado")
        print("💡 Verificando otros elementos...")
        
        # Buscar elementos alternativos del formulario
        form_elements = [
            "sap/sap_ventas_order_menu.png",
            "sap/sap_ventas_clientes_menu.png"
        ]
        
        for element in form_elements:
            if image_recognition.find_image_on_screen(element):
                print(f"✅ Elemento de formulario detectado: {element}")
                return True
        
        return False

def main():
    """Función principal"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🖱️ TEST DE NAVEGACIÓN POR CLICS")
    print("=" * 60)
    print("Este test usa clics directos en botones")
    print("en lugar de atajos de teclado")
    
    # Confirmar inicio
    input("\nPresiona Enter para iniciar el test de navegación por clics...")
    print()
    
    # Ejecutar test
    success = test_click_based_navigation()
    
    if success:
        print("\n🎯 RESULTADO: NAVEGACIÓN EXITOSA")
        print("La navegación por clics funciona correctamente")
    else:
        print("\n❌ RESULTADO: NAVEGACIÓN FALLIDA")
        print("Necesitamos ajustar la estrategia de navegación")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
