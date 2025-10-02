#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Navegación Real - OrderLoader
Prueba Computer Vision para entrar al formulario de SAP
"""

import sys
import time
import pyautogui
import logging
from pathlib import Path
import io

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Importar configuración
from config import (
    PROJECT_ROOT,
    SAP_AUTOMATION_CONFIG,
    WINDOW_ACTIVATION_DELAY,
    WINDOW_MAXIMIZE_DELAY,
    SYSTEM_STABILIZATION_DELAY
)

# Importar SAPAutomation
from sap_automation import SAPAutomation


def setup_logger():
    """Configurar logger para la prueba"""
    logger = logging.getLogger("TestNavegacion")
    logger.setLevel(logging.DEBUG)

    # Handler para consola
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


def countdown(seconds=5):
    """Countdown antes de iniciar"""
    print()
    for i in range(seconds, 0, -1):
        print(f"⏱️  Iniciando en {i}...", end='\r')
        time.sleep(1)
    print("🚀 ¡INICIANDO!                    ")
    print()


def test_navegacion_completa():
    """
    Prueba completa de navegación desde PowerShell hasta formulario SAP.

    Flujo:
    1. PowerShell está activo (ventana actual)
    2. Alt+Tab → activa Chrome/SAP
    3. Espera estabilización
    4. Asume ventana ya maximizada (sin Win+Up)
    5. Navega a Orden de Venta usando Computer Vision
    """
    print("=" * 70)
    print("🧪 TEST DE NAVEGACIÓN REAL - OrderLoader Computer Vision")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANTE:")
    print("   • Este script se ejecuta desde PowerShell")
    print("   • SAP debe estar abierto en Chrome (pero NO activo)")
    print("   • El script hará Alt+Tab automáticamente")
    print("   • NO toques el teclado/mouse durante la ejecución")
    print()
    print("📋 PREPARACIÓN:")
    print("   1. ✅ SAP Business One abierto en Chrome")
    print("   2. ✅ PowerShell activo (esta ventana)")
    print("   3. ✅ No hay ventanas bloqueando la vista")
    print()

    # Confirmar que está listo
    try:
        input("Presiona Enter cuando estés listo para iniciar...")
    except (EOFError, KeyboardInterrupt):
        pass

    # Configurar logger
    logger = setup_logger()

    # Countdown
    countdown(5)

    # CONFIGURACIÓN PARA PRUEBA REAL
    print("⚙️  CONFIGURACIÓN:")
    print(f"   • simulation_mode: False (MODO REAL)")
    print(f"   • confidence: 0.7 (permisivo)")
    print(f"   • search_timeout: 15s")
    print()

    try:
        # PASO 1: Alt+Tab para activar Chrome/SAP
        print("=" * 70)
        print("📍 PASO 1: Activar Chrome/SAP desde PowerShell")
        print("=" * 70)
        logger.info("🔄 Presionando Alt+Tab...")

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        pyautogui.hotkey('alt', 'tab')
        time.sleep(WINDOW_ACTIVATION_DELAY)

        logger.info("✅ Alt+Tab ejecutado")
        print()

        # PASO 2: Esperar estabilización
        print("=" * 70)
        print("📍 PASO 2: Esperando estabilización")
        print("=" * 70)
        logger.info(f"⏳ Esperando {SYSTEM_STABILIZATION_DELAY}s...")
        time.sleep(SYSTEM_STABILIZATION_DELAY)
        logger.info("✅ Estabilizado")
        print()

        # PASO 3: SKIPPED - Asumimos ventana ya maximizada
        # print("=" * 70)
        # print("📍 PASO 3: Maximizar ventana")
        # print("=" * 70)
        # logger.info("📱 Presionando Win+Up...")
        # pyautogui.hotkey('win', 'up')
        # time.sleep(WINDOW_MAXIMIZE_DELAY)
        # logger.info("✅ Ventana maximizada")
        # time.sleep(1)  # Espera adicional
        # print()

        # PASO 3: Inicializar SAPAutomation
        print("=" * 70)
        print("📍 PASO 3: Inicializar Computer Vision")
        print("=" * 70)
        assets_path = PROJECT_ROOT / "assets" / "images" / "sap"
        logger.info(f"📂 Assets path: {assets_path}")

        # IMPORTANTE: Modo real, NO simulación
        sap_automation = SAPAutomation(
            logger=logger,
            assets_path=assets_path,
            simulation_mode=False  # ← MODO REAL
        )

        # Configurar para prueba
        sap_automation.confidence = 0.7  # Más permisivo
        sap_automation.timeout = 15  # Más tiempo

        logger.info("✅ SAPAutomation inicializado en MODO REAL")
        print()

        # PASO 4: Tomar screenshot inicial
        print("=" * 70)
        print("📍 PASO 4: Screenshot inicial")
        print("=" * 70)
        sap_automation.take_debug_screenshot("inicial")
        print()

        # PASO 5: Navegar a Orden de Venta
        print("=" * 70)
        print("📍 PASO 5: Navegación con Computer Vision")
        print("=" * 70)
        logger.info("🧭 Iniciando navegación a Orden de Venta...")
        print()

        success = sap_automation.navigate_to_sales_order()

        print()
        print("=" * 70)

        if success:
            print("🎉 ¡ÉXITO! Formulario de Orden de Venta abierto")
            print("=" * 70)
            print()
            print("✅ El sistema detectó correctamente:")
            print("   • Botón 'Módulos'")
            print("   • Menú 'Ventas'")
            print("   • Botón 'Orden de Venta'")
            print()
            print("📸 Screenshots guardados para referencia")

            # Tomar screenshot final
            sap_automation.take_debug_screenshot("formulario_abierto")

            return True
        else:
            print("❌ FALLO: No se pudo completar la navegación")
            print("=" * 70)
            print()
            print("🔍 Posibles causas:")
            print("   • Imágenes de referencia no coinciden")
            print("   • SAP no estaba visible")
            print("   • Confidence demasiado alto")
            print()
            print("📋 Acciones recomendadas:")
            print("   1. Revisar screenshots en debug_*.png")
            print("   2. Comparar con imágenes de referencia")
            print("   3. Re-capturar imágenes si es necesario")
            print("   4. Reducir confidence a 0.6")

            # Tomar screenshot de error
            sap_automation.take_debug_screenshot("error")

            return False

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por el usuario")
        return False

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        logger.error(f"Error: {type(e).__name__} - {str(e)}")
        return False


def main():
    """Función principal"""
    success = test_navegacion_completa()

    print()
    print("=" * 70)
    print("📊 RESUMEN DE LA PRUEBA")
    print("=" * 70)

    if success:
        print("✅ Estado: ÉXITO")
        print()
        print("🎯 Próximos pasos:")
        print("   1. Capturar imágenes del formulario")
        print("   2. Implementar llenado de campos")
        print("   3. Actualizar config.py con simulation_mode=False")
    else:
        print("❌ Estado: FALLO")
        print()
        print("🔧 Próximos pasos:")
        print("   1. Revisar logs arriba")
        print("   2. Verificar screenshots de debug")
        print("   3. Ajustar imágenes o configuración")
        print("   4. Re-ejecutar prueba")

    print()
    try:
        input("Presiona Enter para salir...")
    except (EOFError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
