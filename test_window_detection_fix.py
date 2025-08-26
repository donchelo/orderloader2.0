#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para Diagnosticar y Solucionar el Problema de Detección de Ventana Activa
"""

import sys
import time
import subprocess
import json

def test_get_active_window_methods():
    """Prueba diferentes métodos para obtener la ventana activa"""
    print("🔍 Probando diferentes métodos para obtener la ventana activa...")
    
    methods = [
        {
            'name': 'Método 1 - Sort by Id',
            'command': 'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object Id | Select-Object -First 1 MainWindowTitle'
        },
        {
            'name': 'Método 2 - Sort by ProcessName',
            'command': 'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object ProcessName | Select-Object -First 1 MainWindowTitle'
        },
        {
            'name': 'Método 3 - Get-Window',
            'command': 'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object ProcessName, MainWindowTitle, Id | Format-Table'
        },
        {
            'name': 'Método 4 - User32 API',
            'command': '''
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Win32 {
                [DllImport("user32.dll")]
                public static extern IntPtr GetForegroundWindow();
                
                [DllImport("user32.dll")]
                public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);
                
                [DllImport("user32.dll")]
                public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int lpdwProcessId);
            }
"@
            $hwnd = [Win32]::GetForegroundWindow()
            $processId = 0
            [Win32]::GetWindowThreadProcessId($hwnd, [ref]$processId)
            $process = Get-Process -Id $processId
            Write-Host "Ventana activa: $($process.MainWindowTitle)"
            '''
        }
    ]
    
    results = []
    
    for method in methods:
        print(f"\n{method['name']}:")
        try:
            result = subprocess.run(['powershell', '-Command', method['command']], 
                                  capture_output=True, text=True)
            
            if result.stdout:
                print(f"  Salida: {result.stdout.strip()}")
                results.append((method['name'], result.stdout.strip()))
            else:
                print(f"  Sin salida")
                results.append((method['name'], "Sin salida"))
                
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"  Error: {e}")
            results.append((method['name'], f"Error: {e}"))
    
    return results

def test_manual_window_activation():
    """Prueba activación manual y verificación"""
    print("\n🔧 Probando activación manual...")
    
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
                
                # Script PowerShell mejorado para activar ventana
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
                    
                    [DllImport("user32.dll")]
                    public static extern IntPtr GetForegroundWindow();
                    
                    [DllImport("user32.dll")]
                    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);
                    
                    [DllImport("user32.dll")]
                    public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int lpdwProcessId);
                }}
"@
                
                $process = Get-Process -Id {process_id}
                if ($process) {{
                    $handle = $process.MainWindowHandle
                    if ($handle -ne [IntPtr]::Zero) {{
                        Write-Host "Activando ventana..."
                        [Win32]::ShowWindow($handle, 9)
                        [Win32]::SetForegroundWindow($handle)
                        
                        Start-Sleep -Seconds 2
                        
                        # Verificar ventana activa usando User32 API
                        $activeHwnd = [Win32]::GetForegroundWindow()
                        $activeProcessId = 0
                        [Win32]::GetWindowThreadProcessId($activeHwnd, [ref]$activeProcessId)
                        
                        if ($activeProcessId -eq {process_id}) {{
                            Write-Host "SUCCESS: Ventana activada correctamente"
                        }} else {{
                            Write-Host "FAILED: Ventana no está activa"
                        }}
                    }} else {{
                        Write-Host "ERROR: No se pudo obtener el handle de la ventana"
                    }}
                }} else {{
                    Write-Host "ERROR: Proceso no encontrado"
                }}
                '''
                
                print("🔄 Ejecutando script PowerShell mejorado...")
                result = subprocess.run(['powershell', '-Command', powershell_script], 
                                      capture_output=True, text=True)
                
                print(f"Salida: {result.stdout}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                
                return "SUCCESS" in result.stdout
            else:
                print("❌ No se encontraron ventanas mstsc")
                return False
        else:
            print("❌ No se pudieron obtener las ventanas")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_visual_verification():
    """Prueba verificación visual de la ventana activa"""
    print("\n🔍 Probando verificación visual...")
    
    try:
        import pyautogui
        
        # Tomar screenshot del área donde debería estar la ventana
        screen_width, screen_height = pyautogui.size()
        
        print(f"Resolución de pantalla: {screen_width}x{screen_height}")
        
        # Verificar si hay una ventana visible en el centro
        center_x, center_y = screen_width // 2, screen_height // 2
        
        # Obtener información de la ventana en esa posición
        try:
            import win32gui
            hwnd = win32gui.WindowFromPoint((center_x, center_y))
            if hwnd:
                window_text = win32gui.GetWindowText(hwnd)
                print(f"Ventana en el centro: {window_text}")
                
                if '20.96.6.64' in window_text or 'remoto' in window_text.lower():
                    print("✅ ¡Ventana del escritorio remoto detectada visualmente!")
                    return True
                else:
                    print(f"❌ Ventana en el centro no es del escritorio remoto: {window_text}")
                    return False
            else:
                print("❌ No se pudo obtener información de la ventana en el centro")
                return False
                
        except ImportError:
            print("⚠️ win32gui no disponible, usando método alternativo")
            return False
            
    except Exception as e:
        print(f"❌ Error en verificación visual: {e}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("=" * 60)
    print("DIAGNÓSTICO - DETECCIÓN DE VENTANA ACTIVA")
    print("=" * 60)
    
    print("\nEste test diagnosticará el problema de detección de ventana activa")
    print("y probará diferentes soluciones.")
    
    print("\nPresiona Enter para comenzar...")
    input()
    
    # Paso 1: Probar diferentes métodos de detección
    print("\n" + "="*40)
    print("PASO 1: MÉTODOS DE DETECCIÓN")
    print("="*40)
    detection_results = test_get_active_window_methods()
    
    # Paso 2: Probar activación manual
    print("\n" + "="*40)
    print("PASO 2: ACTIVACIÓN MANUAL")
    print("="*40)
    activation_success = test_manual_window_activation()
    
    # Paso 3: Verificación visual
    print("\n" + "="*40)
    print("PASO 3: VERIFICACIÓN VISUAL")
    print("="*40)
    visual_success = test_visual_verification()
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DEL DIAGNÓSTICO")
    print("="*60)
    
    print("\nMétodos de detección probados:")
    for method_name, result in detection_results:
        print(f"  {method_name}: {result[:100]}...")
    
    print(f"\nActivación manual: {'✅ EXITOSA' if activation_success else '❌ FALLÓ'}")
    print(f"Verificación visual: {'✅ EXITOSA' if visual_success else '❌ FALLÓ'}")
    
    if activation_success or visual_success:
        print("\n🎉 ¡Se encontró una solución que funciona!")
    else:
        print("\n⚠️ Se necesita más investigación para solucionar el problema")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
