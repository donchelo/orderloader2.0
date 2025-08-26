#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para OrderLoader 2.0
Verifica que todas las dependencias e imágenes estén correctamente configuradas
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Verifica la versión de Python"""
    print("🔍 Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.7+")
        return False

def test_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    dependencies = [
        ('pyautogui', 'pyautogui'),
        ('opencv-python', 'cv2'),
        ('Pillow', 'PIL'),
        ('numpy', 'numpy')
    ]
    
    missing = []
    for package_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            print(f"❌ {package_name} - FALTANTE")
            missing.append(package_name)
    
    if missing:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(missing)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def test_images():
    """Verifica que todas las imágenes de referencia existan"""
    print("\n🔍 Verificando imágenes de referencia...")
    
    reference_path = Path("reference_images")
    if not reference_path.exists():
        print("❌ Carpeta 'reference_images' no encontrada")
        return False
    
    required_images = [
        "remote_desktop.png",
        "sap_desktop.png", 
        "sap_modulos_menu.png",
        "sap_ventas_order_menu.png",
        "sap_ventas_order_button.png",
        "sap_orden_de_ventas_template.png"
    ]
    
    missing = []
    for image in required_images:
        image_path = reference_path / image
        if image_path.exists():
            print(f"✅ {image} - OK")
        else:
            print(f"❌ {image} - FALTANTE")
            missing.append(image)
    
    if missing:
        print(f"\n⚠️  Imágenes faltantes: {', '.join(missing)}")
        return False
    
    return True

def test_config():
    """Verifica que el archivo de configuración esté presente"""
    print("\n🔍 Verificando archivo de configuración...")
    
    if Path("config.py").exists():
        try:
            from config import RECOGNITION_CONFIG, REQUIRED_IMAGES, KEYBOARD_SHORTCUTS
            print("✅ config.py - OK")
            return True
        except ImportError as e:
            print(f"❌ config.py - Error de importación: {e}")
            return False
    else:
        print("❌ config.py - FALTANTE")
        return False

def test_main_script():
    """Verifica que el script principal esté presente"""
    print("\n🔍 Verificando script principal...")
    
    if Path("main.py").exists():
        print("✅ main.py - OK")
        return True
    else:
        print("❌ main.py - FALTANTE")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("OrderLoader 2.0 - Verificación de Configuración")
    print("=" * 60)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_images,
        test_config,
        test_main_script
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    
    if all(results):
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ OrderLoader 2.0 está listo para usar")
        print("\nPara ejecutar:")
        print("  - Doble clic en 'launcher.bat'")
        print("  - O ejecuta: python main.py")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("⚠️  Revisa los errores arriba y corrígelos antes de continuar")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
