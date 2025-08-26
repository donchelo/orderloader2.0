#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Escritorio Remoto - OrderLoader 2.0
Maneja la detección, activación y maximización de ventanas de escritorio remoto
"""

import time
import logging
import subprocess
import json
from typing import Optional, Dict, Any

import pyautogui

from ..config import REMOTE_DESKTOP_CONFIG, ACTIVATION_STRATEGIES, KEYBOARD_SHORTCUTS

logger = logging.getLogger(__name__)

class RemoteDesktopManager:
    """Gestor especializado para el escritorio remoto"""
    
    def __init__(self):
        self.remote_desktop_window = REMOTE_DESKTOP_CONFIG['window_title']
        self.max_attempts = REMOTE_DESKTOP_CONFIG['max_attempts']
        self.retry_delay = REMOTE_DESKTOP_CONFIG['retry_delay']
        
    def find_remote_desktop_window(self) -> Optional[Dict[str, Any]]:
        """Encuentra la ventana del escritorio remoto usando múltiples estrategias"""
        logger.info("🔍 Buscando ventana del escritorio remoto...")
        
        try:
            # Estrategia 1: PowerShell para obtener todas las ventanas
            result = subprocess.run(['powershell', '-Command', 
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'], 
                capture_output=True, text=True)
            
            if result.stdout and result.stdout.strip():
                windows = json.loads(result.stdout)
                if not isinstance(windows, list):
                    windows = [windows]
                
                for window in windows:
                    title = window.get('MainWindowTitle', '')
                    process = window.get('ProcessName', '')
                    
                    # Buscar por múltiples criterios
                    if (process == 'mstsc' or 
                        'Conexión' in title or 
                        'Remote' in title or 
                        'remoto' in title.lower() or
                        '20.96.6.64' in title):
                        logger.info(f"✅ Ventana de escritorio remoto encontrada: {title}")
                        return window
            
            logger.warning("No se encontró ventana de escritorio remoto con PowerShell")
            return None
            
        except Exception as e:
            logger.error(f"Error buscando ventana: {e}")
            return None
    
    def get_active_window_title(self) -> Optional[str]:
        """Obtiene el título de la ventana activa actual usando User32 API"""
        try:
            powershell_script = '''
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
            Write-Host $process.MainWindowTitle
            '''
            
            result = subprocess.run(['powershell', '-Command', powershell_script], 
                                  capture_output=True, text=True)
            
            if result.stdout:
                return result.stdout.strip()
            return None
        except Exception as e:
            logger.error(f"Error obteniendo ventana activa: {e}")
            return None
    
    def activate_window_advanced(self, window_info: Dict[str, Any]) -> bool:
        """Activa la ventana usando múltiples estrategias avanzadas"""
        if not window_info:
            return False
        
        target_title = window_info['MainWindowTitle']
        process_id = window_info['Id']
        logger.info(f"🔄 Activando ventana: {target_title}")
        
        # Estrategia 1: Alt+Tab múltiple
        logger.info("  - Estrategia 1: Alt+Tab múltiple...")
        for i in range(ACTIVATION_STRATEGIES['alt_tab_attempts']):
            pyautogui.hotkey(*KEYBOARD_SHORTCUTS['alt_tab'])
            time.sleep(ACTIVATION_STRATEGIES['alt_tab_delay'])
            
            current_title = self.get_active_window_title()
            if current_title and target_title in current_title:
                logger.info(f"✅ ¡Ventana activada con Alt+Tab en intento {i+1}!")
                return True
        
        # Estrategia 2: PowerShell con SetForegroundWindow
        logger.info("  - Estrategia 2: PowerShell SetForegroundWindow...")
        try:
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
            
            time.sleep(ACTIVATION_STRATEGIES['powershell_timeout'])
            
            # Verificar usando User32 API directamente
            verification_script = f'''
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Win32 {{
                [DllImport("user32.dll")]
                public static extern IntPtr GetForegroundWindow();
                
                [DllImport("user32.dll")]
                public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int lpdwProcessId);
            }}
"@
            $activeHwnd = [Win32]::GetForegroundWindow()
            $activeProcessId = 0
            [Win32]::GetWindowThreadProcessId($activeHwnd, [ref]$activeProcessId)
            
            if ($activeProcessId -eq {process_id}) {{
                Write-Host "SUCCESS"
            }} else {{
                Write-Host "FAILED"
            }}
            '''
            
            verification_result = subprocess.run(['powershell', '-Command', verification_script], 
                                               capture_output=True, text=True)
            
            if "SUCCESS" in verification_result.stdout:
                logger.info("✅ ¡Ventana activada con PowerShell!")
                return True
        except Exception as e:
            logger.error(f"Error con PowerShell: {e}")
        
        # Estrategia 3: Win+Tab y clic
        logger.info("  - Estrategia 3: Win+Tab y clic...")
        try:
            pyautogui.hotkey(*KEYBOARD_SHORTCUTS['win_tab'])
            time.sleep(ACTIVATION_STRATEGIES['win_tab_delay'])
            
            screen_width, screen_height = pyautogui.size()
            click_positions = [
                (screen_width // 2, screen_height // 2),
                (screen_width // 4, screen_height // 2),
                (3 * screen_width // 4, screen_height // 2),
            ]
            
            for pos in click_positions:
                pyautogui.click(pos)
                time.sleep(ACTIVATION_STRATEGIES['click_delay'])
                
                current_title = self.get_active_window_title()
                if current_title and target_title in current_title:
                    logger.info(f"✅ ¡Ventana activada con clic en posición {pos}!")
                    return True
        except Exception as e:
            logger.error(f"Error con Win+Tab: {e}")
        
        # Estrategia 4: Nueva conexión RDP
        logger.info("  - Estrategia 4: Nueva conexión RDP...")
        try:
            if REMOTE_DESKTOP_CONFIG['ip_address'] in target_title:
                subprocess.Popen(['start', 'mstsc', f'/v:{REMOTE_DESKTOP_CONFIG["ip_address"]}'], shell=True)
                time.sleep(ACTIVATION_STRATEGIES['new_connection_timeout'])
                
                current_title = self.get_active_window_title()
                if current_title and target_title in current_title:
                    logger.info("✅ ¡Nueva conexión RDP activada!")
                    return True
        except Exception as e:
            logger.error(f"Error con nueva conexión: {e}")
        
        logger.error("❌ No se pudo activar la ventana con ninguna estrategia")
        return False
    
    def maximize_window_advanced(self) -> bool:
        """Maximiza la ventana usando múltiples estrategias"""
        logger.info("🔄 Maximizando ventana...")
        
        # Estrategia 1: Win+Up
        try:
            pyautogui.hotkey(*KEYBOARD_SHORTCUTS['maximize_window'])
            time.sleep(1)
            logger.info("✅ Ventana maximizada con Win+Up")
            return True
        except Exception as e:
            logger.error(f"Error con Win+Up: {e}")
        
        # Estrategia 2: Alt+Space, X
        try:
            pyautogui.hotkey(*KEYBOARD_SHORTCUTS['maximize_alt_space'])
            time.sleep(0.5)
            pyautogui.press(KEYBOARD_SHORTCUTS['maximize_x'])
            time.sleep(1)
            logger.info("✅ Ventana maximizada con Alt+Space, X")
            return True
        except Exception as e:
            logger.error(f"Error con Alt+Space: {e}")
        
        return False
