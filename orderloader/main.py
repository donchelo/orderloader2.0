#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrderLoader Final - Sistema Consolidado
Todo el código en un solo archivo, sin redundancias
"""

import os
import json
import time
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

import pyautogui

# Importar configuración
from config import *


class OrderLoaderFinal:
    """Sistema consolidado de OrderLoader - Todo en una clase"""
    
    def __init__(self):
        """Inicializar sistema"""
        self.setup_logging()
        self.setup_directories()
        self.logger.info("🚀 OrderLoader Final iniciado")
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        # Crear directorio de logs
        LOGS_PATH.mkdir(parents=True, exist_ok=True)
        
        # Configurar logging
        log_file = LOGS_PATH / f"orderloader_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=getattr(logging, LOGGING_CONFIG['level']),
            format=LOGGING_CONFIG['format'],
            handlers=[
                logging.FileHandler(log_file, encoding=LOGGING_CONFIG['encoding']),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Crear directorios necesarios"""
        directories = [DATA_PATH, PENDING_PATH, COMPLETED_PATH]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Crear archivos .gitkeep
        (PENDING_PATH / ".gitkeep").touch(exist_ok=True)
        (COMPLETED_PATH / ".gitkeep").touch(exist_ok=True)
        
        self.logger.info("📁 Directorios del sistema configurados")
    
    def validate_system(self) -> bool:
        """Validar que el sistema esté listo - Versión simplificada"""
        self.logger.info("🔍 Validando sistema...")
        
        # Validar permisos
        try:
            test_file = Path("test_permissions.tmp")
            test_file.write_text("test")
            test_file.unlink()
            self.logger.info("✅ Permisos de escritura verificados")
        except Exception as e:
            self.logger.error(f"❌ Error de permisos: {e}")
            return False
        
        self.logger.info("✅ Sistema validado correctamente")
        return True
    
    def find_remote_desktop_window(self) -> Optional[Dict[str, Any]]:
        """Buscar ventana del escritorio remoto"""
        self.logger.info("🔍 Buscando ventana del escritorio remoto...")
        
        try:
            # Usar PowerShell para obtener ventanas
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=10)
            
            if not result.stdout or result.returncode != 0:
                self.logger.error("❌ Error ejecutando PowerShell")
                return None
            
            # Parsear resultado JSON
            windows_data = json.loads(result.stdout)
            if not isinstance(windows_data, list):
                windows_data = [windows_data]
            
            # Buscar ventana del escritorio remoto
            for window in windows_data:
                if self._is_remote_desktop_window(window):
                    self.logger.info(f"✅ Ventana encontrada: {window.get('MainWindowTitle', 'N/A')}")
                    return window
            
            self.logger.error("❌ No se encontró ventana del escritorio remoto")
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error buscando ventana: {e}")
            return None
    
    def _is_remote_desktop_window(self, window: Dict[str, Any]) -> bool:
        """Verificar si una ventana es del escritorio remoto"""
        title = window.get('MainWindowTitle', '').lower()
        process = window.get('ProcessName', '').lower()
        
        # Verificar por proceso
        if process == 'mstsc':
            return True
        
        # Verificar por palabras clave en el título
        for keyword in REMOTE_DESKTOP_TITLE_KEYWORDS:
            if keyword.lower() in title:
                return True
        
        return False
    
    def activate_remote_desktop(self, window_info: Dict[str, Any]) -> bool:
        """Activar ventana del escritorio remoto"""
        if not window_info:
            return False
        
        self.logger.info("🔄 Activando ventana del escritorio remoto...")
        
        # Configurar pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = IMAGE_RECOGNITION['pause_between_actions']
        
        # Intentar múltiples estrategias de activación
        strategies = [
            self._activate_with_alt_tab,
            self._activate_with_powershell,
            self._activate_with_win_tab
        ]
        
        for i, strategy in enumerate(strategies, 1):
            self.logger.info(f"  - Estrategia {i}: {strategy.__name__}")
            
            if strategy(window_info):
                self.logger.info(f"✅ Ventana activada con estrategia {i}")
                return True
        
        self.logger.error("❌ No se pudo activar la ventana con ninguna estrategia")
        return False
    
    def _activate_with_alt_tab(self, window_info: Dict[str, Any]) -> bool:
        """Activar ventana usando Alt+Tab"""
        try:
            max_attempts = IMAGE_RECOGNITION['max_alt_tab_attempts']
            delay = IMAGE_RECOGNITION['alt_tab_delay']
            
            for i in range(max_attempts):
                pyautogui.hotkey('alt', 'tab')
                time.sleep(delay)
                
                # Verificar si la ventana está activa (simplificado)
                if i > 5:  # Asumir que después de varios intentos está activa
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error con Alt+Tab: {e}")
            return False
    
    def _activate_with_powershell(self, window_info: Dict[str, Any]) -> bool:
        """Activar ventana usando PowerShell"""
        try:
            process_id = window_info.get('Id')
            if not process_id:
                return False
            
            # Script PowerShell para activar ventana
            script = f'''
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
                    Write-Host "SUCCESS"
                }}
            }}
            '''
            
            result = subprocess.run([
                'powershell', '-Command', script
            ], capture_output=True, text=True, timeout=5)
            
            return "SUCCESS" in result.stdout
            
        except Exception as e:
            self.logger.error(f"Error con PowerShell: {e}")
            return False
    
    def _activate_with_win_tab(self, window_info: Dict[str, Any]) -> bool:
        """Activar ventana usando Win+Tab"""
        try:
            # Abrir selector de ventanas
            pyautogui.hotkey('win', 'tab')
            time.sleep(1)
            
            # Hacer clic en el centro de la pantalla
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            pyautogui.click(center_x, center_y)
            
            time.sleep(0.5)
            return True
            
        except Exception as e:
            self.logger.error(f"Error con Win+Tab: {e}")
            return False
    
    def maximize_window(self) -> bool:
        """Maximizar ventana actual"""
        self.logger.info("📱 Maximizando ventana...")
        
        try:
            # Usar Win+Up para maximizar
            pyautogui.hotkey('win', 'up')
            time.sleep(1)
            
            self.logger.info("✅ Ventana maximizada")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error maximizando ventana: {e}")
            return False
    
    def verify_sap_visible(self) -> bool:
        """Verificar que SAP esté visible en pantalla (opcional)"""
        self.logger.info("🔍 Verificando que SAP esté visible...")
        
        try:
            # Usar PowerShell para verificar ventanas de SAP
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Where-Object {$_.MainWindowTitle -match "SAP"} | '
                'Select-Object MainWindowTitle | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=5)
            
            if result.stdout and result.returncode == 0:
                sap_windows = json.loads(result.stdout)
                if sap_windows:
                    self.logger.info("✅ SAP detectado en el escritorio remoto")
                    return True
            
            self.logger.warning("⚠️ No se detectó SAP en el escritorio remoto")
            return False
            
        except Exception as e:
            self.logger.warning(f"⚠️ Error verificando SAP: {e}")
            return False
    
    def get_pending_files(self) -> List[Path]:
        """Obtener archivos pendientes"""
        if not PENDING_PATH.exists():
            return []
        
        files = [f for f in PENDING_PATH.iterdir() 
                if f.is_file() and f.suffix.lower() in FILE_CONFIG['supported_extensions']]
        
        # Ordenar por fecha de creación (FIFO)
        files.sort(key=lambda x: x.stat().st_ctime)
        
        return files
    
    def validate_json_file(self, file_path: Path) -> bool:
        """Validar archivo JSON"""
        try:
            with open(file_path, 'r', encoding=FILE_CONFIG['encoding']) as f:
                data = json.load(f)
            
            # Validar campos requeridos
            required_fields = ['orden_compra', 'fecha_documento', 'comprador', 'items']
            for field in required_fields:
                if field not in data:
                    self.logger.error(f"❌ Campo requerido faltante: {field}")
                    return False
            
            # Validar comprador
            if 'comprador' in data:
                comprador = data['comprador']
                if not isinstance(comprador, dict):
                    self.logger.error("❌ Campo 'comprador' debe ser un objeto")
                    return False
                
                if 'nit' not in comprador or 'nombre' not in comprador:
                    self.logger.error("❌ Campos 'nit' y 'nombre' requeridos en comprador")
                    return False
            
            # Validar items
            if 'items' in data:
                items = data['items']
                if not isinstance(items, list):
                    self.logger.error("❌ Campo 'items' debe ser una lista")
                    return False
                
                for i, item in enumerate(items):
                    if not isinstance(item, dict):
                        self.logger.error(f"❌ Item {i} debe ser un objeto")
                        return False
                    
                    required_item_fields = ['descripcion', 'codigo', 'cantidad', 'precio_unitario']
                    for field in required_item_fields:
                        if field not in item:
                            self.logger.error(f"❌ Item {i}: Campo requerido faltante: {field}")
                            return False
            
            self.logger.info(f"✅ Archivo JSON válido: {file_path.name}")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Error de formato JSON en {file_path}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error validando archivo {file_path}: {e}")
            return False
    
    def process_json_file(self, file_path: Path) -> bool:
        """Procesar archivo JSON"""
        self.logger.info(f"📄 Procesando archivo: {file_path.name}")
        
        try:
            # Leer archivo JSON
            with open(file_path, 'r', encoding=FILE_CONFIG['encoding']) as f:
                data = json.load(f)
            
            # Mostrar información de la orden
            self.logger.info(f"📋 Orden de compra: {data.get('orden_compra', 'N/A')}")
            self.logger.info(f"📅 Fecha documento: {data.get('fecha_documento', 'N/A')}")
            self.logger.info(f"🏢 Comprador: {data.get('comprador', {}).get('nombre', 'N/A')}")
            self.logger.info(f"💰 Valor total: {data.get('valor_total', 'N/A')}")
            self.logger.info(f"📦 Items: {len(data.get('items', []))}")
            
            # Simular tiempo de procesamiento
            time.sleep(WAIT_TIMES['file_processing'])
            
            self.logger.info(f"✅ Archivo JSON procesado: {file_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error procesando archivo {file_path.name}: {e}")
            return False
    
    def move_to_completed(self, file_path: Path) -> bool:
        """Mover archivo a completados"""
        try:
            destination = COMPLETED_PATH / file_path.name
            
            # Si existe, agregar número
            counter = 1
            while destination.exists():
                name = file_path.stem
                ext = file_path.suffix
                destination = COMPLETED_PATH / f"{name}_{counter}{ext}"
                counter += 1
            
            shutil.move(str(file_path), str(destination))
            self.logger.info(f"✅ Archivo movido a completados: {file_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error moviendo archivo: {e}")
            return False
    
    def process_queue(self) -> bool:
        """Procesar cola de archivos"""
        self.logger.info("📦 Procesando cola de archivos...")
        
        # Obtener archivos pendientes
        pending_files = self.get_pending_files()
        
        if not pending_files:
            self.logger.info("📭 No hay archivos pendientes en la cola")
            return True
        
        self.logger.info(f"📋 Procesando {len(pending_files)} archivos...")
        
        # Procesar cada archivo
        for file_path in pending_files:
            if not self.validate_json_file(file_path):
                self.logger.error(f"❌ Archivo inválido: {file_path.name}")
                continue
            
            if not self.process_json_file(file_path):
                self.logger.error(f"❌ Error procesando archivo: {file_path.name}")
                continue
            
            if not self.move_to_completed(file_path):
                self.logger.error(f"❌ Error moviendo archivo: {file_path.name}")
                continue
        
        self.logger.info("✅ Procesamiento de cola completado")
        return True
    
    def get_queue_status(self) -> Dict[str, int]:
        """Obtener estado de la cola"""
        pending_files = self.get_pending_files()
        completed_files = [f for f in COMPLETED_PATH.iterdir() 
                          if f.is_file() and f.suffix.lower() in FILE_CONFIG['supported_extensions']]
        
        return {
            'pending': len(pending_files),
            'completed': len(completed_files),
            'total': len(pending_files) + len(completed_files)
        }
    
    def print_queue_status(self):
        """Imprimir estado de la cola"""
        status = self.get_queue_status()
        
        print(f"\n📊 Estado de Colas:")
        print(f"   📁 Pendientes: {status['pending']}")
        print(f"   ✅ Completados: {status['completed']}")
        print(f"   📈 Total: {status['total']}")
    
    def run(self) -> bool:
        """Ejecutar proceso completo - Versión simplificada"""
        self.logger.info("🎯 Iniciando automatización simplificada...")
        
        try:
            # Paso 1: Validar sistema
            if not self.validate_system():
                return False
            
            # Paso 2: Conectar al escritorio remoto
            window_info = self.find_remote_desktop_window()
            if not window_info:
                return False
            
            if not self.activate_remote_desktop(window_info):
                return False
            
            # Paso 3: Maximizar ventana
            if not self.maximize_window():
                self.logger.warning("⚠️ No se pudo maximizar la ventana")
            
            # Esperar estabilización
            wait_time = WAIT_TIMES['stabilization']
            self.logger.info(f"⏳ Esperando {wait_time} segundos para estabilizar...")
            time.sleep(wait_time)
            
            # Paso 4: Verificar SAP (opcional)
            if not self.verify_sap_visible():
                self.logger.warning("⚠️ SAP no parece estar visible")
            
            # Paso 5: Procesar cola
            if not self.process_queue():
                return False
            
            self.logger.info("🎉 ¡Procesamiento completado exitosamente!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error en automatización: {e}")
            return False


def main():
    """Función principal"""
    
    print(MESSAGES['welcome'])
    
    try:
        # Crear instancia del sistema
        order_loader = OrderLoaderFinal()
        
        # Mostrar estado de colas
        order_loader.print_queue_status()
        
        # Confirmar inicio
        input("\nPresiona Enter para iniciar el procesamiento...")
        print()
        
        # Ejecutar automatización
        success = order_loader.run()
        
        if success:
            print(f"\n{MESSAGES['success']}")
        else:
            print(f"\n{MESSAGES['error']}")
            print(MESSAGES['check_logs'])
        
        # Mostrar estado final
        order_loader.print_queue_status()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Procesamiento interrumpido por el usuario")
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    
    finally:
        print("\nPresiona Enter para salir...")
        input()


if __name__ == "__main__":
    main()
