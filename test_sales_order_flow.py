#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del Flujo de Órdenes de Venta - OrderLoader 2.0
Verifica que el sistema puede navegar correctamente hasta el formulario de órdenes de venta
"""

import sys
import time
from pathlib import Path

# Importar módulos del sistema
try:
    from src.core.sap_automation import SAPAutomation
    from src.config import MESSAGES
    from src.utils.logger import setup_logging
except ImportError as e:
    print(f"Error: No se pudo importar módulos del sistema: {e}")
    sys.exit(1)

def test_sales_order_flow():
    """Test del flujo completo hasta órdenes de venta"""
    
    print("=" * 60)
    print("🧪 TEST DEL FLUJO DE ÓRDENES DE VENTA")
    print("=" * 60)
    
    # Configurar logging
    logger = setup_logging()
    
    # Crear instancia de automatización
    automation = SAPAutomation()
    
    print("\n📋 PASOS DEL TEST:")
    print("1. ✅ Verificar imágenes de referencia")
    print("2. 🔍 Activar escritorio remoto")
    print("3. ✅ Verificar SAP Desktop")
    print("4. 📱 Maximizar ventana")
    print("5. ⌨️ Alt+M (menú de módulos)")
    print("6. ⌨️ V (navegar a ventas)")
    print("7. 🔍 Buscar botón de órdenes de venta")
    print("8. ✅ Verificar formulario de órdenes")
    
    print("\n" + "=" * 60)
    
    # Paso 1: Verificar imágenes
    print("📍 PASO 1: Verificando imágenes de referencia...")
    missing_images = automation.verify_required_images()
    
    if missing_images:
        print(f"❌ ERROR: Faltan las siguientes imágenes:")
        for image in missing_images:
            print(f"   - {image}")
        return False
    
    print("✅ Todas las imágenes de referencia están presentes")
    
    # Paso 2: Activar escritorio remoto
    print("\n📍 PASO 2: Activando escritorio remoto...")
    if not automation.get_remote_desktop():
        print("❌ ERROR: No se pudo activar el escritorio remoto")
        print("   Verifica que:")
        print("   - El escritorio remoto esté abierto")
        print("   - Esté conectado a 20.96.6.64")
        return False
    
    print("✅ Escritorio remoto activado correctamente")
    
    # Paso 3: Verificar SAP Desktop
    print("\n📍 PASO 3: Verificando SAP Desktop...")
    if not automation.verify_sap_desktop():
        print("❌ ERROR: No se pudo verificar SAP Desktop")
        print("   Verifica que:")
        print("   - SAP Desktop esté iniciado en el escritorio remoto")
        print("   - La aplicación esté visible")
        return False
    
    print("✅ SAP Desktop detectado correctamente")
    
    # Paso 4: Maximizar ventana
    print("\n📍 PASO 4: Maximizando ventana...")
    if not automation.remote_manager.maximize_window_advanced():
        print("⚠️ ADVERTENCIA: No se pudo maximizar la ventana, pero continuando...")
    else:
        print("✅ Ventana maximizada correctamente")
    
    # Paso 5: Abrir menú de módulos
    print("\n📍 PASO 5: Abriendo menú de módulos (Alt+M)...")
    if not automation.open_modules_menu():
        print("❌ ERROR: No se pudo abrir el menú de módulos")
        return False
    
    print("✅ Menú de módulos abierto correctamente")
    
    # Paso 6: Navegar a ventas
    print("\n📍 PASO 6: Navegando a ventas (V)...")
    if not automation.navigate_to_sales():
        print("❌ ERROR: No se pudo navegar a ventas")
        return False
    
    print("✅ Navegación a ventas completada")
    
    # Paso 7: Buscar botón de órdenes
    print("\n📍 PASO 7: Buscando botón de órdenes de venta...")
    if not automation.open_sales_order():
        print("❌ ERROR: No se pudo encontrar el botón de órdenes de venta")
        return False
    
    print("✅ Botón de órdenes de venta encontrado y clickeado")
    
    # Paso 8: Verificar formulario
    print("\n📍 PASO 8: Verificando formulario de orden de venta...")
    if not automation.verify_sales_order_form():
        print("❌ ERROR: No se pudo verificar el formulario de orden de venta")
        return False
    
    print("✅ Formulario de orden de venta verificado correctamente")
    
    print("\n" + "=" * 60)
    print("🎉 ¡TEST COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print("✅ El sistema puede navegar correctamente hasta las órdenes de venta")
    print("✅ Todas las técnicas de reconocimiento funcionan correctamente")
    print("✅ El flujo de automatización está operativo")
    
    return True

def main():
    """Función principal del test"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🧪 INICIANDO TEST DEL FLUJO DE ÓRDENES DE VENTA")
    print("=" * 60)
    
    # Confirmar inicio del test
    input("\nPresiona Enter para iniciar el test...")
    print()
    
    # Ejecutar test
    success = test_sales_order_flow()
    
    if success:
        print("\n🎯 RESULTADO: TEST EXITOSO")
        print("El sistema está listo para procesar órdenes de venta")
    else:
        print("\n❌ RESULTADO: TEST FALLIDO")
        print("Revisa los logs para más detalles")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
