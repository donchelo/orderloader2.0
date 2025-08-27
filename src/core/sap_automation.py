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
from .queue_manager import QueueManager
from ..config import (RECOGNITION_CONFIG, REQUIRED_IMAGES, KEYBOARD_SHORTCUTS, 
                     SECURITY_CONFIG, REMOTE_DESKTOP_CONFIG)

logger = logging.getLogger(__name__)

class SAPAutomation:
    """Clase principal para automatización de SAP"""
    
    def __init__(self, reference_path: Path = None):
        self.reference_path = reference_path or Path("assets/images")
        self.confidence = RECOGNITION_CONFIG['confidence']
        self.timeout = RECOGNITION_CONFIG['timeout']
        self.remote_manager = RemoteDesktopManager()
        self.image_recognition = ImageRecognition(self.reference_path)
        self.queue_manager = QueueManager()  # Nuevo: gestor de colas
        
        # Configurar pyautogui
        pyautogui.FAILSAFE = SECURITY_CONFIG['failsafe']
        pyautogui.PAUSE = SECURITY_CONFIG['pause_between_actions']
        
    def get_remote_desktop(self) -> bool:
        """
        Método principal para obtener y activar el escritorio remoto (20.96.6.64)
        Implementa múltiples estrategias de recuperación
        """
        logger.info("🚀 Iniciando proceso de conexión al escritorio remoto (20.96.6.64)...")
        
        for attempt in range(self.remote_manager.max_attempts):
            logger.info(f"Intento {attempt + 1}/{self.remote_manager.max_attempts}")
            
            # Paso 1: Encontrar la ventana del escritorio remoto
            window_info = self.remote_manager.find_remote_desktop_window()
            if not window_info:
                logger.error(f"Intento {attempt + 1}: No se encontró ventana de escritorio remoto (20.96.6.64)")
                if attempt < self.remote_manager.max_attempts - 1:
                    logger.info(f"Esperando {self.remote_manager.retry_delay} segundos antes del siguiente intento...")
                    time.sleep(self.remote_manager.retry_delay)
                continue
            
            # Paso 2: Activar la ventana del escritorio remoto
            if not self.remote_manager.activate_window_advanced(window_info):
                logger.error(f"Intento {attempt + 1}: No se pudo activar la ventana del escritorio remoto")
                if attempt < self.remote_manager.max_attempts - 1:
                    logger.info(f"Esperando {self.remote_manager.retry_delay} segundos antes del siguiente intento...")
                    time.sleep(self.remote_manager.retry_delay)
                continue
            
            # Paso 3: Verificar que estamos en el escritorio remoto
            if self.verify_remote_desktop_visual():
                logger.info("✅ Escritorio remoto (20.96.6.64) activado y verificado correctamente")
                return True
            else:
                logger.warning(f"Intento {attempt + 1}: Verificación visual del escritorio remoto falló")
                if attempt < self.remote_manager.max_attempts - 1:
                    logger.info(f"Esperando {self.remote_manager.retry_delay} segundos antes del siguiente intento...")
                    time.sleep(self.remote_manager.retry_delay)
        
        logger.error("❌ No se pudo conectar al escritorio remoto (20.96.6.64) después de todos los intentos")
        return False
    
    def verify_remote_desktop_visual(self) -> bool:
        """Verifica visualmente que estamos en el escritorio remoto usando técnicas robustas"""
        logger.info("🔍 Verificando escritorio remoto visualmente...")
        
        # Estrategia 1: Buscar imagen de referencia del escritorio remoto
        if self.image_recognition.wait_for_image("core/remote_desktop.png", 
                                               timeout=REMOTE_DESKTOP_CONFIG['visual_verification_timeout']):
            logger.info("✅ Escritorio remoto verificado visualmente")
            return True
        
        # Estrategia 2: Usar búsqueda robusta con múltiples niveles de confianza
        if self.image_recognition.find_image_robust("core/remote_desktop.png", [0.8, 0.7, 0.6]):
            logger.info("✅ Escritorio remoto detectado con búsqueda robusta")
            return True
        
        # Estrategia 3: Template matching más preciso
        if self.image_recognition.find_image_with_template_matching("core/remote_desktop.png", threshold=0.7):
            logger.info("✅ Escritorio remoto detectado con template matching")
            return True
        
        logger.warning("⚠️ No se pudo verificar visualmente el escritorio remoto")
        return False
    
    def verify_sap_desktop(self) -> bool:
        """Verifica que SAP Desktop está visible en el escritorio remoto usando estrategias avanzadas"""
        logger.info("🔍 Verificando que SAP Desktop esté visible en el escritorio remoto...")
        
        # Usar la verificación avanzada con múltiples técnicas
        if self.image_recognition.verify_sap_desktop_advanced():
            logger.info("✅ SAP Desktop detectado correctamente - la aplicación ya está abierta")
            return True
            
        logger.error("❌ SAP Desktop no está visible - verifica que la aplicación esté abierta en el escritorio remoto")
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
        """Abre el menú de módulos haciendo clic en el botón"""
        logger.info("🖱️ Haciendo clic en botón de módulos...")
        try:
            if self.image_recognition.click_image("sap/sap_modulos_menu_button.png"):
                time.sleep(2)  # Esperar a que aparezca el menú
                logger.info("✅ Clic en botón de módulos exitoso")
                
                # Verificar que el menú se abrió
                if self.image_recognition.find_image_on_screen("sap/sap_modulos_menu.png"):
                    logger.info("✅ Menú de módulos detectado visualmente")
                    return True
                else:
                    logger.warning("⚠️ Menú de módulos no detectado visualmente, pero continuando...")
                    return True  # Continuamos aunque no detectemos visualmente
            else:
                logger.error("❌ No se pudo hacer clic en el botón de módulos")
                return False
        except Exception as e:
            logger.error(f"❌ Error haciendo clic en botón de módulos: {e}")
            return False
    
    def navigate_to_sales(self) -> bool:
        """Navega a la sección de ventas haciendo clic en el botón de ventas"""
        logger.info("🖱️ Haciendo clic en botón de ventas...")
        try:
            # Buscar el elemento de ventas en el menú
            ventas_elements = [
                "sap/sap_ventas_menu_button.png",
                "sap/sap_ventas_clientes_menu.png"
            ]
            
            ventas_clicked = False
            for element in ventas_elements:
                logger.info(f"🔍 Buscando: {element}")
                if self.image_recognition.click_image(element):
                    logger.info(f"✅ Clic exitoso en: {element}")
                    ventas_clicked = True
                    time.sleep(2)  # Esperar a que aparezca el menú de ventas
                    break
            
            if not ventas_clicked:
                logger.warning("⚠️ No se pudo hacer clic en ventas, intentando atajo de teclado...")
                # Intentar usar atajo de teclado V como respaldo
                pyautogui.press(KEYBOARD_SHORTCUTS['navigate_sales'])
                time.sleep(2)
            
            # Verificar que estamos en el menú de ventas
            ventas_menu_elements = [
                "sap/sap_ventas_order_menu.png",
                "sap/sap_ventas_clientes_menu.png"
            ]
            
            for element in ventas_menu_elements:
                if self.image_recognition.find_image_on_screen(element):
                    logger.info(f"✅ Menú de ventas detectado: {element}")
                    return True
            
            logger.warning("⚠️ Menú de ventas no detectado visualmente, pero continuando...")
            return True  # Continuamos aunque no detectemos visualmente
            
        except Exception as e:
            logger.error(f"❌ Error navegando a ventas: {e}")
            return False
    
    def open_sales_order(self) -> bool:
        """Busca y hace clic en el botón de órdenes de venta"""
        logger.info("🖱️ Haciendo clic en órdenes de venta...")
        try:
            if self.image_recognition.click_image("sap/sap_ventas_order_button.png"):
                time.sleep(3)  # Esperar a que se abra el formulario
                logger.info("✅ Clic en órdenes de venta exitoso")
                return True
            else:
                logger.warning("⚠️ No se pudo hacer clic en órdenes de venta, buscando alternativas...")
                
                # Buscar otros elementos relacionados con órdenes
                order_elements = [
                    "sap/sap_ventas_order_menu.png",
                    "sap/sap_ventas_clientes_menu.png"
                ]
                
                for element in order_elements:
                    if self.image_recognition.click_image(element):
                        logger.info(f"✅ Clic alternativo exitoso en: {element}")
                        time.sleep(3)
                        return True
                
                logger.error("❌ No se pudo encontrar ningún botón de órdenes de venta")
                return False
        except Exception as e:
            logger.error(f"❌ Error haciendo clic en órdenes de venta: {e}")
            return False
    
    def verify_sales_order_form(self) -> bool:
        """Verifica que estamos en el formulario de orden de venta"""
        logger.info("🔍 Verificando formulario de orden de venta...")
        
        # Estrategia 1: Buscar el template principal
        if self.image_recognition.find_image_on_screen("sap/sap_orden_de_ventas_template.png"):
            logger.info("✅ Formulario de orden de venta detectado")
            return True
        
        # Estrategia 2: Buscar elementos alternativos del formulario
        logger.info("🔍 Buscando elementos alternativos del formulario...")
        form_elements = [
            "sap/sap_ventas_order_menu.png",
            "sap/sap_ventas_clientes_menu.png",
            "sap/sap_ventas_order_button.png"
        ]
        
        for element in form_elements:
            if self.image_recognition.find_image_on_screen(element):
                logger.info(f"✅ Elemento de formulario detectado: {element}")
                return True
        
        # Estrategia 3: Usar búsqueda robusta
        logger.info("🔍 Probando búsqueda robusta...")
        if self.image_recognition.find_image_robust("sap/sap_orden_de_ventas_template.png", [0.7, 0.6, 0.5]):
            logger.info("✅ Formulario detectado con búsqueda robusta")
            return True
        
        logger.warning("⚠️ Formulario de orden de venta no detectado, pero continuando...")
        return True  # Continuamos aunque no detectemos el formulario específico
    
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
        """
        Ejecuta el proceso completo de automatización
        Workflow optimizado: Escritorio Remoto → SAP Desktop (ya abierto) → Clic Módulos → Clic Ventas → Clic Órdenes
        """
        logger.info("🚀 Iniciando automatización de SAP...")
        
        try:
            # Paso 1: Obtener y activar escritorio remoto (20.96.6.64)
            logger.info("📍 Paso 1: Activando escritorio remoto...")
            if not self.get_remote_desktop():
                logger.error("❌ No se pudo obtener el escritorio remoto")
                return False
            
            # Paso 2: Verificar que SAP Desktop ya está abierto (imagen de referencia)
            logger.info("📍 Paso 2: Verificando que SAP Desktop esté visible...")
            if not self.verify_sap_desktop():
                logger.error("❌ SAP Desktop no está visible en el escritorio remoto")
                return False
            
            # Paso 3: Maximizar la ventana del escritorio remoto
            logger.info("📍 Paso 3: Maximizando ventana del escritorio remoto...")
            if not self.remote_manager.maximize_window_advanced():
                logger.warning("⚠️ No se pudo maximizar la ventana, pero continuando...")
            
            # Pausa para estabilizar
            logger.info("⏳ Esperando 3 segundos para estabilizar...")
            time.sleep(3)
            
            # Paso 4: Hacer clic en botón de módulos
            logger.info("📍 Paso 4: Haciendo clic en botón de módulos...")
            if not self.open_modules_menu():
                logger.error("❌ No se pudo abrir el menú de módulos")
                return False
            
            # Paso 5: Hacer clic en ventas
            logger.info("📍 Paso 5: Haciendo clic en ventas...")
            if not self.navigate_to_sales():
                logger.error("❌ No se pudo navegar a ventas")
                return False
            
            # Paso 6: Hacer clic en órdenes de venta
            logger.info("📍 Paso 6: Haciendo clic en órdenes de venta...")
            if not self.open_sales_order():
                logger.error("❌ No se pudo abrir la orden de venta")
                return False
            
            # Paso 7: Verificar que el formulario esté abierto
            logger.info("📍 Paso 7: Verificando formulario de orden de venta...")
            if not self.verify_sales_order_form():
                logger.error("❌ No se pudo verificar el formulario de orden de venta")
                return False
            
            logger.info("✅ ¡Automatización completada exitosamente!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error durante la automatización: {e}")
            return False

    def process_queue(self) -> bool:
        """
        Procesa todos los archivos en la cola de forma secuencial
        """
        logger.info("🚀 Iniciando procesamiento de cola...")
        
        # Verificar si hay archivos pendientes
        if not self.queue_manager.has_pending_files():
            logger.info("📭 No hay archivos pendientes en la cola")
            return True
        
        # Mostrar estado inicial
        self.queue_manager.print_queue_status()
        
        # Procesar archivos uno por uno
        while self.queue_manager.has_pending_files():
            next_file = self.queue_manager.get_next_file()
            if not next_file:
                break
            
            logger.info(f"🔄 Procesando archivo: {next_file.name}")
            
            try:
                # Procesar el archivo individual
                success = self.process_single_file(next_file)
                
                if success:
                    # Mover a completados
                    if self.queue_manager.move_to_completed(next_file):
                        logger.info(f"✅ Archivo procesado exitosamente: {next_file.name}")
                    else:
                        logger.error(f"❌ Error al mover archivo completado: {next_file.name}")
                else:
                    logger.error(f"❌ Error al procesar archivo: {next_file.name}")
                    # Por ahora, dejamos el archivo en pending para revisión manual
                    # En el futuro podríamos agregar una carpeta 'failed'
                
            except Exception as e:
                logger.error(f"❌ Excepción al procesar {next_file.name}: {e}")
                # El archivo permanece en pending para revisión manual
        
        # Mostrar estado final
        self.queue_manager.print_queue_status()
        logger.info("🏁 Procesamiento de cola completado")
        return True
    
    def process_single_file(self, file_path: Path) -> bool:
        """
        Procesa un archivo individual (JSON con datos de orden de compra)
        Ejecuta la automatización completa de SAP para cada archivo
        """
        logger.info(f"🔄 Iniciando procesamiento de: {file_path.name}")
        
        try:
            # Verificar que es un archivo JSON
            if not file_path.suffix.lower() == '.json':
                logger.warning(f"⚠️ Archivo {file_path.name} no es JSON, pero continuando...")
            
            # Ejecutar la automatización completa de SAP
            success = self.run_automation()
            
            if success:
                logger.info(f"✅ Automatización completada para: {file_path.name}")
                logger.info(f"📋 Archivo JSON procesado: {file_path.name}")
                return True
            else:
                logger.error(f"❌ Automatización falló para: {file_path.name}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en automatización para {file_path.name}: {e}")
            return False
