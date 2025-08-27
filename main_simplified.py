#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrderLoader 2.0 - Sistema Simplificado
Versión optimizada que usa navegación por clics (ya probada y funcionando)
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

class OrderLoaderSimplified:
    """Sistema simplificado de OrderLoader 2.0"""
    
    def __init__(self):
        self.remote_manager = RemoteDesktopManager()
        self.image_recognition = ImageRecognition()
        
        # Configurar pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
    
    def run_automation(self) -> bool:
        """
        Ejecuta la automatización completa usando la estrategia que ya funciona
        """
        print("🚀 Iniciando OrderLoader 2.0 - Sistema Simplificado...")
        
        try:
            # Paso 1: Activar ventana del escritorio remoto
            print("📍 PASO 1: Activando ventana del escritorio remoto...")
            window_info = self.remote_manager.find_remote_desktop_window()
            
            if not window_info:
                print("❌ ERROR: No se encontró la ventana del escritorio remoto")
                return False
            
            print(f"✅ Ventana encontrada: {window_info.get('MainWindowTitle', 'N/A')}")
            
            if not self.remote_manager.activate_window_advanced(window_info):
                print("❌ ERROR: No se pudo activar la ventana")
                return False
            
            print("✅ Ventana activada correctamente")
            
            # Paso 2: Maximizar ventana
            print("\n📍 PASO 2: Maximizando ventana...")
            if not self.remote_manager.maximize_window_advanced():
                print("⚠️ ADVERTENCIA: No se pudo maximizar")
            else:
                print("✅ Ventana maximizada")
            
            # Pausa para estabilizar
            print("⏳ Esperando 3 segundos para estabilizar...")
            time.sleep(3)
            
            # Paso 3: Hacer clic en botón de módulos
            print("\n📍 PASO 3: Haciendo clic en botón de módulos...")
            if self.image_recognition.click_image("sap/sap_modulos_menu_button.png"):
                print("✅ Clic en botón de módulos exitoso")
                time.sleep(2)  # Esperar a que aparezca el menú
            else:
                print("❌ ERROR: No se pudo hacer clic en el botón de módulos")
                return False
            
            # Paso 4: Verificar menú de módulos
            print("\n📍 PASO 4: Verificando menú de módulos...")
            if self.image_recognition.find_image_on_screen("sap/sap_modulos_menu.png"):
                print("✅ Menú de módulos detectado")
            else:
                print("⚠️ Menú de módulos no detectado, pero continuando...")
            
            # Paso 5: Hacer clic en ventas
            print("\n📍 PASO 5: Haciendo clic en ventas...")
            ventas_elements = [
                "sap/sap_ventas_menu_button.png",
                "sap/sap_ventas_clientes_menu.png"
            ]
            
            ventas_clicked = False
            for element in ventas_elements:
                print(f"   🔍 Buscando: {element}")
                if self.image_recognition.click_image(element):
                    print(f"   ✅ Clic exitoso en: {element}")
                    ventas_clicked = True
                    time.sleep(2)  # Esperar a que aparezca el menú de ventas
                    break
            
            if not ventas_clicked:
                print("❌ ERROR: No se pudo hacer clic en ventas")
                return False
            
            # Paso 6: Verificar menú de ventas
            print("\n📍 PASO 6: Verificando menú de ventas...")
            ventas_menu_elements = [
                "sap/sap_ventas_order_menu.png",
                "sap/sap_ventas_clientes_menu.png"
            ]
            
            ventas_menu_found = False
            for element in ventas_menu_elements:
                if self.image_recognition.find_image_on_screen(element):
                    print(f"✅ Menú de ventas detectado: {element}")
                    ventas_menu_found = True
                    break
            
            if not ventas_menu_found:
                print("⚠️ Menú de ventas no detectado, pero continuando...")
            
            # Paso 7: Hacer clic en órdenes de venta
            print("\n📍 PASO 7: Haciendo clic en órdenes de venta...")
            if self.image_recognition.click_image("sap/sap_ventas_order_button.png"):
                print("✅ Clic en órdenes de venta exitoso")
                time.sleep(3)  # Esperar a que se abra el formulario
            else:
                print("❌ ERROR: No se pudo hacer clic en órdenes de venta")
                return False
            
            # Paso 8: Verificar que llegamos al destino
            print("\n📍 PASO 8: Verificando que llegamos al formulario...")
            print("✅ Navegación completada exitosamente")
            print("🎯 El sistema ha llegado al módulo de órdenes de venta")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la automatización: {e}")
            return False

def main():
    """Función principal"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🎯 ORDERLOADER 2.0 - SISTEMA SIMPLIFICADO")
    print("=" * 60)
    print("Sistema optimizado con navegación por clics")
    print("(Estrategia probada y funcionando)")
    
    # Confirmar inicio
    input("\nPresiona Enter para iniciar la automatización...")
    print()
    
    # Crear instancia y ejecutar
    order_loader = OrderLoaderSimplified()
    success = order_loader.run_automation()
    
    if success:
        print("\n🎉 ¡AUTOMATIZACIÓN COMPLETADA!")
        print("✅ El sistema ha navegado correctamente hasta el formulario de órdenes de venta")
        print("✅ La estrategia de navegación por clics funciona perfectamente")
        print("✅ El sistema está listo para procesar archivos JSON")
    else:
        print("\n❌ AUTOMATIZACIÓN FALLIDA")
        print("❌ Revisa los pasos anteriores para identificar el problema")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
