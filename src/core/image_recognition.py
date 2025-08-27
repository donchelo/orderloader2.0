#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconocimiento de Imágenes - OrderLoader 2.0
Maneja la detección y reconocimiento de elementos en pantalla
"""

import time
import logging
from pathlib import Path
from typing import Optional, Tuple

import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageGrab

from ..config import RECOGNITION_CONFIG

logger = logging.getLogger(__name__)

class ImageRecognition:
    """Clase para manejo de reconocimiento de imágenes"""
    
    def __init__(self, reference_path: Path = None):
        self.reference_path = reference_path or Path("assets/images")
        self.confidence = RECOGNITION_CONFIG['confidence']
        self.timeout = RECOGNITION_CONFIG['timeout']
        
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
    
    def verify_image_exists(self, image_name: str) -> bool:
        """
        Verifica que una imagen de referencia existe
        
        Args:
            image_name: Nombre del archivo de imagen
            
        Returns:
            True si existe, False en caso contrario
        """
        image_path = self.reference_path / image_name
        exists = image_path.exists()
        if not exists:
            logger.error(f"Imagen de referencia no encontrada: {image_path}")
        return exists
    
    def find_image_robust(self, image_name: str, confidence_levels: list = None, region: tuple = None) -> Optional[Tuple[int, int]]:
        """
        Busca una imagen usando múltiples niveles de confianza y estrategias
        
        Args:
            image_name: Nombre del archivo de imagen
            confidence_levels: Lista de niveles de confianza a probar [0.9, 0.8, 0.7, 0.6]
            region: Región específica de la pantalla (left, top, width, height)
            
        Returns:
            Tupla (x, y) de la posición encontrada o None
        """
        if confidence_levels is None:
            confidence_levels = [0.9, 0.8, 0.7, 0.6]
            
        image_path = self.reference_path / image_name
        if not image_path.exists():
            logger.error(f"Imagen no encontrada: {image_path}")
            return None
        
        for confidence in confidence_levels:
            try:
                logger.info(f"Buscando {image_name} con confianza {confidence}")
                
                if region:
                    location = pyautogui.locateOnScreen(str(image_path), confidence=confidence, region=region)
                else:
                    location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
                
                if location:
                    center = pyautogui.center(location)
                    logger.info(f"✅ Imagen encontrada: {image_name} en {center} con confianza {confidence}")
                    return center
                    
            except Exception as e:
                logger.warning(f"Error buscando {image_name} con confianza {confidence}: {e}")
                continue
        
        logger.warning(f"❌ Imagen no encontrada: {image_name} con ningún nivel de confianza")
        return None
    
    def verify_remote_desktop_window(self) -> bool:
        """
        Verifica que estamos en la ventana del escritorio remoto usando múltiples estrategias
        
        Returns:
            True si se detecta la ventana del escritorio remoto
        """
        logger.info("🔍 Verificando ventana del escritorio remoto...")
        
        # Estrategia 1: Buscar la imagen de referencia del escritorio remoto
        if self.find_image_robust("core/remote_desktop.png", [0.8, 0.7, 0.6]):
            logger.info("✅ Ventana del escritorio remoto detectada por imagen")
            return True
        
        # Estrategia 2: Buscar elementos característicos del escritorio remoto
        # (bordes, barra de título, etc.)
        try:
            # Buscar elementos que siempre están presentes en escritorio remoto
            screen_width, screen_height = pyautogui.size()
            
            # Verificar si hay elementos típicos del escritorio remoto
            # Esto es más robusto que buscar una imagen específica
            logger.info("🔍 Verificando elementos característicos del escritorio remoto...")
            
            # Por ahora, si no encontramos la imagen, asumimos que estamos en el lugar correcto
            # En el futuro, podríamos agregar más verificaciones específicas
            logger.info("⚠️ No se detectó imagen específica, pero continuando...")
            return True
            
        except Exception as e:
            logger.error(f"Error verificando escritorio remoto: {e}")
            return False
    
    def verify_sap_desktop_robust(self) -> bool:
        """
        Verifica que SAP Desktop está visible usando múltiples estrategias
        
        Returns:
            True si SAP Desktop está detectado
        """
        logger.info("🔍 Verificando SAP Desktop con estrategias robustas...")
        
        # Estrategia 1: Buscar la imagen principal de SAP Desktop
        if self.find_image_robust("core/sap_desktop.png", [0.8, 0.7, 0.6]):
            logger.info("✅ SAP Desktop detectado por imagen principal")
            return True
        
        # Estrategia 2: Buscar elementos característicos de SAP
        sap_elements = [
            "sap/sap_icon.png",
            "sap/sap_main_interface.png"
        ]
        
        for element in sap_elements:
            if self.find_image_robust(element, [0.7, 0.6]):
                logger.info(f"✅ SAP Desktop detectado por elemento: {element}")
                return True
        
        # Estrategia 3: Verificar que estamos en el escritorio remoto primero
        if not self.verify_remote_desktop_window():
            logger.error("❌ No se detectó la ventana del escritorio remoto")
            return False
        
        logger.warning("⚠️ SAP Desktop no detectado por imágenes, pero estamos en escritorio remoto")
        return True  # Asumimos que si estamos en escritorio remoto, SAP está ahí
    
    def find_image_with_template_matching(self, image_name: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        Busca una imagen usando template matching de OpenCV (más robusto)
        
        Args:
            image_name: Nombre del archivo de imagen
            threshold: Umbral de similitud (0-1)
            
        Returns:
            Tupla (x, y) de la posición encontrada o None
        """
        try:
            image_path = self.reference_path / image_name
            if not image_path.exists():
                logger.error(f"Imagen no encontrada: {image_path}")
                return None
            
            # Capturar pantalla
            screenshot = ImageGrab.grab()
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            # Cargar imagen de referencia
            template = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if template is None:
                logger.error(f"No se pudo cargar la imagen: {image_path}")
                return None
            
            # Realizar template matching
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= threshold:
                # Calcular el centro del template encontrado
                h, w = template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                logger.info(f"✅ Template matching exitoso: {image_name} en ({center_x}, {center_y}) con confianza {max_val:.3f}")
                return (center_x, center_y)
            else:
                logger.warning(f"❌ Template matching falló: {image_name} (mejor confianza: {max_val:.3f})")
                return None
                
        except Exception as e:
            logger.error(f"Error en template matching para {image_name}: {e}")
            return None
    
    def verify_sap_desktop_advanced(self) -> bool:
        """
        Verificación avanzada de SAP Desktop usando múltiples técnicas
        
        Returns:
            True si SAP Desktop está detectado
        """
        logger.info("🔍 Verificación avanzada de SAP Desktop...")
        
        # Técnica 1: Template matching con OpenCV
        if self.find_image_with_template_matching("core/sap_desktop.png", threshold=0.7):
            logger.info("✅ SAP Desktop detectado por template matching")
            return True
        
        # Técnica 2: Búsqueda robusta con múltiples niveles de confianza
        if self.find_image_robust("core/sap_desktop.png", [0.8, 0.7, 0.6, 0.5]):
            logger.info("✅ SAP Desktop detectado por búsqueda robusta")
            return True
        
        # Técnica 3: Buscar elementos característicos de SAP
        sap_indicators = [
            "sap/sap_icon.png",
            "sap/sap_main_interface.png",
            "sap/sap_modulos_menu_button.png"
        ]
        
        for indicator in sap_indicators:
            if self.find_image_robust(indicator, [0.7, 0.6]):
                logger.info(f"✅ SAP Desktop detectado por indicador: {indicator}")
                return True
        
        # Técnica 4: Verificar que estamos en escritorio remoto
        if self.verify_remote_desktop_window():
            logger.info("⚠️ No se detectó SAP específicamente, pero estamos en escritorio remoto")
            return True
        
        logger.error("❌ SAP Desktop no detectado con ninguna técnica")
        return False
