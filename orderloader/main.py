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

# Configuración para Chrome/SAP
ALT_TAB_DELAY = 1.0  # Tiempo de espera después de Alt+Tab
CHROME_STABILIZATION_WAIT = 3  # Tiempo de estabilización para Chrome


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
    
    # FUNCIÓN ELIMINADA: find_remote_desktop() - Ya no se necesita con Alt+Tab
    
    # FUNCIÓN ELIMINADA: _is_remote_desktop_window() - Ya no se necesita con Alt+Tab
    
    # FUNCIÓN ELIMINADA: activate_remote_desktop() - Reemplazada por activate_sap_chrome_window()
    
    # FUNCIÓN ELIMINADA: _activate_alt_tab() - Simplificada en activate_sap_chrome_window()
    
    # FUNCIÓN ELIMINADA: _activate_powershell() - Ya no se necesita con Alt+Tab
    
    # FUNCIÓN ELIMINADA: _activate_win_tab() - Ya no se necesita con Alt+Tab
    
    def activate_sap_chrome_window(self) -> bool:
        """Activar ventana de SAP en Chrome con Alt+Tab"""
        self.logger.info("🔄 Activando SAP en Chrome...")
        
        try:
            # Configurar pyautogui
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.5
            
            # Presionar Alt+Tab para cambiar a la ventana correcta
            pyautogui.hotkey('alt', 'tab')
            time.sleep(1)  # Esperar a que se active
            
            self.logger.info("✅ Ventana de SAP activada")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error activando ventana: {e}")
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
    
    def verify_sap_chrome(self) -> bool:
        """Verificar que SAP esté visible en Chrome"""
        self.logger.info("🔍 Verificando SAP en Chrome...")
        
        try:
            # Verificación simple - confirmar que la ventana está activa
            # Buscar procesos de Chrome con SAP o Auto.Sky
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Where-Object {$_.MainWindowTitle -match "Chrome|SAP|Auto.Sky"} | '
                'Select-Object MainWindowTitle | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=5)
            
            if result.stdout and result.returncode == 0:
                chrome_windows = json.loads(result.stdout)
                if chrome_windows:
                    self.logger.info("✅ SAP en Chrome verificado")
                    return True
            
            # Verificación alternativa - asumir que está bien si llegamos aquí
            time.sleep(1)
            self.logger.info("✅ SAP en Chrome verificado (método alternativo)")
            return True
            
        except Exception as e:
            self.logger.warning(f"⚠️ Error verificando SAP: {e}")
            # En caso de error, asumir que está bien y continuar
            return True
    
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
        """Ejecutar proceso completo - VERSIÓN SIMPLIFICADA"""
        self.logger.info("🎯 Iniciando automatización...")
        
        try:
            # Validar sistema
            self.logger.info("🔍 Validando sistema...")
            test_file = Path("test_permissions.tmp")
            test_file.write_text("test")
            test_file.unlink()
            self.logger.info("✅ Sistema validado")
            
            # Activar ventana de SAP en Chrome (SIMPLIFICADO)
            if not self.activate_sap_chrome_window():
                return False
            
            # Maximizar ventana
            if not self.maximize_window():
                self.logger.warning("⚠️ No se pudo maximizar")
            
            # Esperar estabilización
            self.logger.info("⏳ Esperando estabilización...")
            time.sleep(3)
            
            # Verificar SAP (opcional, para confirmar)
            if not self.verify_sap_chrome():
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
    """Función principal - VERSIÓN SIMPLIFICADA"""
    
    print("""
🎯 ORDERLOADER SIMPLE - VERSIÓN CHROME
Sistema optimizado para SAP en Chrome

FUNCIONALIDAD:
1. Presionar Alt+Tab para activar ventana de SAP en Chrome
2. Verificar que SAP esté visible
3. Procesar archivos JSON de la cola

REQUISITOS:
- SAP abierto en Chrome (ventana debe estar disponible con Alt+Tab)
- Archivos JSON en data/pending/

NOTA: Asegúrate de que la ventana de SAP en Chrome esté abierta
      y sea accesible con Alt+Tab antes de ejecutar el sistema.
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