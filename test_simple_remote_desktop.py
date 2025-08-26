#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple para el Escritorio Remoto - OrderLoader 2.0
"""

import sys
import time
import subprocess
import json

def test_find_remote_desktop():
    """Prueba simple para encontrar ventanas del escritorio remoto"""
    print("🔍 Buscando ventanas del escritorio remoto...")
    
    try:
        # Usar PowerShell para obtener todas las ventanas
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'], 
            capture_output=True, text=True)
        
        if result.stdout and result.stdout.strip():
            windows = json.loads(result.stdout)
            if not isinstance(windows, list):
                windows = [windows]
            
            print(f"📋 Encontradas {len(windows)} ventanas:")
            
            remote_windows = []
            for window in windows:
                title = window.get('MainWindowTitle', '')
                process = window.get('ProcessName', '')
                process_id = window.get('Id', '')
                
                print(f"  - {process}: {title} (ID: {process_id})")
                
                # Buscar ventanas de escritorio remoto
                if (process == 'mstsc' or 
                    'Conexión' in title or 
                    'Remote' in title or 
                    'remoto' in title.lower() or
                    '20.96.6.64' in title):
                    remote_windows.append(window)
            
            if remote_windows:
                print(f"\n✅ Encontradas {len(remote_windows)} ventanas de escritorio remoto:")
                for window in remote_windows:
                    print(f"  - {window['MainWindowTitle']} (ID: {window['Id']})")
                return remote_windows
            else:
                print("\n❌ No se encontraron ventanas de escritorio remoto")
                return []
                
        else:
            print("❌ No se pudieron obtener las ventanas")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_get_active_window():
    """Prueba para obtener la ventana activa actual"""
    print("\n🔍 Obteniendo ventana activa actual...")
    
    try:
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object Id | Select-Object -First 1 MainWindowTitle'], 
            capture_output=True, text=True)
        
        if result.stdout:
            active_title = result.stdout.strip()
            print(f"✅ Ventana activa: {active_title}")
            return active_title
        else:
            print("❌ No se pudo obtener la ventana activa")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_activate_window_simple(window_info):
    """Prueba simple de activación de ventana"""
    if not window_info:
        print("❌ No hay información de ventana para activar")
        return False
    
    print(f"\n🔄 Intentando activar: {window_info['MainWindowTitle']}")
    
    try:
        # Estrategia simple: Alt+Tab
        import pyautogui
        print("  - Probando Alt+Tab...")
        
        # Obtener ventana activa antes
        active_before = test_get_active_window()
        
        # Hacer Alt+Tab
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        
        # Obtener ventana activa después
        active_after = test_get_active_window()
        
        if active_after and window_info['MainWindowTitle'] in active_after:
            print("✅ ¡Ventana activada exitosamente con Alt+Tab!")
            return True
        else:
            print(f"❌ Alt+Tab no funcionó. Antes: {active_before}, Después: {active_after}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante activación: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("TEST SIMPLE - ESCRITORIO REMOTO")
    print("=" * 60)
    
    print("\nEste test verificará:")
    print("1. Detección de ventanas del escritorio remoto")
    print("2. Obtención de ventana activa")
    print("3. Activación simple de ventana")
    
    print("\nPresiona Enter para comenzar...")
    input()
    
    # Paso 1: Buscar ventanas
    remote_windows = test_find_remote_desktop()
    
    if not remote_windows:
        print("\n❌ No se encontraron ventanas de escritorio remoto")
        print("Asegúrate de que el escritorio remoto esté abierto")
        print("\nPresiona Enter para salir...")
        input()
        return
    
    # Paso 2: Obtener ventana activa
    active_window = test_get_active_window()
    
    # Paso 3: Intentar activar la primera ventana encontrada
    print(f"\n¿Deseas intentar activar la ventana del escritorio remoto? (s/n): ", end="")
    response = input().lower().strip()
    
    if response == 's':
        success = test_activate_window_simple(remote_windows[0])
        if success:
            print("\n🎉 ¡Test exitoso! La ventana del escritorio remoto está activa")
        else:
            print("\n⚠️ Test parcialmente exitoso. Se detectó la ventana pero no se pudo activar")
    else:
        print("\nTest de activación omitido")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
