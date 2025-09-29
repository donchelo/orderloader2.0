#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple para OrderLoader
Verificar funcionalidad básica
"""

import sys
import json
from pathlib import Path

try:
    from main import OrderLoader
except ImportError as e:
    print(f"❌ Error importando OrderLoader: {e}")
    sys.exit(1)


def test_system_initialization():
    """Test 1: Inicialización del sistema"""
    print("🔧 Test 1: Inicialización...")
    
    try:
        order_loader = OrderLoader()
        assert order_loader is not None
        assert hasattr(order_loader, 'logger')
        assert hasattr(order_loader, 'run')
        print("✅ Sistema inicializado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        return False


def test_directory_structure():
    """Test 2: Estructura de directorios"""
    print("📁 Test 2: Directorios...")
    
    try:
        order_loader = OrderLoader()
        
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
        print(f"❌ Error en directorios: {e}")
        return False


def test_json_processing():
    """Test 3: Procesamiento de JSON"""
    print("📄 Test 3: Procesamiento JSON...")
    
    try:
        order_loader = OrderLoader()
        
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
        is_valid = order_loader.validate_json(test_file)
        assert is_valid, "Validación de JSON falló"
        
        # Verificar procesamiento
        success = order_loader.process_json(test_file)
        assert success, "Procesamiento de JSON falló"
        
        # Limpiar archivo de prueba
        test_file.unlink(missing_ok=True)
        
        print("✅ Procesamiento de JSON funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en procesamiento JSON: {e}")
        return False


def test_queue_management():
    """Test 4: Gestión de colas"""
    print("📊 Test 4: Gestión de colas...")
    
    try:
        order_loader = OrderLoader()
        
        # Verificar estado de colas
        status = order_loader.get_queue_status()
        assert 'pending' in status
        assert 'completed' in status
        assert 'total' in status
        
        # Verificar que print_status no genera error
        order_loader.print_status()
        
        print("✅ Gestión de colas funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en gestión de colas: {e}")
        return False


def test_system_validation():
    """Test 5: Validación del sistema"""
    print("🔍 Test 5: Validación del sistema...")
    
    try:
        order_loader = OrderLoader()
        
        # Verificar que validate_system funciona
        result = order_loader.validate_system()
        assert isinstance(result, bool)
        
        print("✅ Validación del sistema funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en validación del sistema: {e}")
        return False


def test_sap_environment_setup():
    """Test 6: Configuración del entorno SAP"""
    print("🖥️ Test 6: Configuración del entorno SAP...")
    
    try:
        order_loader = OrderLoader()
        
        # Verificar que setup_sap_environment existe y es callable
        assert hasattr(order_loader, 'setup_sap_environment')
        assert callable(order_loader.setup_sap_environment)
        
        # Nota: No ejecutamos setup_sap_environment porque requiere SAP real
        print("✅ Configuración del entorno SAP está disponible")
        return True
    except Exception as e:
        print(f"❌ Error en configuración del entorno SAP: {e}")
        return False


def test_error_handling():
    """Test 7: Manejo de errores"""
    print("⚠️ Test 7: Manejo de errores...")
    
    try:
        order_loader = OrderLoader()
        
        # Test con archivo inexistente
        from pathlib import Path
        fake_file = Path("archivo_inexistente.json")
        result = order_loader.validate_json(fake_file)
        assert result == False, "Debería fallar con archivo inexistente"
        
        # Test con JSON inválido
        invalid_json = Path("data/pending/invalid.json")
        invalid_json.parent.mkdir(parents=True, exist_ok=True)
        invalid_json.write_text("{ invalid json }")
        
        result = order_loader.validate_json(invalid_json)
        assert result == False, "Debería fallar con JSON inválido"
        
        # Limpiar
        invalid_json.unlink(missing_ok=True)
        
        print("✅ Manejo de errores funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en manejo de errores: {e}")
        return False


def run_all_tests():
    """Ejecutar todos los tests"""
    print("=" * 50)
    print("🧪 TESTS PARA ORDERLOADER SIMPLE")
    print("=" * 50)
    print("Verificando funcionalidad básica...")
    print()
    
    tests = [
        test_system_initialization,
        test_directory_structure,
        test_json_processing,
        test_queue_management,
        test_system_validation,
        test_sap_environment_setup,
        test_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} falló con error: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 RESULTADOS: {passed} ✅ | {failed} ❌")
    
    if failed == 0:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ El sistema está listo para usar")
    else:
        print("⚠️ Algunos tests fallaron")
        print("🔧 Revisa los errores antes de usar")
    
    print("=" * 50)
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    
    print("\n📋 PRÓXIMOS PASOS:")
    if success:
        print("1. ✅ Ejecuta: python main.py")
        print("2. ✅ Asegúrate de que SAP esté abierto en el escritorio remoto")
        print("3. ✅ Coloca archivos JSON en data/pending/")
    else:
        print("1. 🔧 Corrige los errores mostrados arriba")
        print("2. 🔄 Ejecuta este test nuevamente")
    
    input("\nPresiona Enter para salir...")
