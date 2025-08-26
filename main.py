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
from pathlib import Path
from typing import Optional, Tuple

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
    from config import RECOGNITION_CONFIG, REQUIRED_IMAGES, KEYBOARD_SHORTCUTS, LOGGING_CONFIG, SECURITY_CONFIG, MESSAGES
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

class SAPAutomation:
    """Clase principal para automatización de SAP"""
    
    def __init__(self):
        self.reference_path = Path("reference_images")
        self.confidence = RECOGNITION_CONFIG['confidence']
        self.timeout = RECOGNITION_CONFIG['timeout']
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
    
    def check_remote_desktop_running(self):
        """Verifica que el escritorio remoto esté ejecutándose"""
        logger.info("Verificando escritorio remoto...")
        
        try:
            import subprocess
            result = subprocess.run(['powershell', '-Command', 
                'Get-Process | Where-Object {$_.ProcessName -like "*mstsc*"} | Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'], 
                capture_output=True, text=True)
            
            if result.stdout and result.stdout.strip() != '':
                import json
                try:
                    windows = json.loads(result.stdout)
                    if not isinstance(windows, list):
                        windows = [windows]
                    
                    for window in windows:
                        title = window.get('MainWindowTitle', '')
                        process = window.get('ProcessName', '')
                        process_id = window.get('Id', '')
                        
                        logger.info(f"Escritorio remoto encontrado: {title} (ID: {process_id})")
                        return True
                        
                except json.JSONDecodeError:
                    logger.warning("Error parseando información de ventanas")
            
            logger.error("No se encontró escritorio remoto ejecutándose")
            return False
            
        except Exception as e:
            logger.error(f"Error verificando escritorio remoto: {e}")
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
            # Paso 1: Verificar que el escritorio remoto esté ejecutándose
            if not self.check_remote_desktop_running():
                logger.error("No se detectó escritorio remoto ejecutándose")
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
