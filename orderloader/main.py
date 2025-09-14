#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrderLoader - Sistema Simple y Funcional
Una sola clase, una sola forma de ejecutar
"""

import json
import time
import shutil
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

import pyautogui

# Configuración simple
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data"
PENDING_PATH = DATA_PATH / "pending"
COMPLETED_PATH = DATA_PATH / "completed"
LOGS_PATH = PROJECT_ROOT / "logs"

REMOTE_DESKTOP_IP = "20.96.6.64"
REMOTE_DESKTOP_KEYWORDS = ["remoto", "Conexión", "Remote", REMOTE_DESKTOP_IP]


class OrderLoader:
    """Sistema simple de OrderLoader - Todo en una clase"""
    
    def __init__(self):
        """Inicializar sistema"""
        self.setup_logging()
        self.setup_directories()
        self.logger.info("🚀 OrderLoader iniciado")
    
    def setup_logging(self):
        """Configurar logging simple"""
        LOGS_PATH.mkdir(parents=True, exist_ok=True)
        log_file = LOGS_PATH / f"orderloader_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Crear directorios necesarios"""
        for directory in [PENDING_PATH, COMPLETED_PATH]:
            directory.mkdir(parents=True, exist_ok=True)
        self.logger.info("📁 Directorios configurados")
    
    def find_remote_desktop(self) -> Optional[Dict[str, Any]]:
        """Buscar ventana del escritorio remoto"""
        self.logger.info("🔍 Buscando escritorio remoto...")
        
        try:
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=10)
            
            if not result.stdout or result.returncode != 0:
                self.logger.error("❌ Error ejecutando PowerShell")
                return None
            
            windows_data = json.loads(result.stdout)
            if not isinstance(windows_data, list):
                windows_data = [windows_data]
            
            for window in windows_data:
                if self._is_remote_desktop_window(window):
                    self.logger.info(f"✅ Ventana encontrada: {window.get('MainWindowTitle', 'N/A')}")
                    return window
            
            self.logger.error("❌ No se encontró escritorio remoto")
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error buscando ventana: {e}")
            return None
    
    def _is_remote_desktop_window(self, window: Dict[str, Any]) -> bool:
        """Verificar si es ventana de escritorio remoto"""
        title = window.get('MainWindowTitle', '').lower()
        process = window.get('ProcessName', '').lower()
        
        if process == 'mstsc':
            return True
        
        for keyword in REMOTE_DESKTOP_KEYWORDS:
            if keyword.lower() in title:
                return True
        
        return False
    
    def activate_remote_desktop(self, window_info: Dict[str, Any]) -> bool:
        """Activar ventana del escritorio remoto"""
        if not window_info:
            return False
        
        self.logger.info("🔄 Activando escritorio remoto...")
        
        # Configurar pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Intentar múltiples estrategias
        strategies = [
            self._activate_alt_tab,
            self._activate_powershell,
            self._activate_win_tab
        ]
        
        for i, strategy in enumerate(strategies, 1):
            self.logger.info(f"  - Estrategia {i}")
            if strategy(window_info):
                self.logger.info(f"✅ Activado con estrategia {i}")
                return True
        
        self.logger.error("❌ No se pudo activar")
        return False
    
    def _activate_alt_tab(self, window_info: Dict[str, Any]) -> bool:
        """Activar con Alt+Tab"""
        try:
            for i in range(10):
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.3)
                if i > 5:
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error Alt+Tab: {e}")
            return False
    
    def _activate_powershell(self, window_info: Dict[str, Any]) -> bool:
        """Activar con PowerShell"""
        try:
            process_id = window_info.get('Id')
            if not process_id:
                return False
            
            script = f'''
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Win32 {{
                [DllImport("user32.dll")]
                public static extern bool SetForegroundWindow(IntPtr hWnd);
                [DllImport("user32.dll")]
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
            self.logger.error(f"Error PowerShell: {e}")
            return False
    
    def _activate_win_tab(self, window_info: Dict[str, Any]) -> bool:
        """Activar con Win+Tab"""
        try:
            pyautogui.hotkey('win', 'tab')
            time.sleep(1)
            
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            pyautogui.click(center_x, center_y)
            
            time.sleep(0.5)
            return True
            
        except Exception as e:
            self.logger.error(f"Error Win+Tab: {e}")
            return False
    
    def maximize_window(self) -> bool:
        """Maximizar ventana"""
        self.logger.info("📱 Maximizando ventana...")
        try:
            pyautogui.hotkey('win', 'up')
            time.sleep(1)
            self.logger.info("✅ Ventana maximizada")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error maximizando: {e}")
            return False
    
    def verify_sap(self) -> bool:
        """Verificar que SAP esté visible"""
        self.logger.info("🔍 Verificando SAP...")
        try:
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Where-Object {$_.MainWindowTitle -match "SAP"} | '
                'Select-Object MainWindowTitle | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=5)
            
            if result.stdout and result.returncode == 0:
                sap_windows = json.loads(result.stdout)
                if sap_windows:
                    self.logger.info("✅ SAP detectado")
                    return True
            
            self.logger.warning("⚠️ SAP no detectado")
            return False
            
        except Exception as e:
            self.logger.warning(f"⚠️ Error verificando SAP: {e}")
            return False
    
    def get_pending_files(self) -> List[Path]:
        """Obtener archivos pendientes"""
        if not PENDING_PATH.exists():
            return []
        
        files = [f for f in PENDING_PATH.iterdir() 
                if f.is_file() and f.suffix.lower() == '.json']
        
        files.sort(key=lambda x: x.stat().st_ctime)
        return files
    
    def validate_json(self, file_path: Path) -> bool:
        """Validar archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required_fields = ['orden_compra', 'fecha_documento', 'comprador', 'items']
            for field in required_fields:
                if field not in data:
                    self.logger.error(f"❌ Campo faltante: {field}")
                    return False
            
            # Validar comprador
            comprador = data.get('comprador', {})
            if not isinstance(comprador, dict) or 'nit' not in comprador or 'nombre' not in comprador:
                self.logger.error("❌ Comprador inválido")
                return False
            
            # Validar items
            items = data.get('items', [])
            if not isinstance(items, list):
                self.logger.error("❌ Items debe ser lista")
                return False
            
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    self.logger.error(f"❌ Item {i} inválido")
                    return False
                
                required_item_fields = ['descripcion', 'codigo', 'cantidad', 'precio_unitario']
                for field in required_item_fields:
                    if field not in item:
                        self.logger.error(f"❌ Item {i}: Campo faltante: {field}")
                        return False
            
            self.logger.info(f"✅ JSON válido: {file_path.name}")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Error JSON en {file_path}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error validando {file_path}: {e}")
            return False
    
    def process_json(self, file_path: Path) -> bool:
        """Procesar archivo JSON"""
        self.logger.info(f"📄 Procesando: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"📋 Orden: {data.get('orden_compra', 'N/A')}")
            self.logger.info(f"📅 Fecha: {data.get('fecha_documento', 'N/A')}")
            self.logger.info(f"🏢 Comprador: {data.get('comprador', {}).get('nombre', 'N/A')}")
            self.logger.info(f"💰 Total: {data.get('valor_total', 'N/A')}")
            self.logger.info(f"📦 Items: {len(data.get('items', []))}")
            
            time.sleep(2)  # Simular procesamiento
            
            self.logger.info(f"✅ Procesado: {file_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error procesando {file_path.name}: {e}")
            return False
    
    def move_to_completed(self, file_path: Path) -> bool:
        """Mover archivo a completados"""
        try:
            destination = COMPLETED_PATH / file_path.name
            
            counter = 1
            while destination.exists():
                name = file_path.stem
                ext = file_path.suffix
                destination = COMPLETED_PATH / f"{name}_{counter}{ext}"
                counter += 1
            
            shutil.move(str(file_path), str(destination))
            self.logger.info(f"✅ Movido: {file_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error moviendo: {e}")
            return False
    
    def process_queue(self) -> bool:
        """Procesar cola de archivos"""
        self.logger.info("📦 Procesando cola...")
        
        pending_files = self.get_pending_files()
        
        if not pending_files:
            self.logger.info("📭 No hay archivos pendientes")
            return True
        
        self.logger.info(f"📋 Procesando {len(pending_files)} archivos...")
        
        for file_path in pending_files:
            if not self.validate_json(file_path):
                self.logger.error(f"❌ Inválido: {file_path.name}")
                continue
            
            if not self.process_json(file_path):
                self.logger.error(f"❌ Error procesando: {file_path.name}")
                continue
            
            if not self.move_to_completed(file_path):
                self.logger.error(f"❌ Error moviendo: {file_path.name}")
                continue
        
        self.logger.info("✅ Cola procesada")
        return True
    
    def get_queue_status(self) -> Dict[str, int]:
        """Obtener estado de la cola"""
        pending_files = self.get_pending_files()
        completed_files = [f for f in COMPLETED_PATH.iterdir() 
                          if f.is_file() and f.suffix.lower() == '.json']
        
        return {
            'pending': len(pending_files),
            'completed': len(completed_files),
            'total': len(pending_files) + len(completed_files)
        }
    
    def print_status(self):
        """Imprimir estado"""
        status = self.get_queue_status()
        print(f"\n📊 Estado:")
        print(f"   📁 Pendientes: {status['pending']}")
        print(f"   ✅ Completados: {status['completed']}")
        print(f"   📈 Total: {status['total']}")
    
    def run(self) -> bool:
        """Ejecutar proceso completo"""
        self.logger.info("🎯 Iniciando automatización...")
        
        try:
            # Validar sistema
            self.logger.info("🔍 Validando sistema...")
            test_file = Path("test_permissions.tmp")
            test_file.write_text("test")
            test_file.unlink()
            self.logger.info("✅ Sistema validado")
            
            # Conectar al escritorio remoto
            window_info = self.find_remote_desktop()
            if not window_info:
                return False
            
            if not self.activate_remote_desktop(window_info):
                return False
            
            # Maximizar ventana
            if not self.maximize_window():
                self.logger.warning("⚠️ No se pudo maximizar")
            
            # Esperar estabilización
            self.logger.info("⏳ Esperando estabilización...")
            time.sleep(3)
            
            # Verificar SAP
            if not self.verify_sap():
                self.logger.warning("⚠️ SAP no detectado")
            
            # Procesar cola
            if not self.process_queue():
                return False
            
            self.logger.info("🎉 ¡Procesamiento completado!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error en automatización: {e}")
            return False


def main():
    """Función principal - Una sola forma de ejecutar"""
    
    print("""
🎯 ORDERLOADER SIMPLE
Sistema optimizado para procesamiento de cola

FUNCIONALIDAD:
1. Conectar al escritorio remoto (20.96.6.64)
2. Verificar que SAP esté abierto
3. Procesar archivos JSON de la cola

REQUISITOS:
- Escritorio remoto abierto y conectado a 20.96.6.64
- SAP Desktop ya abierto en el escritorio remoto
- Archivos JSON en data/pending/
""")
    
    try:
        # Crear instancia del sistema
        order_loader = OrderLoader()
        
        # Mostrar estado
        order_loader.print_status()
        
        # Confirmar inicio
        input("\nPresiona Enter para iniciar...")
        print()
        
        # Ejecutar automatización
        success = order_loader.run()
        
        if success:
            print("\n🎉 ¡Procesamiento completado exitosamente!")
        else:
            print("\n❌ El procesamiento falló")
            print("Revisa los logs para más detalles")
        
        # Mostrar estado final
        order_loader.print_status()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Procesamiento interrumpido por el usuario")
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    
    finally:
        print("\nPresiona Enter para salir...")
        input()


if __name__ == "__main__":
    main()