#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para OrderLoader 2.0
Identifica ventanas abiertas y procesos de escritorio remoto
"""

import subprocess
import pyautogui
import time

def get_active_windows():
    """Obtiene todas las ventanas activas"""
    print("🔍 Buscando ventanas activas...")
    print("=" * 50)
    
    try:
        # Usar PowerShell para obtener ventanas
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object ProcessName, MainWindowTitle, Id | Format-Table -AutoSize'], 
            capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        else:
            print("No se encontraron ventanas con títulos")
            
    except Exception as e:
        print(f"Error obteniendo ventanas: {e}")

def get_remote_desktop_processes():
    """Busca específicamente procesos de escritorio remoto"""
    print("\n🔍 Buscando procesos de escritorio remoto...")
    print("=" * 50)
    
    try:
        # Buscar procesos relacionados con escritorio remoto
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.ProcessName -like "*mstsc*" -or $_.ProcessName -like "*rdp*" -or $_.MainWindowTitle -like "*Remote*" -or $_.MainWindowTitle -like "*remoto*" -or $_.MainWindowTitle -like "*RDP*"} | Select-Object ProcessName, MainWindowTitle, Id, Path | Format-Table -AutoSize'], 
            capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        else:
            print("No se encontraron procesos de escritorio remoto")
            
    except Exception as e:
        print(f"Error buscando procesos de escritorio remoto: {e}")

def capture_screen_info():
    """Captura información de la pantalla actual"""
    print("\n🔍 Información de pantalla...")
    print("=" * 50)
    
    try:
        screen_width, screen_height = pyautogui.size()
        print(f"Resolución de pantalla: {screen_width}x{screen_height}")
        
        # Obtener posición actual del mouse
        mouse_x, mouse_y = pyautogui.position()
        print(f"Posición del mouse: ({mouse_x}, {mouse_y})")
        
        # Obtener ventana activa
        active_window = pyautogui.getActiveWindow()
        if active_window:
            print(f"Ventana activa: {active_window.title}")
        else:
            print("No se pudo obtener la ventana activa")
            
    except Exception as e:
        print(f"Error obteniendo información de pantalla: {e}")

def test_image_recognition():
    """Prueba el reconocimiento de imágenes"""
    print("\n🔍 Probando reconocimiento de imágenes...")
    print("=" * 50)
    
    try:
        import cv2
        from pathlib import Path
        
        reference_path = Path("reference_images")
        if not reference_path.exists():
            print("❌ Carpeta reference_images no encontrada")
            return
        
        images = list(reference_path.glob("*.png"))
        print(f"Imágenes encontradas: {len(images)}")
        
        for image_path in images:
            print(f"  - {image_path.name}")
            
    except Exception as e:
        print(f"Error probando reconocimiento: {e}")

def main():
    """Función principal de diagnóstico"""
    print("=" * 60)
    print("OrderLoader 2.0 - Diagnóstico del Sistema")
    print("=" * 60)
    
    print("\nEste script te ayudará a identificar:")
    print("1. Ventanas abiertas en el sistema")
    print("2. Procesos de escritorio remoto")
    print("3. Información de pantalla")
    print("4. Imágenes de referencia disponibles")
    
    print("\nPresiona Enter para comenzar el diagnóstico...")
    input()
    
    # Ejecutar diagnósticos
    get_active_windows()
    get_remote_desktop_processes()
    capture_screen_info()
    test_image_recognition()
    
    print("\n" + "=" * 60)
    print("DIAGNÓSTICO COMPLETADO")
    print("=" * 60)
    print("\nRevisa la información arriba para:")
    print("- Identificar el proceso de escritorio remoto")
    print("- Verificar que las imágenes de referencia estén disponibles")
    print("- Confirmar que la resolución de pantalla sea correcta")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
