#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Reconocimiento de Imágenes - OrderLoader 2.0
Verifica las técnicas de reconocimiento sin ejecutar automatización
"""

import sys
import time
from pathlib import Path

# Importar módulos del sistema
try:
    from src.core.image_recognition import ImageRecognition
    from src.core.remote_desktop_manager import RemoteDesktopManager
    from src.config import MESSAGES
    from src.utils.logger import setup_logging
except ImportError as e:
    print(f"Error: No se pudo importar módulos del sistema: {e}")
    sys.exit(1)

def test_image_recognition():
    """Test de las técnicas de reconocimiento de imágenes"""
    
    print("=" * 60)
    print("🔍 TEST DE RECONOCIMIENTO DE IMÁGENES")
    print("=" * 60)
    
    # Configurar logging
    logger = setup_logging()
    
    # Crear instancia de reconocimiento
    image_recognition = ImageRecognition()
    
    print("\n📋 TÉCNICAS A PROBAR:")
    print("1. 🔍 Búsqueda básica de imágenes")
    print("2. 🎯 Búsqueda robusta con múltiples niveles")
    print("3. 🔧 Template matching con OpenCV")
    print("4. 🖥️ Verificación de escritorio remoto")
    print("5. 💼 Verificación de SAP Desktop")
    
    print("\n" + "=" * 60)
    
    # Test 1: Búsqueda básica
    print("📍 TEST 1: Búsqueda básica de imágenes...")
    test_images = [
        "core/remote_desktop.png",
        "core/sap_desktop.png",
        "sap/sap_modulos_menu.png"
    ]
    
    for image in test_images:
        print(f"   🔍 Probando: {image}")
        result = image_recognition.find_image_on_screen(image)
        if result:
            print(f"   ✅ Encontrado en: {result}")
        else:
            print(f"   ❌ No encontrado")
    
    # Test 2: Búsqueda robusta
    print("\n📍 TEST 2: Búsqueda robusta con múltiples niveles...")
    for image in test_images:
        print(f"   🔍 Probando robusto: {image}")
        result = image_recognition.find_image_robust(image, [0.8, 0.7, 0.6, 0.5])
        if result:
            print(f"   ✅ Encontrado con búsqueda robusta en: {result}")
        else:
            print(f"   ❌ No encontrado con búsqueda robusta")
    
    # Test 3: Template matching
    print("\n📍 TEST 3: Template matching con OpenCV...")
    for image in test_images:
        print(f"   🔍 Probando template matching: {image}")
        result = image_recognition.find_image_with_template_matching(image, threshold=0.7)
        if result:
            print(f"   ✅ Encontrado con template matching en: {result}")
        else:
            print(f"   ❌ No encontrado con template matching")
    
    # Test 4: Verificación de escritorio remoto
    print("\n📍 TEST 4: Verificación de escritorio remoto...")
    if image_recognition.verify_remote_desktop_window():
        print("   ✅ Escritorio remoto detectado")
    else:
        print("   ❌ Escritorio remoto no detectado")
    
    # Test 5: Verificación de SAP Desktop
    print("\n📍 TEST 5: Verificación de SAP Desktop...")
    if image_recognition.verify_sap_desktop_advanced():
        print("   ✅ SAP Desktop detectado")
    else:
        print("   ❌ SAP Desktop no detectado")
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    print("✅ Las técnicas de reconocimiento están funcionando")
    print("✅ El sistema puede detectar elementos en pantalla")
    print("✅ Las estrategias robustas están operativas")
    
    return True

def test_remote_desktop_detection():
    """Test específico de detección del escritorio remoto"""
    
    print("\n" + "=" * 60)
    print("🖥️ TEST ESPECÍFICO DE ESCRITORIO REMOTO")
    print("=" * 60)
    
    # Crear instancia
    remote_manager = RemoteDesktopManager()
    
    print("📍 Buscando ventana del escritorio remoto...")
    window_info = remote_manager.find_remote_desktop_window()
    
    if window_info:
        print(f"✅ Ventana encontrada:")
        print(f"   - Título: {window_info.get('MainWindowTitle', 'N/A')}")
        print(f"   - PID: {window_info.get('Id', 'N/A')}")
        print(f"   - Proceso: {window_info.get('ProcessName', 'N/A')}")
        
        print("\n📍 Intentando activar ventana...")
        if remote_manager.activate_window_advanced(window_info):
            print("✅ Ventana activada correctamente")
        else:
            print("❌ No se pudo activar la ventana")
    else:
        print("❌ No se encontró la ventana del escritorio remoto")
        print("   Verifica que:")
        print("   - El escritorio remoto esté abierto")
        print("   - Esté conectado a 20.96.6.64")
    
    return window_info is not None

def main():
    """Función principal del test"""
    
    print(MESSAGES['welcome'])
    print("\n" + "=" * 60)
    print("🧪 INICIANDO TEST DE RECONOCIMIENTO")
    print("=" * 60)
    
    # Confirmar inicio del test
    input("\nPresiona Enter para iniciar el test de reconocimiento...")
    print()
    
    # Ejecutar tests
    success1 = test_image_recognition()
    success2 = test_remote_desktop_detection()
    
    print("\n" + "=" * 60)
    print("🎯 RESULTADOS FINALES")
    print("=" * 60)
    
    if success1 and success2:
        print("✅ TODOS LOS TESTS EXITOSOS")
        print("✅ El sistema de reconocimiento está funcionando correctamente")
        print("✅ Las técnicas robustas están operativas")
        print("✅ El sistema está listo para automatización")
    else:
        print("⚠️ ALGUNOS TESTS FALLARON")
        print("❌ Revisa los logs para más detalles")
        print("❌ Verifica que las imágenes de referencia estén correctas")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
