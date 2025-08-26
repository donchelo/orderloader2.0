#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Avanzado para el Escritorio Remoto - OrderLoader 2.0
Prueba las estrategias avanzadas de activación
"""

import sys
import time
import subprocess
import json

def test_remote_desktop_manager():
    """Prueba el RemoteDesktopManager completo"""
    print("🔧 Probando RemoteDesktopManager...")
    
    try:
        from main import RemoteDesktopManager
        manager = RemoteDesktopManager()
        
        # Prueba 1: Buscar ventana
        print("\n1️⃣ Buscando ventana del escritorio remoto...")
        window_info = manager.find_remote_desktop_window()
        
        if window_info:
            print(f"✅ Ventana encontrada: {window_info['MainWindowTitle']}")
            print(f"   Proceso: {window_info['ProcessName']}")
            print(f"   ID: {window_info['Id']}")
            
            # Prueba 2: Obtener ventana activa
            print("\n2️⃣ Obteniendo ventana activa...")
            active_title = manager.get_active_window_title()
            print(f"✅ Ventana activa: {active_title}")
            
            # Prueba 3: Activar ventana con estrategias avanzadas
            print("\n3️⃣ Probando activación avanzada...")
            print("¿Deseas probar la activación avanzada? (s/n): ", end="")
            response = input().lower().strip()
            
            if response == 's':
                success = manager.activate_window_advanced(window_info)
                if success:
                    print("✅ ¡Activación avanzada exitosa!")
                    
                    # Prueba 4: Maximizar ventana
                    print("\n4️⃣ Probando maximización...")
                    maximize_success = manager.maximize_window_advanced()
                    if maximize_success:
                        print("✅ ¡Maximización exitosa!")
                    else:
                        print("⚠️ Maximización falló")
                        
                    return True
                else:
                    print("❌ Activación avanzada falló")
                    return False
            else:
                print("Prueba de activación omitida")
                return True
        else:
            print("❌ No se encontró ventana del escritorio remoto")
            return False
            
    except Exception as e:
        print(f"❌ Error en RemoteDesktopManager: {e}")
        return False

def test_powershell_activation():
    """Prueba específica de activación con PowerShell"""
    print("\n🔧 Probando activación con PowerShell...")
    
    try:
        # Buscar ventana del escritorio remoto
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.ProcessName -eq "mstsc"} | Select-Object Id, MainWindowTitle | ConvertTo-Json'], 
            capture_output=True, text=True)
        
        if result.stdout and result.stdout.strip():
            windows = json.loads(result.stdout)
            if not isinstance(windows, list):
                windows = [windows]
            
            if windows:
                window = windows[0]
                process_id = window['Id']
                
                print(f"✅ Encontrada ventana mstsc con ID: {process_id}")
                
                # Script PowerShell para activar ventana
                powershell_script = f'''
                Add-Type -TypeDefinition @"
                using System;
                using System.Runtime.InteropServices;
                public class Win32 {{
                    [DllImport("user32.dll")]
                    [return: MarshalAs(UnmanagedType.Bool)]
                    public static extern bool SetForegroundWindow(IntPtr hWnd);
                    
                    [DllImport("user32.dll")]
                    [return: MarshalAs(UnmanagedType.Bool)]
                    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
                }}
"@
                
                $process = Get-Process -Id {process_id}
                if ($process) {{
                    $handle = $process.MainWindowHandle
                    if ($handle -ne [IntPtr]::Zero) {{
                        [Win32]::ShowWindow($handle, 9)
                        [Win32]::SetForegroundWindow($handle)
                        Write-Host "Ventana activada exitosamente"
                    }} else {{
                        Write-Host "No se pudo obtener el handle de la ventana"
                    }}
                }} else {{
                    Write-Host "Proceso no encontrado"
                }}
                '''
                
                print("🔄 Ejecutando script PowerShell...")
                result = subprocess.run(['powershell', '-Command', powershell_script], 
                                      capture_output=True, text=True)
                
                print(f"Salida: {result.stdout}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                
                time.sleep(2)
                
                # Verificar si la ventana está activa
                active_result = subprocess.run(['powershell', '-Command', 
                    'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object Id | Select-Object -First 1 MainWindowTitle'], 
                    capture_output=True, text=True)
                
                if active_result.stdout:
                    active_title = active_result.stdout.strip()
                    print(f"Ventana activa después: {active_title}")
                    
                    if '20.96.6.64' in active_title or 'remoto' in active_title.lower():
                        print("✅ ¡PowerShell activación exitosa!")
                        return True
                    else:
                        print("❌ PowerShell activación no funcionó")
                        return False
                else:
                    print("❌ No se pudo verificar la ventana activa")
                    return False
            else:
                print("❌ No se encontraron ventanas mstsc")
                return False
        else:
            print("❌ No se pudieron obtener las ventanas")
            return False
            
    except Exception as e:
        print(f"❌ Error en PowerShell activation: {e}")
        return False

def test_win_tab_activation():
    """Prueba específica de activación con Win+Tab"""
    print("\n🔧 Probando activación con Win+Tab...")
    
    try:
        import pyautogui
        
        # Obtener ventana activa antes
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object Id | Select-Object -First 1 MainWindowTitle'], 
            capture_output=True, text=True)
        
        active_before = result.stdout.strip() if result.stdout else "Desconocida"
        print(f"Ventana activa antes: {active_before}")
        
        # Ejecutar Win+Tab
        print("🔄 Ejecutando Win+Tab...")
        pyautogui.hotkey('win', 'tab')
        time.sleep(2)
        
        # Hacer clic en el centro de la pantalla
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        print(f"🔄 Haciendo clic en ({center_x}, {center_y})...")
        pyautogui.click(center_x, center_y)
        time.sleep(1)
        
        # Obtener ventana activa después
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object Id | Select-Object -First 1 MainWindowTitle'], 
            capture_output=True, text=True)
        
        active_after = result.stdout.strip() if result.stdout else "Desconocida"
        print(f"Ventana activa después: {active_after}")
        
        if active_after != active_before:
            print("✅ ¡Win+Tab activación exitosa!")
            return True
        else:
            print("❌ Win+Tab activación no funcionó")
            return False
            
    except Exception as e:
        print(f"❌ Error en Win+Tab activation: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("TEST AVANZADO - ESCRITORIO REMOTO")
    print("=" * 60)
    
    print("\nEste test probará las estrategias avanzadas de activación:")
    print("1. RemoteDesktopManager completo")
    print("2. Activación con PowerShell")
    print("3. Activación con Win+Tab")
    
    print("\nPresiona Enter para comenzar...")
    input()
    
    results = []
    
    # Prueba 1: RemoteDesktopManager
    print("\n" + "="*40)
    print("PRUEBA 1: REMOTE DESKTOP MANAGER")
    print("="*40)
    result1 = test_remote_desktop_manager()
    results.append(("RemoteDesktopManager", result1))
    
    # Prueba 2: PowerShell
    print("\n" + "="*40)
    print("PRUEBA 2: POWERSHELL ACTIVATION")
    print("="*40)
    result2 = test_powershell_activation()
    results.append(("PowerShell", result2))
    
    # Prueba 3: Win+Tab
    print("\n" + "="*40)
    print("PRUEBA 3: WIN+TAB ACTIVATION")
    print("="*40)
    result3 = test_win_tab_activation()
    results.append(("Win+Tab", result3))
    
    # Resumen de resultados
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ EXITOSO" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
    
    successful_tests = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    print(f"\nTotal: {successful_tests}/{total_tests} pruebas exitosas")
    
    if successful_tests > 0:
        print("🎉 ¡Al menos una estrategia de activación funciona!")
    else:
        print("⚠️ Ninguna estrategia funcionó. Revisa la configuración.")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
