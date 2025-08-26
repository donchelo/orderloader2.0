#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrderLoader 2.0 - Automatización de SAP para Órdenes de Venta
Autor: Sistema Automatizado
Versión: 2.0
"""

import sys
import time
import logging
import subprocess
import json
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# Importar módulos de automatización
try:
    import pyautogui
    import cv2
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(f"Error: Faltan dependencias. Ejecuta: pip install pyautogui opencv-python pillow")
    print(f"Error específico: {e}")
    sys.exit(1)

# Importar configuración
try:
    from config import (RECOGNITION_CONFIG, REQUIRED_IMAGES, KEYBOARD_SHORTCUTS, 
                       LOGGING_CONFIG, SECURITY_CONFIG, MESSAGES, REMOTE_DESKTOP_CONFIG, 
                       ACTIVATION_STRATEGIES, ERROR_RECOVERY_CONFIG)
except ImportError:
    print("Error: No se pudo importar config.py")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format'],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['file']),
        logging.StreamHandler()
    ]
)
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

class SAPAutomation:
    """Clase principal para automatización de SAP"""
    
    def __init__(self):
        self.reference_path = Path("reference_images")
        self.confidence = RECOGNITION_CONFIG['confidence']
        self.timeout = RECOGNITION_CONFIG['timeout']
        self.remote_manager = RemoteDesktopManager()
        pyautogui.FAILSAFE = SECURITY_CONFIG['failsafe']
        pyautogui.PAUSE = SECURITY_CONFIG['pause_between_actions']
        
    def find_image_on_screen(self, image_name: str, confidence: float = None) -> Optional[Tuple[int, int]]:
        """
        Busca una imagen en la pantalla
        
        Args:
            image_name: Nombre del archivo de imagen
            confidence: Nivel de confianza (0-1)
            
        Returns:
            Tupla (x, y) de la posición encontrada o None
        """
        if confidence is None:
            confidence = self.confidence
            
        image_path = self.reference_path / image_name
        if not image_path.exists():
            logger.error(f"Imagen no encontrada: {image_path}")
            return None
            
        try:
            location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
            if location:
                center = pyautogui.center(location)
                logger.info(f"Imagen encontrada: {image_name} en {center}")
                return center
            else:
                logger.warning(f"Imagen no encontrada en pantalla: {image_name}")
                return None
        except Exception as e:
            logger.error(f"Error buscando imagen {image_name}: {e}")
            return None
    
    def click_image(self, image_name: str, confidence: float = None) -> bool:
        """
        Busca y hace clic en una imagen
        
        Args:
            image_name: Nombre del archivo de imagen
            confidence: Nivel de confianza
            
        Returns:
            True si se encontró y se hizo clic, False en caso contrario
        """
        position = self.find_image_on_screen(image_name, confidence)
        if position:
            pyautogui.click(position)
            logger.info(f"Clic en: {image_name}")
            return True
        return False
    
    def wait_for_image(self, image_name: str, timeout: int = None) -> Optional[Tuple[int, int]]:
        """
        Espera hasta que aparezca una imagen en pantalla
        
        Args:
            image_name: Nombre del archivo de imagen
            timeout: Tiempo máximo de espera en segundos
            
        Returns:
            Tupla (x, y) de la posición encontrada o None
        """
        if timeout is None:
            timeout = self.timeout
            
        logger.info(f"Esperando imagen: {image_name} (timeout: {timeout}s)")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            position = self.find_image_on_screen(image_name)
            if position:
                return position
            time.sleep(0.5)
            
        logger.error(f"Timeout esperando imagen: {image_name}")
        return None
    
    def maximize_window(self):
        """Maximiza la ventana actual usando Windows + M"""
        logger.info("Maximizando ventana...")
        pyautogui.hotkey(*KEYBOARD_SHORTCUTS['maximize_window'])
        time.sleep(1)
    
    def get_remote_desktop(self) -> bool:
        """
        Método principal para obtener y activar el escritorio remoto
        Implementa múltiples estrategias de recuperación
        """
        logger.info("🚀 Iniciando proceso de conexión al escritorio remoto...")
        
        for attempt in range(self.remote_manager.max_attempts):
            logger.info(f"Intento {attempt + 1}/{self.remote_manager.max_attempts}")
            
            # Paso 1: Encontrar la ventana
            window_info = self.remote_manager.find_remote_desktop_window()
            if not window_info:
                logger.error(f"Intento {attempt + 1}: No se encontró ventana de escritorio remoto")
                if attempt < self.remote_manager.max_attempts - 1:
                    logger.info(f"Esperando {self.remote_manager.retry_delay} segundos antes del siguiente intento...")
                    time.sleep(self.remote_manager.retry_delay)
                continue
            
            # Paso 2: Activar la ventana
            if not self.remote_manager.activate_window_advanced(window_info):
                logger.error(f"Intento {attempt + 1}: No se pudo activar la ventana")
                if attempt < self.remote_manager.max_attempts - 1:
                    logger.info(f"Esperando {self.remote_manager.retry_delay} segundos antes del siguiente intento...")
                    time.sleep(self.remote_manager.retry_delay)
                continue
            
            # Paso 3: Maximizar la ventana
            if not self.remote_manager.maximize_window_advanced():
                logger.warning("No se pudo maximizar la ventana, pero continuando...")
            
            # Paso 4: Verificar que estamos en el escritorio remoto
            if self.verify_remote_desktop_visual():
                logger.info("✅ Escritorio remoto activado y verificado correctamente")
                return True
            else:
                logger.warning(f"Intento {attempt + 1}: Verificación visual falló")
                if attempt < self.remote_manager.max_attempts - 1:
                    logger.info(f"Esperando {self.remote_manager.retry_delay} segundos antes del siguiente intento...")
                    time.sleep(self.remote_manager.retry_delay)
        
        logger.error("❌ No se pudo conectar al escritorio remoto después de todos los intentos")
        return False
    
    def verify_remote_desktop_visual(self) -> bool:
        """Verifica visualmente que estamos en el escritorio remoto"""
        logger.info("🔍 Verificando escritorio remoto visualmente...")
        
        # Buscar imagen de referencia del escritorio remoto
        if self.wait_for_image("remote_desktop.png", timeout=REMOTE_DESKTOP_CONFIG['visual_verification_timeout']):
            logger.info("✅ Escritorio remoto verificado visualmente")
            return True
        
        logger.warning("⚠️ No se pudo verificar visualmente el escritorio remoto")
        return False
    
    def verify_sap_desktop(self):
        """Verifica que estamos en SAP Desktop"""
        logger.info("Verificando SAP Desktop...")
        if self.wait_for_image("sap_desktop.png"):
            logger.info("SAP Desktop detectado correctamente")
            return True
        logger.error("SAP Desktop no detectado")
        return False
    
    def open_modules_menu(self):
        """Abre el menú de módulos usando Alt+M"""
        logger.info("Abriendo menú de módulos...")
        pyautogui.hotkey(*KEYBOARD_SHORTCUTS['open_modules'])
        time.sleep(1)
        
        # Verificar que el menú se abrió
        if self.wait_for_image("sap_modulos_menu.png"):
            logger.info("Menú de módulos abierto correctamente")
            return True
        return False
    
    def navigate_to_sales(self):
        """Navega a la sección de ventas"""
        logger.info("Navegando a ventas...")
        pyautogui.press(KEYBOARD_SHORTCUTS['navigate_sales'])
        time.sleep(1)
        
        # Verificar que estamos en el menú de ventas
        if self.wait_for_image("sap_ventas_order_menu.png"):
            logger.info("Menú de ventas abierto correctamente")
            return True
        return False
    
    def open_sales_order(self):
        """Abre la orden de venta"""
        logger.info("Abriendo orden de venta...")
        if self.click_image("sap_ventas_order_button.png"):
            time.sleep(2)
            return True
        return False
    
    def verify_sales_order_form(self):
        """Verifica que estamos en el formulario de orden de venta"""
        logger.info("Verificando formulario de orden de venta...")
        if self.wait_for_image("sap_orden_de_ventas_template.png"):
            logger.info("Formulario de orden de venta abierto correctamente")
            return True
        logger.error("Formulario de orden de venta no detectado")
        return False
    
    def run_automation(self):
        """Ejecuta el proceso completo de automatización"""
        logger.info("Iniciando automatización de SAP...")
        
        try:
            # Paso 1: Obtener el escritorio remoto
            if not self.get_remote_desktop():
                logger.error("No se pudo conectar al escritorio remoto")
                return False
            
            # Paso 2: Verificar SAP Desktop
            if not self.verify_sap_desktop():
                logger.error("No se detectó SAP Desktop")
                return False
            
            # Paso 3: Maximizar ventana
            self.maximize_window()
            
            # Paso 4: Abrir menú de módulos
            if not self.open_modules_menu():
                logger.error("No se pudo abrir el menú de módulos")
                return False
            
            # Paso 5: Navegar a ventas
            if not self.navigate_to_sales():
                logger.error("No se pudo navegar a ventas")
                return False
            
            # Paso 6: Abrir orden de venta
            if not self.open_sales_order():
                logger.error("No se pudo abrir la orden de venta")
                return False
            
            # Paso 7: Verificar formulario
            if not self.verify_sales_order_form():
                logger.error("No se pudo verificar el formulario de orden de venta")
                return False
            
            logger.info("¡Automatización completada exitosamente!")
            return True
            
        except Exception as e:
            logger.error(f"Error durante la automatización: {e}")
            return False

def main():
    """Función principal"""
    print(MESSAGES['welcome'])
    
    # Crear instancia de automatización
    automation = SAPAutomation()
    
    # Verificar que las imágenes de referencia existen
    missing_images = []
    for image in REQUIRED_IMAGES:
        if not (automation.reference_path / image).exists():
            missing_images.append(image)
    
    if missing_images:
        print("Error: Faltan las siguientes imágenes de referencia:")
        for image in missing_images:
            print(f"  - {image}")
        print("\nAsegúrate de que todas las imágenes estén en la carpeta 'reference_images'")
        return
    
    print("Imágenes de referencia verificadas correctamente")
    print()
    
    # Confirmar inicio
    input("Presiona Enter para iniciar la automatización...")
    print()
    
    # Ejecutar automatización
    success = automation.run_automation()
    
    if success:
        print(f"\n{MESSAGES['success']}")
        print(MESSAGES['ready'])
    else:
        print(f"\n{MESSAGES['error']}")
        print(MESSAGES['check_log'])
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
