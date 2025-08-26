#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatización de SAP - OrderLoader 2.0
Clase principal para la automatización de procesos en SAP
"""

import time
import logging
from pathlib import Path

import pyautogui

from .remote_desktop_manager import RemoteDesktopManager
from .image_recognition import ImageRecognition
from ..config import (RECOGNITION_CONFIG, REQUIRED_IMAGES, KEYBOARD_SHORTCUTS, 
                     SECURITY_CONFIG, REMOTE_DESKTOP_CONFIG)

logger = logging.getLogger(__name__)

class SAPAutomation:
    """Clase principal para automatización de SAP"""
    
    def __init__(self, reference_path: Path = None):
        self.reference_path = reference_path or Path("reference_images")
        self.confidence = RECOGNITION_CONFIG['confidence']
        self.timeout = RECOGNITION_CONFIG['timeout']
        self.remote_manager = RemoteDesktopManager()
        self.image_recognition = ImageRecognition(self.reference_path)
        
        # Configurar pyautogui
        pyautogui.FAILSAFE = SECURITY_CONFIG['failsafe']
        pyautogui.PAUSE = SECURITY_CONFIG['pause_between_actions']
        
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
        if self.image_recognition.wait_for_image("remote_desktop.png", 
                                               timeout=REMOTE_DESKTOP_CONFIG['visual_verification_timeout']):
            logger.info("✅ Escritorio remoto verificado visualmente")
            return True
        
        logger.warning("⚠️ No se pudo verificar visualmente el escritorio remoto")
        return False
    
    def verify_sap_desktop(self) -> bool:
        """Verifica que estamos en SAP Desktop"""
        logger.info("Verificando SAP Desktop...")
        if self.image_recognition.wait_for_image("sap_desktop.png"):
            logger.info("SAP Desktop detectado correctamente")
            return True
        logger.error("SAP Desktop no detectado")
        return False
    
    def maximize_window(self) -> bool:
        """Maximiza la ventana actual usando Windows + Up"""
        logger.info("Maximizando ventana...")
        try:
            pyautogui.hotkey(*KEYBOARD_SHORTCUTS['maximize_window'])
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"Error maximizando ventana: {e}")
            return False
    
    def open_modules_menu(self) -> bool:
        """Abre el menú de módulos usando Alt+M"""
        logger.info("Abriendo menú de módulos...")
        try:
            pyautogui.hotkey(*KEYBOARD_SHORTCUTS['open_modules'])
            time.sleep(1)
            
            # Verificar que el menú se abrió
            if self.image_recognition.wait_for_image("sap_modulos_menu.png"):
                logger.info("Menú de módulos abierto correctamente")
                return True
            return False
        except Exception as e:
            logger.error(f"Error abriendo menú de módulos: {e}")
            return False
    
    def navigate_to_sales(self) -> bool:
        """Navega a la sección de ventas"""
        logger.info("Navegando a ventas...")
        try:
            pyautogui.press(KEYBOARD_SHORTCUTS['navigate_sales'])
            time.sleep(1)
            
            # Verificar que estamos en el menú de ventas
            if self.image_recognition.wait_for_image("sap_ventas_order_menu.png"):
                logger.info("Menú de ventas abierto correctamente")
                return True
            return False
        except Exception as e:
            logger.error(f"Error navegando a ventas: {e}")
            return False
    
    def open_sales_order(self) -> bool:
        """Abre la orden de venta"""
        logger.info("Abriendo orden de venta...")
        if self.image_recognition.click_image("sap_ventas_order_button.png"):
            time.sleep(2)
            return True
        return False
    
    def verify_sales_order_form(self) -> bool:
        """Verifica que estamos en el formulario de orden de venta"""
        logger.info("Verificando formulario de orden de venta...")
        if self.image_recognition.wait_for_image("sap_orden_de_ventas_template.png"):
            logger.info("Formulario de orden de venta abierto correctamente")
            return True
        logger.error("Formulario de orden de venta no detectado")
        return False
    
    def verify_required_images(self) -> list:
        """
        Verifica que todas las imágenes de referencia existen
        
        Returns:
            Lista de imágenes faltantes
        """
        missing_images = []
        for image in REQUIRED_IMAGES:
            if not self.image_recognition.verify_image_exists(image):
                missing_images.append(image)
        return missing_images
    
    def run_automation(self) -> bool:
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
            if not self.maximize_window():
                logger.warning("No se pudo maximizar la ventana, pero continuando...")
            
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
