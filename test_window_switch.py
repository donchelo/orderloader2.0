#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para cambiar a la ventana del escritorio remoto
"""

import subprocess
import pyautogui
import time
import json
import os

def find_remote_desktop_window():
    """Encuentra la ventana del escritorio remoto"""
    print("🔍 Buscando ventana del escritorio remoto...")
    
    try:
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'], 
            capture_output=True, text=True)
        
        if result.stdout:
            windows = json.loads(result.stdout)
            if not isinstance(windows, list):
                windows = [windows]
            
            for window in windows:
                title = window.get('MainWindowTitle', '')
                process = window.get('ProcessName', '')
                
                print(f"  - {process}: {title}")
                
                if (process == 'mstsc' or 
                    'Conexión' in title or 
                    'Remote' in title or 
                    'remoto' in title.lower()):
                    print(f"✅ Ventana de escritorio remoto encontrada: {title}")
                    return window
        
        print("❌ No se encontró ventana de escritorio remoto")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_active_window_title():
    """Obtiene el título de la ventana activa actual"""
    try:
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object Id | Select-Object -First 1 MainWindowTitle'], 
            capture_output=True, text=True)
        
        if result.stdout:
            return result.stdout.strip()
        return None
    except:
        return None

def switch_to_window_advanced(window_info):
    """Cambia a la ventana usando múltiples estrategias"""
    if not window_info:
        return False
    
    target_title = window_info['MainWindowTitle']
    print(f"🔄 Cambiando a: {target_title}")
    
    # Estrategia 1: Alt+Tab múltiples veces
    print("  - Estrategia 1: Alt+Tab múltiple...")
    for i in range(10):
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.3)
        
        current_title = get_active_window_title()
        if current_title and target_title in current_title:
            print(f"✅ ¡Ventana activada con Alt+Tab en intento {i+1}!")
            return True
    
    # Estrategia 2: Usar Win+Tab para ver todas las ventanas
    print("  - Estrategia 2: Win+Tab...")
    pyautogui.hotkey('win', 'tab')
    time.sleep(1)
    
    # Buscar y hacer clic en la ventana del escritorio remoto
    screen_width, screen_height = pyautogui.size()
    
    # Intentar hacer clic en diferentes posiciones donde podría estar la ventana
    click_positions = [
        (screen_width // 2, screen_height // 2),  # Centro
        (screen_width // 4, screen_height // 2),  # Izquierda
        (3 * screen_width // 4, screen_height // 2),  # Derecha
        (screen_width // 2, screen_height // 4),  # Arriba
        (screen_width // 2, 3 * screen_height // 4),  # Abajo
    ]
    
    for pos in click_positions:
        pyautogui.click(pos)
        time.sleep(0.5)
        
        current_title = get_active_window_title()
        if current_title and target_title in current_title:
            print(f"✅ ¡Ventana activada con clic en posición {pos}!")
            return True
    
    # Estrategia 3: Usar Alt+Esc para cambiar entre ventanas
    print("  - Estrategia 3: Alt+Esc...")
    for i in range(5):
        pyautogui.hotkey('alt', 'esc')
        time.sleep(0.5)
        
        current_title = get_active_window_title()
        if current_title and target_title in current_title:
            print(f"✅ ¡Ventana activada con Alt+Esc en intento {i+1}!")
            return True
    
    # Estrategia 4: Usar PowerShell para activar directamente
    print("  - Estrategia 4: Activación directa con PowerShell...")
    try:
        process_id = window_info['Id']
        result = subprocess.run(['powershell', '-Command', 
            f'$process = Get-Process -Id {process_id}; if ($process) {{ $process.MainWindowHandle | ForEach-Object {{ [System.Windows.Forms.SendKeys]::SendWait("{{ENTER}}") }} }}'], 
            capture_output=True, text=True)
        
        time.sleep(1)
        current_title = get_active_window_title()
        if current_title and target_title in current_title:
            print("✅ ¡Ventana activada con PowerShell!")
            return True
    except Exception as e:
        print(f"    Error con PowerShell: {e}")
    
    # Estrategia 5: Hacer clic en la barra de tareas
    print("  - Estrategia 5: Clic en barra de tareas...")
    try:
        # Hacer clic en la parte inferior de la pantalla (barra de tareas)
        pyautogui.click(screen_width // 2, screen_height - 10)
        time.sleep(0.5)
        
        # Buscar y hacer clic en el icono del escritorio remoto
        # Esto es más difícil, pero podemos intentar
        pyautogui.click(screen_width // 2, screen_height - 50)
        time.sleep(1)
        
        current_title = get_active_window_title()
        if current_title and target_title in current_title:
            print("✅ ¡Ventana activada desde barra de tareas!")
            return True
    except Exception as e:
        print(f"    Error con barra de tareas: {e}")
    
    # Estrategia 6: Usar comandos directos de Windows
    print("  - Estrategia 6: Comandos directos de Windows...")
    try:
        # Usar tasklist para verificar que el proceso esté ejecutándose
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq mstsc.exe'], 
                              capture_output=True, text=True)
        
        if 'mstsc.exe' in result.stdout:
            print("    Proceso mstsc.exe encontrado, intentando activar...")
            
            # Usar el comando taskkill para "refrescar" el proceso
            subprocess.run(['taskkill', '/F', '/IM', 'mstsc.exe'], 
                         capture_output=True, text=True)
            time.sleep(1)
            
            # Volver a ejecutar mstsc
            subprocess.Popen(['mstsc'], shell=True)
            time.sleep(3)
            
            current_title = get_active_window_title()
            if current_title and target_title in current_title:
                print("✅ ¡Ventana activada con comandos directos!")
                return True
    except Exception as e:
        print(f"    Error con comandos directos: {e}")
    
    # Estrategia 7: Usar PowerShell para forzar la activación
    print("  - Estrategia 7: PowerShell forzado...")
    try:
        process_id = window_info['Id']
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
                Write-Host "Ventana activada"
            }}
        }}
        '''
        
        result = subprocess.run(['powershell', '-Command', powershell_script], 
                              capture_output=True, text=True)
        
        time.sleep(2)
        current_title = get_active_window_title()
        if current_title and target_title in current_title:
            print("✅ ¡Ventana activada con PowerShell forzado!")
            return True
    except Exception as e:
        print(f"    Error con PowerShell forzado: {e}")
    
    # Estrategia 8: Usar el comando start para abrir una nueva conexión
    print("  - Estrategia 8: Nueva conexión RDP...")
    try:
        # Extraer la IP del título de la ventana
        if '20.96.6.64' in target_title:
            ip = '20.96.6.64'
            print(f"    Intentando conectar a {ip}...")
            
            # Usar el comando start para abrir una nueva conexión
            subprocess.Popen(['start', 'mstsc', f'/v:{ip}'], shell=True)
            time.sleep(3)
            
            current_title = get_active_window_title()
            if current_title and target_title in current_title:
                print("✅ ¡Nueva conexión RDP activada!")
                return True
    except Exception as e:
        print(f"    Error con nueva conexión: {e}")
    
    print("❌ No se pudo activar la ventana con ninguna estrategia")
    return False

def main():
    """Función principal"""
    print("=" * 60)
    print("Test de Cambio de Ventanas - OrderLoader 2.0")
    print("=" * 60)
    
    print("\nEste script probará múltiples estrategias para activar")
    print("la ventana del escritorio remoto")
    print("Asegúrate de que el escritorio remoto esté abierto")
    
    print("\nPresiona Enter para comenzar...")
    input()
    
    # Encontrar la ventana
    remote_window = find_remote_desktop_window()
    
    if remote_window:
        print(f"\nVentana encontrada: {remote_window['MainWindowTitle']}")
        print("ID:", remote_window['Id'])
        print("Proceso:", remote_window['ProcessName'])
        
        print("\nPresiona Enter para intentar cambiar a esta ventana...")
        input()
        
        # Cambiar a la ventana con estrategias avanzadas
        success = switch_to_window_advanced(remote_window)
        
        if success:
            print("\n🎉 ¡Test exitoso! La ventana del escritorio remoto está activa")
            print("Ahora puedes ejecutar la automatización completa")
        else:
            print("\n❌ Test fallido. No se pudo cambiar a la ventana")
            print("Sugerencias:")
            print("- Intenta hacer clic manualmente en la ventana del escritorio remoto")
            print("- Asegúrate de que la ventana no esté minimizada")
            print("- Verifica que no haya otras ventanas bloqueando")
            print("- Considera usar el comando: start mstsc /v:20.96.6.64")
    else:
        print("\n❌ No se encontró la ventana del escritorio remoto")
        print("Asegúrate de que esté abierta y visible")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
