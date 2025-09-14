#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para OrderLoader Final
Verificar que la versión consolidada funciona correctamente
"""

import sys
import json
import tempfile
from pathlib import Path

# Importar la clase principal
try:
    from main import OrderLoaderFinal
    from config import REQUIRED_IMAGES, IMAGES_PATH
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)

def test_system_initialization():
    """Test 1: Inicialización del sistema"""
    print("🔧 Test 1: Inicialización del sistema...")
    
    try:
        order_loader = OrderLoaderFinal()
        assert order_loader is not None
        assert hasattr(order_loader, 'logger')
        assert hasattr(order_loader, 'validate_system')
        assert hasattr(order_loader, 'run')
        print("✅ Sistema inicializado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        return False

def test_directory_structure():
    """Test 2: Estructura de directorios"""
    print("📁 Test 2: Estructura de directorios...")
    
    try:
        order_loader = OrderLoaderFinal()
        
        # Verificar que se crearon las carpetas esenciales
        required_dirs = [
            Path("data"),
            Path("data/pending"),
            Path("data/completed"),
            Path("logs")
        ]
        
        for directory in required_dirs:
            assert directory.exists(), f"Directorio no existe: {directory}"
        
        print("✅ Estructura de directorios correcta")
        return True
    except Exception as e:
        print(f"❌ Error en estructura de directorios: {e}")
        return False

def test_image_validation():
    """Test 3: Validación de imágenes (ya no requeridas)"""
    print("🖼️ Test 3: Validación de imágenes...")
    
    try:
        order_loader = OrderLoaderFinal()
        
        # Ya no se requieren imágenes para navegación automática
        assert len(REQUIRED_IMAGES) == 0, "No deberían requerirse imágenes"
        print("✅ Sistema simplificado - No se requieren imágenes")
        
        return True
    except Exception as e:
        print(f"❌ Error en validación de imágenes: {e}")
        return False

def test_json_processing():
    """Test 4: Procesamiento de JSON"""
    print("📄 Test 4: Procesamiento de JSON...")
    
    try:
        order_loader = OrderLoaderFinal()
        
        # Crear archivo JSON de prueba
        test_json = {
            "orden_compra": "TEST001",
            "fecha_documento": "01/01/2024",
            "comprador": {"nit": "TEST", "nombre": "Test Company"},
            "items": [{"descripcion": "Test Item", "codigo": "TEST001", "cantidad": 1, "precio_unitario": 100}],
            "valor_total": 100
        }
        
        test_file = Path("data/pending/test.json")
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_json, f, indent=2, ensure_ascii=False)
        
        # Verificar que puede leer archivos pendientes
        pending_files = order_loader.get_pending_files()
        assert len(pending_files) >= 1, "No se detectaron archivos pendientes"
        
        # Verificar validación de JSON
        is_valid = order_loader.validate_json_file(test_file)
        assert is_valid, "Validación de JSON falló"
        
        # Verificar procesamiento
        success = order_loader.process_json_file(test_file)
        assert success, "Procesamiento de JSON falló"
        
        # Limpiar archivo de prueba
        test_file.unlink(missing_ok=True)
        
        print("✅ Procesamiento de JSON funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en procesamiento de JSON: {e}")
        return False

def test_queue_management():
    """Test 5: Gestión de colas"""
    print("📊 Test 5: Gestión de colas...")
    
    try:
        order_loader = OrderLoaderFinal()
        
        # Crear archivo de prueba
        test_file = Path("data/pending/queue_test.json")
        test_data = {"test": "data"}
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Verificar detección
        pending_before = len(order_loader.get_pending_files())
        assert pending_before >= 1, "No se detectó archivo de prueba"
        
        # Verificar estado de colas
        status = order_loader.get_queue_status()
        assert 'pending' in status
        assert 'completed' in status
        assert 'total' in status
        
        # Limpiar
        test_file.unlink(missing_ok=True)
        
        print("✅ Gestión de colas funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en gestión de colas: {e}")
        return False

def test_basic_functionality():
    """Test 6: Funcionalidad básica"""
    print("🔧 Test 6: Funcionalidad básica...")
    
    try:
        order_loader = OrderLoaderFinal()
        
        # Verificar que la clase se inicializa correctamente
        assert hasattr(order_loader, 'validate_system'), "Método validate_system no existe"
        assert hasattr(order_loader, 'find_remote_desktop_window'), "Método find_remote_desktop_window no existe"
        assert hasattr(order_loader, 'verify_sap_visible'), "Método verify_sap_visible no existe"
        assert hasattr(order_loader, 'process_queue'), "Método process_queue no existe"
        
        # Verificar que ya no existe navigate_sap
        assert not hasattr(order_loader, 'navigate_sap'), "Método navigate_sap debería haber sido eliminado"
        
        # Verificar estado de colas
        order_loader.print_queue_status()  # No debe generar error
        
        print("✅ Funcionalidad básica correcta")
        return True
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("=" * 60)
    print("🧪 TESTS PARA ORDERLOADER SIMPLIFICADO v5.0.0")
    print("=" * 60)
    print("Verificando funcionalidad básica sin conexión SAP...")
    print()
    
    tests = [
        test_system_initialization,
        test_directory_structure,
        test_image_validation,
        test_json_processing,
        test_queue_management,
        test_basic_functionality
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test.__name__} falló")
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} falló con error: {e}")
        print()
    
    print("=" * 60)
    print(f"📊 RESULTADOS: {passed} ✅ | {failed} ❌")
    
    if failed == 0:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ La versión final consolidada está lista para usar")
    else:
        print("⚠️ Algunos tests fallaron")
        print("🔧 Revisa los errores antes de usar en producción")
    
    print("=" * 60)
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    
    print("\n📋 PRÓXIMOS PASOS:")
    if success:
        print("1. ✅ Asegúrate de que SAP esté abierto en el escritorio remoto")
        print("2. ✅ Coloca archivos JSON en data/pending/")
        print("3. ✅ Ejecuta: python main.py")
    else:
        print("1. 🔧 Corrige los errores mostrados arriba")
        print("2. 🔄 Ejecuta este test nuevamente")
    
    input("\nPresiona Enter para salir...")
