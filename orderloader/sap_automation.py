#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAP Automation - Computer Vision Module
Automatización de SAP Business One usando pyautogui
"""

import time
import pyautogui
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import logging


class SAPAutomation:
    """
    Automatización de SAP Business One con Computer Vision.

    Utiliza pyautogui para detectar elementos visuales en pantalla
    y automatizar la interacción con SAP.
    """

    def __init__(self, logger: logging.Logger, assets_path: Path, simulation_mode: bool = False):
        """
        Inicializar automatización SAP.

        Args:
            logger: Logger para registro de eventos
            assets_path: Ruta a las imágenes de referencia
            simulation_mode: Si True, simula acciones sin ejecutarlas
        """
        self.logger = logger
        self.assets_path = assets_path
        self.simulation_mode = simulation_mode
        self.confidence = 0.8  # Confidence por defecto
        self.timeout = 10  # Timeout por defecto

        # Configurar pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5

        self.logger.info(f"🤖 SAPAutomation inicializado (Simulación: {simulation_mode})")

    def find_and_click(self, image_name: str, confidence: float = 0.8,
                       timeout: int = 10, region: Optional[Tuple] = None) -> bool:
        """
        Buscar imagen en pantalla y hacer clic.

        Args:
            image_name: Nombre del archivo de imagen relativo a assets_path
            confidence: Nivel de confianza de detección (0.0 - 1.0)
            timeout: Tiempo máximo de búsqueda en segundos
            region: Región de búsqueda (x, y, width, height) opcional

        Returns:
            bool: True si encontró y hizo clic exitosamente
        """
        image_path = self.assets_path / image_name

        # Validar que la imagen existe
        if not image_path.exists():
            self.logger.error(f"❌ Imagen no encontrada: {image_path}")
            return False

        # Modo simulación
        if self.simulation_mode:
            self.logger.info(f"🎭 [SIMULACIÓN] Click en {image_name}")
            time.sleep(0.5)
            return True

        # Búsqueda real
        self.logger.debug(f"🔍 Buscando: {image_name} (confidence={confidence})")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(
                    str(image_path),
                    confidence=confidence,
                    region=region
                )

                if location:
                    # Obtener centro de la imagen detectada
                    center = pyautogui.center(location)
                    pyautogui.click(center)
                    self.logger.info(f"✅ Click en {image_name} en posición {center}")
                    return True

            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                self.logger.debug(f"Error buscando {image_name}: {e}")

            time.sleep(0.5)

        self.logger.warning(f"⚠️ Timeout: No se encontró {image_name} después de {timeout}s")
        return False

    def type_text(self, text: str, interval: float = 0.05, press_enter: bool = False):
        """
        Escribir texto en el campo activo.

        Args:
            text: Texto a escribir
            interval: Intervalo entre teclas en segundos
            press_enter: Si True, presiona Enter al final
        """
        if self.simulation_mode:
            self.logger.info(f"🎭 [SIMULACIÓN] Escribiendo: {text}")
            time.sleep(0.3)
            return

        pyautogui.write(str(text), interval=interval)
        self.logger.info(f"✍️ Texto escrito: {text}")

        if press_enter:
            pyautogui.press('enter')
            time.sleep(0.5)

    def press_key(self, key: str, times: int = 1):
        """
        Presionar una tecla.

        Args:
            key: Tecla a presionar ('enter', 'tab', 'esc', etc.)
            times: Número de veces a presionar
        """
        if self.simulation_mode:
            self.logger.info(f"🎭 [SIMULACIÓN] Presionando tecla: {key} x{times}")
            return

        for _ in range(times):
            pyautogui.press(key)
            time.sleep(0.2)

        self.logger.debug(f"⌨️ Tecla presionada: {key} x{times}")

    def navigate_to_sales_order(self) -> bool:
        """
        Navegar al formulario de Orden de Venta en SAP.

        Secuencia:
        1. Click en menú "Módulos"
        2. Click en "Ventas"
        3. Click en "Orden de Venta"

        Returns:
            bool: True si la navegación fue exitosa
        """
        self.logger.info("🧭 Navegando a Orden de Venta...")

        # 1. Click en Módulos
        if not self.find_and_click("navegacion/menu_modulos.png", confidence=self.confidence, timeout=self.timeout):
            self.logger.error("❌ No se pudo abrir menú Módulos")
            return False
        time.sleep(1.5)

        # 2. Click en Ventas
        if not self.find_and_click("navegacion/menu_ventas.png", confidence=self.confidence, timeout=self.timeout):
            self.logger.error("❌ No se pudo abrir menú Ventas")
            return False
        time.sleep(1.5)

        # 3. Click en Orden de Venta
        if not self.find_and_click("navegacion/boton_orden_venta.png", confidence=self.confidence, timeout=self.timeout):
            self.logger.error("❌ No se pudo abrir Orden de Venta")
            return False
        time.sleep(2)  # Esperar que cargue el formulario

        self.logger.info("✅ Formulario de Orden de Venta abierto")
        return True

    def fill_customer(self, nit: str, nombre: str) -> bool:
        """
        Rellenar campo de cliente con NIT.

        Args:
            nit: NIT del cliente
            nombre: Nombre del cliente (para validación)

        Returns:
            bool: True si se rellenó exitosamente
        """
        self.logger.info(f"👤 Rellenando cliente: {nit} - {nombre}")

        # En modo simulación, solo simular
        if self.simulation_mode:
            self.logger.info(f"🎭 [SIMULACIÓN] Cliente: {nit}")
            time.sleep(0.5)
            return True

        # TODO: Implementar búsqueda de campo cliente
        # Por ahora, asumir que el campo está activo
        self.type_text(nit, press_enter=True)
        time.sleep(1)

        self.logger.info(f"✅ Cliente {nit} seleccionado")
        return True

    def fill_order_header(self, order_data: Dict[str, Any]) -> bool:
        """
        Rellenar encabezado de la orden.

        Args:
            order_data: Diccionario con datos de la orden

        Returns:
            bool: True si se rellenó exitosamente
        """
        self.logger.info("📝 Rellenando encabezado de orden...")

        # Cliente (NIT)
        comprador = order_data.get('comprador', {})
        if not self.fill_customer(comprador.get('nit'), comprador.get('nombre')):
            return False

        # Fecha de documento
        fecha_doc = order_data.get('fecha_documento')
        if fecha_doc:
            self.logger.info(f"📅 Fecha documento: {fecha_doc}")
            # TODO: Implementar llenado de fecha si es necesario
            if not self.simulation_mode:
                # Navegar al campo de fecha y rellenar
                pass

        # Fecha de entrega
        fecha_entrega = order_data.get('fecha_entrega')
        if fecha_entrega:
            self.logger.info(f"📅 Fecha entrega: {fecha_entrega}")
            # TODO: Implementar llenado de fecha de entrega

        self.logger.info("✅ Encabezado rellenado")
        return True

    def add_item(self, item: Dict[str, Any], item_number: int) -> bool:
        """
        Agregar un item a la orden.

        Args:
            item: Diccionario con datos del item
            item_number: Número de item (para logging)

        Returns:
            bool: True si se agregó exitosamente
        """
        codigo = item.get('codigo')
        descripcion = item.get('descripcion')
        cantidad = item.get('cantidad')
        precio = item.get('precio_unitario')

        self.logger.info(f"➕ Item {item_number}: {codigo} - Cant: {cantidad}")

        if self.simulation_mode:
            self.logger.info(f"🎭 [SIMULACIÓN] Item: {codigo} x {cantidad}")
            time.sleep(0.5)
            return True

        # TODO: Implementar lógica real de agregar item
        # 1. Click en campo código o primera celda vacía
        # 2. Escribir código
        # 3. Tab/Enter para siguiente campo
        # 4. Escribir cantidad
        # 5. Tab/Enter (precio se autocompleta generalmente)
        # 6. Confirmar item

        # Por ahora, simulación simple
        self.type_text(codigo, press_enter=True)
        time.sleep(0.5)
        self.type_text(str(cantidad), press_enter=True)
        time.sleep(0.5)

        self.logger.info(f"✅ Item {item_number} agregado")
        return True

    def save_order(self, order_number: str) -> bool:
        """
        Guardar la orden en SAP.

        Args:
            order_number: Número de orden (para logging)

        Returns:
            bool: True si se guardó exitosamente
        """
        self.logger.info(f"💾 Guardando orden {order_number}...")

        if self.simulation_mode:
            self.logger.info(f"🎭 [SIMULACIÓN] Orden {order_number} guardada")
            time.sleep(1)
            return True

        # TODO: Implementar guardado real
        # Generalmente: Ctrl+S o botón "Actualizar"/"Agregar"
        pyautogui.hotkey('ctrl', 's')
        time.sleep(2)

        # TODO: Verificar confirmación de guardado
        # Buscar mensaje de éxito o ventana de confirmación

        self.logger.info(f"✅ Orden {order_number} guardada exitosamente")
        return True

    def close_order_window(self) -> bool:
        """
        Cerrar ventana de orden actual.

        Returns:
            bool: True si se cerró exitosamente
        """
        if self.simulation_mode:
            self.logger.info("🎭 [SIMULACIÓN] Cerrando ventana de orden")
            time.sleep(0.3)
            return True

        # Ctrl+W o Esc para cerrar
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)

        self.logger.info("✅ Ventana de orden cerrada")
        return True

    def process_order(self, order_data: Dict[str, Any]) -> bool:
        """
        Procesar una orden completa en SAP.

        Este es el método principal que orquesta todo el proceso:
        1. Navegar a Orden de Venta
        2. Rellenar encabezado
        3. Agregar todos los items
        4. Guardar orden
        5. Cerrar ventana

        Args:
            order_data: Diccionario completo con datos de la orden

        Returns:
            bool: True si la orden se procesó exitosamente
        """
        orden_compra = order_data.get('orden_compra', 'N/A')
        items = order_data.get('items', [])

        self.logger.info(f"🎯 Procesando orden: {orden_compra} ({len(items)} items)")

        try:
            # 1. Navegar a Orden de Venta
            if not self.navigate_to_sales_order():
                self.logger.error("❌ Fallo en navegación")
                return False

            # 2. Rellenar encabezado
            if not self.fill_order_header(order_data):
                self.logger.error("❌ Fallo rellenando encabezado")
                return False

            # 3. Agregar items
            for idx, item in enumerate(items, 1):
                if not self.add_item(item, idx):
                    self.logger.error(f"❌ Fallo agregando item {idx}: {item.get('codigo')}")
                    return False

            # 4. Guardar orden
            if not self.save_order(orden_compra):
                self.logger.error("❌ Fallo guardando orden")
                return False

            # 5. Cerrar ventana
            self.close_order_window()

            self.logger.info(f"🎉 Orden {orden_compra} procesada exitosamente!")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error crítico procesando orden {orden_compra}: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False

    def take_debug_screenshot(self, name: str = "debug"):
        """
        Tomar screenshot para debugging.

        Args:
            name: Nombre del archivo (sin extensión)
        """
        if self.simulation_mode:
            return

        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.assets_path.parent.parent / f"debug_{name}_{timestamp}.png"
            pyautogui.screenshot(str(screenshot_path))
            self.logger.info(f"📸 Screenshot guardado: {screenshot_path}")
        except Exception as e:
            self.logger.warning(f"⚠️ Error guardando screenshot: {e}")
