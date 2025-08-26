#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Final - Escritorio Remoto Corregido
"""

import sys
import time
import subprocess
import json

def test_corrected_remote_desktop_manager():
    """Prueba el RemoteDesktopManager corregido"""
    print("🔧 Probando RemoteDesktopManager corregido...")
    
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
            
            # Prueba 2: Obtener ventana activa (método corregido)
            print("\n2️⃣ Obteniendo ventana activa (método corregido)...")
            active_title = manager.get_active_window_title()
            print(f"✅ Ventana activa: {active_title}")
            
            # Prueba 3: Activar ventana
            print("\n3️⃣ Probando activación corregida...")
            print("¿Deseas probar la activación? (s/n): ", end="")
            response = input().lower().strip()
            
            if response == 's':
                success = manager.activate_window_advanced(window_info)
                if success:
                    print("✅ ¡Activación exitosa!")
                    
                    # Verificar que realmente está activa
                    time.sleep(1)
                    new_active_title = manager.get_active_window_title()
                    print(f"✅ Ventana activa después: {new_active_title}")
                    
                    # Prueba 4: Maximizar ventana
                    print("\n4️⃣ Probando maximización...")
                    maximize_success = manager.maximize_window_advanced()
                    if maximize_success:
                        print("✅ ¡Maximización exitosa!")
                    else:
                        print("⚠️ Maximización falló")
                        
                    return True
                else:
                    print("❌ Activación falló")
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

def test_sap_automation_complete():
    """Prueba la automatización completa de SAP"""
    print("\n🔧 Probando automatización completa de SAP...")
    
    try:
        from main import SAPAutomation
        automation = SAPAutomation()
        
        # Verificar imágenes de referencia
        print("\n🔍 Verificando imágenes de referencia...")
        missing_images = []
        for image in ["remote_desktop.png", "sap_desktop.png"]:
            if not (automation.reference_path / image).exists():
                missing_images.append(image)
        
        if missing_images:
            print(f"❌ Faltan imágenes: {missing_images}")
            return False
        
        print("✅ Todas las imágenes de referencia están disponibles")
        
        # Prueba de conexión al escritorio remoto
        print("\n🔍 Prueba de conexión al escritorio remoto...")
        print("¿Deseas ejecutar la prueba completa? (s/n): ", end="")
        response = input().lower().strip()
        
        if response == 's':
            success = automation.get_remote_desktop()
            if success:
                print("✅ Conexión al escritorio remoto exitosa")
                
                # Prueba de verificación visual
                print("\n🔍 Prueba de verificación visual...")
                visual_success = automation.verify_remote_desktop_visual()
                if visual_success:
                    print("✅ Verificación visual exitosa")
                else:
                    print("⚠️ Verificación visual falló")
                
                return True
            else:
                print("❌ Conexión al escritorio remoto falló")
                return False
        else:
            print("Prueba completa omitida")
            return False
            
    except Exception as e:
        print(f"❌ Error en automatización SAP: {e}")
        return False

def test_quick_activation():
    """Prueba rápida de activación sin interacción"""
    print("\n🔧 Prueba rápida de activación...")
    
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
                title = window['MainWindowTitle']
                
                print(f"✅ Encontrada ventana: {title} (ID: {process_id})")
                
                # Script de activación rápida
                activation_script = f'''
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
                    
                    [DllImport("user32.dll")]
                    public static extern IntPtr GetForegroundWindow();
                    
                    [DllImport("user32.dll")]
                    public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int lpdwProcessId);
                }}
"@
                
                $process = Get-Process -Id {process_id}
                if ($process) {{
                    $handle = $process.MainWindowHandle
                    if ($handle -ne [IntPtr]::Zero) {{
                        [Win32]::ShowWindow($handle, 9)
                        [Win32]::SetForegroundWindow($handle)
                        
                        Start-Sleep -Seconds 1
                        
                        $activeHwnd = [Win32]::GetForegroundWindow()
                        $activeProcessId = 0
                        [Win32]::GetWindowThreadProcessId($activeHwnd, [ref]$activeProcessId)
                        
                        if ($activeProcessId -eq {process_id}) {{
                            Write-Host "SUCCESS"
                        }} else {{
                            Write-Host "FAILED"
                        }}
                    }} else {{
                        Write-Host "ERROR"
                    }}
                }} else {{
                    Write-Host "ERROR"
                }}
                '''
                
                print("🔄 Ejecutando activación rápida...")
                result = subprocess.run(['powershell', '-Command', activation_script], 
                                      capture_output=True, text=True)
                
                if "SUCCESS" in result.stdout:
                    print("✅ ¡Activación rápida exitosa!")
                    return True
                else:
                    print("❌ Activación rápida falló")
                    return False
            else:
                print("❌ No se encontraron ventanas mstsc")
                return False
        else:
            print("❌ No se pudieron obtener las ventanas")
            return False
            
    except Exception as e:
        print(f"❌ Error en activación rápida: {e}")
        return False

def main():
    """Función principal de prueba final"""
    print("=" * 60)
    print("TEST FINAL - ESCRITORIO REMOTO CORREGIDO")
    print("=" * 60)
    
    print("\nEste test verificará que las correcciones implementadas funcionen:")
    print("1. RemoteDesktopManager corregido")
    print("2. Automatización completa de SAP")
    print("3. Activación rápida")
    
    print("\nPresiona Enter para comenzar...")
    input()
    
    results = []
    
    # Prueba 1: RemoteDesktopManager corregido
    print("\n" + "="*40)
    print("PRUEBA 1: REMOTE DESKTOP MANAGER CORREGIDO")
    print("="*40)
    result1 = test_corrected_remote_desktop_manager()
    results.append(("RemoteDesktopManager Corregido", result1))
    
    # Prueba 2: Automatización completa
    print("\n" + "="*40)
    print("PRUEBA 2: AUTOMATIZACIÓN COMPLETA")
    print("="*40)
    result2 = test_sap_automation_complete()
    results.append(("Automatización Completa", result2))
    
    # Prueba 3: Activación rápida
    print("\n" + "="*40)
    print("PRUEBA 3: ACTIVACIÓN RÁPIDA")
    print("="*40)
    result3 = test_quick_activation()
    results.append(("Activación Rápida", result3))
    
    # Resumen de resultados
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS FINALES")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ EXITOSO" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
    
    successful_tests = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    print(f"\nTotal: {successful_tests}/{total_tests} pruebas exitosas")
    
    if successful_tests == total_tests:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS! El sistema está funcionando correctamente.")
    elif successful_tests > 0:
        print("✅ ¡La mayoría de las pruebas exitosas! El sistema funciona parcialmente.")
    else:
        print("⚠️ Ninguna prueba exitosa. Se necesita más trabajo.")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
