#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Capturas de Pantalla - OrderLoader 2.0
Maneja la toma de capturas de pantalla de SAP
"""

import os
import time
import logging
from datetime import datetime
from typing import Optional

import pyautogui
from PIL import Image

from .remote_desktop_manager import RemoteDesktopManager
from ..config import SECURITY_CONFIG

logger = logging.getLogger(__name__)

class ScreenshotManager:
    """Gestor especializado para capturas de pantalla de SAP"""
    
    def __init__(self):
        self.remote_desktop_manager = RemoteDesktopManager()
        self.screenshots_dir = "assets/screenshots"
        self._ensure_screenshots_directory()
        
    def _ensure_screenshots_directory(self):
        """Asegura que el directorio de capturas de pantalla existe"""
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
            logger.info(f"📁 Directorio de capturas creado: {self.screenshots_dir}")
    
    def take_sap_screenshot(self, filename: Optional[str] = None) -> Optional[str]:
        """
        Toma una captura de pantalla de SAP
        
        Args:
            filename: Nombre del archivo (opcional). Si no se proporciona, se genera automáticamente
            
        Returns:
            Ruta del archivo de captura guardado o None si falla
        """
        logger.info("📸 Iniciando captura de pantalla de SAP...")
        
        try:
            # Paso 1: Encontrar y activar el escritorio remoto
            logger.info("🔄 Buscando ventana del escritorio remoto...")
            window_info = self.remote_desktop_manager.find_remote_desktop_window()
            
            if not window_info:
                logger.error("❌ No se encontró la ventana del escritorio remoto")
                return None
            
            # Paso 2: Activar la ventana usando Alt+Tab
            logger.info("🔄 Activando escritorio remoto con Alt+Tab...")
            for attempt in range(5):  # Intentar hasta 5 veces
                pyautogui.hotkey('alt', 'tab')
                time.sleep(SECURITY_CONFIG['pause_between_actions'])
                
                # Verificar si la ventana está activa
                current_title = self.remote_desktop_manager.get_active_window_title()
                if current_title and window_info['MainWindowTitle'] in current_title:
                    logger.info("✅ Escritorio remoto activado correctamente")
                    break
            else:
                logger.warning("⚠️ No se pudo activar con Alt+Tab, intentando estrategias avanzadas...")
                if not self.remote_desktop_manager.activate_window_advanced(window_info):
                    logger.error("❌ No se pudo activar el escritorio remoto")
                    return None
            
            # Paso 3: Maximizar la ventana
            logger.info("🔄 Maximizando ventana...")
            if not self.remote_desktop_manager.maximize_window_advanced():
                logger.warning("⚠️ No se pudo maximizar la ventana, continuando...")
            
            # Paso 4: Esperar un momento para que la ventana se estabilice
            time.sleep(2)
            
            # Paso 5: Tomar la captura de pantalla
            logger.info("📸 Tomando captura de pantalla...")
            screenshot = pyautogui.screenshot()
            
            # Paso 6: Generar nombre de archivo
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sap_screenshot_{timestamp}.png"
            
            # Asegurar que el archivo tenga extensión .png
            if not filename.lower().endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # Paso 7: Guardar la captura
            screenshot.save(filepath)
            logger.info(f"✅ Captura guardada exitosamente: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Error al tomar captura de pantalla: {e}")
            return None
    
    def take_multiple_screenshots(self, count: int = 3, delay: float = 2.0) -> list:
        """
        Toma múltiples capturas de pantalla con un delay entre ellas
        
        Args:
            count: Número de capturas a tomar
            delay: Delay en segundos entre capturas
            
        Returns:
            Lista de rutas de archivos guardados
        """
        logger.info(f"📸 Tomando {count} capturas de pantalla...")
        
        saved_files = []
        
        for i in range(count):
            logger.info(f"📸 Captura {i+1}/{count}")
            
            filename = f"sap_screenshot_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i+1}.png"
            filepath = self.take_sap_screenshot(filename)
            
            if filepath:
                saved_files.append(filepath)
            
            # Esperar antes de la siguiente captura (excepto en la última)
            if i < count - 1:
                time.sleep(delay)
        
        logger.info(f"✅ Proceso completado. {len(saved_files)}/{count} capturas guardadas")
        return saved_files
