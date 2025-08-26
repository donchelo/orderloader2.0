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

from ..config import RECOGNITION_CONFIG

logger = logging.getLogger(__name__)

class ImageRecognition:
    """Clase para manejo de reconocimiento de imágenes"""
    
    def __init__(self, reference_path: Path = None):
        self.reference_path = reference_path or Path("reference_images")
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
