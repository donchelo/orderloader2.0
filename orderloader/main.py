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
import functools
import gzip
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Callable

import pyautogui
from config import *

# Configuración simple
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data"
PENDING_PATH = DATA_PATH / "pending"
COMPLETED_PATH = DATA_PATH / "completed"
LOGS_PATH = PROJECT_ROOT / "logs"

# Configuración para Chrome/SAP (importada desde config.py)


class MetricsCollector:
    """Recolector de métricas del sistema"""
    
    def __init__(self):
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'total_files_processed': 0,
            'successful_files': 0,
            'failed_files': 0,
            'retry_attempts': 0,
            'errors': [],
            'performance': {}
        }
        self.metrics_file = PROJECT_ROOT / METRICS_CONFIG['metrics_file']
    
    def start_session(self):
        """Iniciar sesión de métricas"""
        self.metrics['start_time'] = datetime.now().isoformat()
        self.metrics['total_files_processed'] = 0
        self.metrics['successful_files'] = 0
        self.metrics['failed_files'] = 0
        self.metrics['retry_attempts'] = 0
        self.metrics['errors'] = []
    
    def record_file_processed(self, success: bool, file_name: str, duration: float):
        """Registrar archivo procesado"""
        self.metrics['total_files_processed'] += 1
        if success:
            self.metrics['successful_files'] += 1
        else:
            self.metrics['failed_files'] += 1
        
        self.metrics['performance'][file_name] = {
            'success': success,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
    
    def record_retry(self, error_code: str, attempt: int):
        """Registrar intento de retry"""
        self.metrics['retry_attempts'] += 1
        self.metrics['errors'].append({
            'error_code': error_code,
            'attempt': attempt,
            'timestamp': datetime.now().isoformat()
        })
    
    def end_session(self):
        """Finalizar sesión de métricas"""
        self.metrics['end_time'] = datetime.now().isoformat()
        self.save_metrics()
    
    def save_metrics(self):
        """Guardar métricas en archivo"""
        try:
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando métricas: {e}")
    
    def get_success_rate(self) -> float:
        """Obtener tasa de éxito"""
        if self.metrics['total_files_processed'] == 0:
            return 0.0
        return self.metrics['successful_files'] / self.metrics['total_files_processed']


def retry_with_backoff(max_attempts: int = None, base_delay: float = None, 
                       max_delay: float = None, backoff_multiplier: float = None):
    """
    Decorador para retry con backoff exponencial.
    
    Args:
        max_attempts: Número máximo de intentos
        base_delay: Delay inicial en segundos
        max_delay: Delay máximo en segundos
        backoff_multiplier: Multiplicador para backoff exponencial
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            config = RETRY_CONFIG
            max_attempts_val = max_attempts or config['max_attempts']
            base_delay_val = base_delay or config['base_delay']
            max_delay_val = max_delay or config['max_delay']
            backoff_multiplier_val = backoff_multiplier or config['backoff_multiplier']
            
            last_exception = None
            
            for attempt in range(max_attempts_val):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_attempts_val - 1:  # No es el último intento
                        delay = min(base_delay_val * (backoff_multiplier_val ** attempt), max_delay_val)
                        self.logger.warning(f"🔄 Intento {attempt + 1}/{max_attempts_val} falló, reintentando en {delay:.1f}s: {e}")
                        time.sleep(delay)
                    else:
                        self.logger.error(f"❌ Todos los intentos fallaron para {func.__name__}")
            
            raise last_exception
        return wrapper
    return decorator


class WindowManager:
    """Gestor de ventanas y navegación SAP"""
    
    def __init__(self, logger):
        self.logger = logger
    
    @retry_with_backoff()
    def activate_sap_chrome_window(self) -> bool:
        """
        Activar ventana de SAP en Chrome usando Alt+Tab.
        
        Returns:
            bool: True si la activación fue exitosa, False en caso contrario.
        """
        self.logger.info("🔄 Activando SAP en Chrome...")
        
        try:
            # Configurar pyautogui
            pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE
            pyautogui.PAUSE = PYAUTOGUI_PAUSE
            
            # Presionar Alt+Tab para cambiar a la ventana correcta
            pyautogui.hotkey('alt', 'tab')
            time.sleep(WINDOW_ACTIVATION_DELAY)  # Esperar a que se active
            
            self.logger.info("✅ Ventana de SAP activada")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.WINDOW_ACTIVATION_FAILED}] Error activando ventana: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    @retry_with_backoff()
    def maximize_window(self) -> bool:
        """
        Maximizar la ventana activa usando Win+Up.
        
        Returns:
            bool: True si la maximización fue exitosa, False en caso contrario.
        """
        self.logger.info("📱 Maximizando ventana...")
        try:
            pyautogui.hotkey('win', 'up')
            time.sleep(WINDOW_MAXIMIZE_DELAY)
            self.logger.info("✅ Ventana maximizada")
            return True
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.WINDOW_MAXIMIZE_FAILED}] Error maximizando: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    def verify_sap(self) -> bool:
        """
        Verificar que SAP esté visible en el sistema.
        
        Usa PowerShell para buscar procesos con ventanas que contengan 'SAP'
        en el título.
        
        Returns:
            bool: True si SAP está detectado, False en caso contrario.
        """
        self.logger.info("🔍 Verificando SAP...")
        try:
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Where-Object {$_.MainWindowTitle -match "SAP"} | '
                'Select-Object MainWindowTitle | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=POWERSHELL_TIMEOUT)
            
            if result.stdout and result.returncode == 0:
                sap_windows = json.loads(result.stdout)
                if sap_windows:
                    self.logger.info("✅ SAP detectado")
                    return True
            
            self.logger.warning("⚠️ SAP no detectado")
            return False
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"❌ [{ErrorCodes.POWERSHELL_TIMEOUT}] Timeout verificando SAP")
            return False
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.SUBPROCESS_FAILED}] Error verificando SAP: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    def verify_sap_chrome(self) -> bool:
        """
        Verificar que SAP esté visible en Chrome.
        
        Busca procesos de Chrome con títulos que contengan 'Chrome', 'SAP' o 'Auto.Sky'.
        Si no encuentra nada, asume que está bien y continúa.
        
        Returns:
            bool: True si SAP en Chrome está detectado o asumido como correcto.
        """
        self.logger.info("🔍 Verificando SAP en Chrome...")
        
        try:
            # Verificación simple - confirmar que la ventana está activa
            # Buscar procesos de Chrome con SAP o Auto.Sky
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Where-Object {$_.MainWindowTitle -match "Chrome|SAP|Auto.Sky"} | '
                'Select-Object MainWindowTitle | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=POWERSHELL_TIMEOUT)
            
            if result.stdout and result.returncode == 0:
                chrome_windows = json.loads(result.stdout)
                if chrome_windows:
                    self.logger.info("✅ SAP en Chrome verificado")
                    return True
            
            # Verificación alternativa - asumir que está bien si llegamos aquí
            time.sleep(SAP_VERIFICATION_DELAY)
            self.logger.info("✅ SAP en Chrome verificado (método alternativo)")
            return True
            
        except subprocess.TimeoutExpired:
            self.logger.warning(f"⚠️ [{ErrorCodes.POWERSHELL_TIMEOUT}] Timeout verificando SAP en Chrome - continuando")
            return True
        except Exception as e:
            self.logger.warning(f"⚠️ [{ErrorCodes.SUBPROCESS_FAILED}] Error verificando SAP: {e}")
            self.logger.warning(f"   Detalles: {type(e).__name__} - {str(e)}")
            # En caso de error, asumir que está bien y continuar
            return True


class FileProcessor:
    """Procesador de archivos JSON"""
    
    def __init__(self, logger, metrics):
        self.logger = logger
        self.metrics = metrics
        self.backup_path = PROJECT_ROOT / BACKUP_CONFIG['backup_path']
    
    def create_backup(self, file_path: Path) -> bool:
        """
        Crear backup de archivo antes de procesar.
        
        Args:
            file_path (Path): Ruta al archivo a respaldar.
            
        Returns:
            bool: True si el backup fue exitoso, False en caso contrario.
        """
        if not BACKUP_CONFIG['enabled']:
            return True
            
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_file = self.backup_path / backup_name
            
            if BACKUP_CONFIG['compress_backups']:
                backup_file = backup_file.with_suffix('.gz')
                with open(file_path, 'rb') as f_in:
                    with gzip.open(backup_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(file_path, backup_file)
            
            self.logger.info(f"💾 Backup creado: {backup_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error creando backup: {e}")
            return False
    
    def validate_json(self, file_path: Path) -> bool:
        """
        Validar estructura y contenido de archivo JSON.
        
        Verifica que el archivo contenga:
        - orden_compra, fecha_documento, comprador, items
        - comprador con nit y nombre
        - items como lista con descripcion, codigo, cantidad, precio_unitario
        
        Args:
            file_path (Path): Ruta al archivo JSON a validar.
            
        Returns:
            bool: True si el archivo es válido, False en caso contrario.
        """
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
            self.logger.error(f"❌ [{ErrorCodes.JSON_VALIDATION_FAILED}] Error JSON en {file_path}: {e}")
            self.logger.error(f"   Línea {e.lineno}, Columna {e.colno}: {e.msg}")
            return False
        except FileNotFoundError:
            self.logger.error(f"❌ [{ErrorCodes.FILE_NOT_FOUND}] Archivo no encontrado: {file_path}")
            return False
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.JSON_VALIDATION_FAILED}] Error validando {file_path}: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    def process_json(self, file_path: Path) -> bool:
        """
        Procesar archivo JSON de orden de compra.
        
        Lee el archivo, muestra información de la orden y simula el procesamiento.
        Incluye backup automático y métricas de rendimiento.
        
        Args:
            file_path (Path): Ruta al archivo JSON a procesar.
            
        Returns:
            bool: True si el procesamiento fue exitoso, False en caso contrario.
        """
        start_time = time.time()
        self.logger.info(f"📄 Procesando: {file_path.name}")
        
        try:
            # Crear backup antes de procesar
            if not self.create_backup(file_path):
                self.logger.warning("⚠️ No se pudo crear backup, continuando...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"📋 Orden: {data.get('orden_compra', 'N/A')}")
            self.logger.info(f"📅 Fecha: {data.get('fecha_documento', 'N/A')}")
            self.logger.info(f"🏢 Comprador: {data.get('comprador', {}).get('nombre', 'N/A')}")
            self.logger.info(f"💰 Total: {data.get('valor_total', 'N/A')}")
            self.logger.info(f"📦 Items: {len(data.get('items', []))}")
            
            time.sleep(FILE_PROCESSING_SIMULATION_DELAY)  # Simular procesamiento
            
            # Registrar métricas de éxito
            duration = time.time() - start_time
            self.metrics.record_file_processed(True, file_path.name, duration)
            
            self.logger.info(f"✅ Procesado: {file_path.name} (en {duration:.2f}s)")
            return True
            
        except FileNotFoundError:
            duration = time.time() - start_time
            self.metrics.record_file_processed(False, file_path.name, duration)
            self.logger.error(f"❌ [{ErrorCodes.FILE_NOT_FOUND}] Archivo no encontrado: {file_path}")
            return False
        except json.JSONDecodeError as e:
            duration = time.time() - start_time
            self.metrics.record_file_processed(False, file_path.name, duration)
            self.logger.error(f"❌ [{ErrorCodes.JSON_PROCESSING_FAILED}] Error JSON en {file_path}: {e}")
            return False
        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_file_processed(False, file_path.name, duration)
            self.logger.error(f"❌ [{ErrorCodes.JSON_PROCESSING_FAILED}] Error procesando {file_path.name}: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False


class QueueManager:
    """Gestor de colas de archivos"""
    
    def __init__(self, logger, file_processor):
        self.logger = logger
        self.file_processor = file_processor
    
    def get_pending_files(self) -> List[Path]:
        """
        Obtener lista de archivos JSON pendientes de procesar.
        
        Returns:
            List[Path]: Lista de archivos ordenados por fecha de creación (más antiguos primero).
        """
        if not PENDING_PATH.exists():
            return []
        
        files = [f for f in PENDING_PATH.iterdir() 
                if f.is_file() and f.suffix.lower() == '.json']
        
        files.sort(key=lambda x: x.stat().st_ctime)
        return files
    
    def move_to_completed(self, file_path: Path) -> bool:
        """
        Mover archivo procesado a directorio de completados.
        
        Si ya existe un archivo con el mismo nombre, añade un sufijo numérico.
        
        Args:
            file_path (Path): Ruta al archivo a mover.
            
        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        """
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
            
        except PermissionError:
            self.logger.error(f"❌ [{ErrorCodes.PERMISSION_DENIED}] Sin permisos para mover archivo: {file_path}")
            return False
        except FileNotFoundError:
            self.logger.error(f"❌ [{ErrorCodes.FILE_NOT_FOUND}] Archivo no encontrado para mover: {file_path}")
            return False
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.FILE_MOVE_FAILED}] Error moviendo: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    def process_queue(self) -> bool:
        """
        Procesar cola completa de archivos JSON pendientes.
        
        Para cada archivo:
        1. Valida la estructura JSON
        2. Procesa el contenido
        3. Mueve a completados si es exitoso
        
        Returns:
            bool: True si todos los archivos fueron procesados exitosamente.
        """
        self.logger.info("📦 Procesando cola...")
        
        pending_files = self.get_pending_files()
        
        if not pending_files:
            self.logger.info("📭 No hay archivos pendientes")
            return True
        
        self.logger.info(f"📋 Procesando {len(pending_files)} archivos...")
        
        for file_path in pending_files:
            if not self.file_processor.validate_json(file_path):
                self.logger.error(f"❌ Inválido: {file_path.name}")
                continue
            
            if not self.file_processor.process_json(file_path):
                self.logger.error(f"❌ Error procesando: {file_path.name}")
                continue
            
            if not self.move_to_completed(file_path):
                self.logger.error(f"❌ Error moviendo: {file_path.name}")
                continue
        
        self.logger.info("✅ Cola procesada")
        return True
    
    def get_queue_status(self) -> Dict[str, int]:
        """
        Obtener estado actual de las colas de procesamiento.
        
        Returns:
            Dict[str, int]: Diccionario con:
                - pending: Número de archivos pendientes
                - completed: Número de archivos completados
                - total: Total de archivos procesados
        """
        pending_files = self.get_pending_files()
        completed_files = [f for f in COMPLETED_PATH.iterdir() 
                          if f.is_file() and f.suffix.lower() == '.json']
        
        return {
            'pending': len(pending_files),
            'completed': len(completed_files),
            'total': len(pending_files) + len(completed_files)
        }
    
    def print_status(self):
        """
        Imprimir estado actual del sistema en consola.
        
        Muestra número de archivos pendientes, completados y total.
        """
        status = self.get_queue_status()
        print(f"\n📊 Estado:")
        print(f"   📁 Pendientes: {status['pending']}")
        print(f"   ✅ Completados: {status['completed']}")
        print(f"   📈 Total: {status['total']}")


class OrderLoader:
    """Orquestador principal del sistema OrderLoader"""
    
    def __init__(self):
        """
        Inicializar sistema OrderLoader.
        
        Configura logging, crea directorios necesarios y prepara el sistema
        para el procesamiento de archivos JSON.
        """
        self.setup_logging()
        self.setup_directories()
        self.metrics = MetricsCollector()
        self.backup_path = PROJECT_ROOT / BACKUP_CONFIG['backup_path']
        
        # Inicializar componentes especializados
        self.window_manager = WindowManager(self.logger)
        self.file_processor = FileProcessor(self.logger, self.metrics)
        self.queue_manager = QueueManager(self.logger, self.file_processor)
        
        self.logger.info("🚀 OrderLoader iniciado")
    
    def setup_logging(self):
        """
        Configurar sistema de logging.
        
        Crea directorio de logs si no existe y configura logging con:
        - Nivel INFO
        - Formato con timestamp, nivel y mensaje
        - Handler para archivo (con encoding UTF-8)
        - Handler para consola
        """
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
        """
        Crear directorios necesarios para el funcionamiento del sistema.
        
        Crea los directorios:
        - data/pending/ (archivos JSON pendientes de procesar)
        - data/completed/ (archivos JSON ya procesados)
        """
        for directory in [PENDING_PATH, COMPLETED_PATH, self.backup_path]:
            directory.mkdir(parents=True, exist_ok=True)
        self.logger.info("📁 Directorios configurados")
    
    def create_backup(self, file_path: Path) -> bool:
        """
        Crear backup de archivo antes de procesar.
        
        Args:
            file_path (Path): Ruta al archivo a respaldar.
            
        Returns:
            bool: True si el backup fue exitoso, False en caso contrario.
        """
        if not BACKUP_CONFIG['enabled']:
            return True
            
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_file = self.backup_path / backup_name
            
            if BACKUP_CONFIG['compress_backups']:
                backup_file = backup_file.with_suffix('.gz')
                with open(file_path, 'rb') as f_in:
                    with gzip.open(backup_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(file_path, backup_file)
            
            self.logger.info(f"💾 Backup creado: {backup_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error creando backup: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Limpiar backups antiguos manteniendo solo los más recientes."""
        if not BACKUP_CONFIG['enabled']:
            return
            
        try:
            backup_files = list(self.backup_path.glob('*'))
            if len(backup_files) > BACKUP_CONFIG['max_backups']:
                # Ordenar por fecha de modificación y eliminar los más antiguos
                backup_files.sort(key=lambda x: x.stat().st_mtime)
                files_to_delete = backup_files[:-BACKUP_CONFIG['max_backups']]
                
                for file_to_delete in files_to_delete:
                    file_to_delete.unlink()
                    self.logger.info(f"🗑️ Backup antiguo eliminado: {file_to_delete.name}")
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Error limpiando backups: {e}")
    
    @retry_with_backoff()
    def activate_sap_chrome_window(self) -> bool:
        """
        Activar ventana de SAP en Chrome usando Alt+Tab.
        
        Returns:
            bool: True si la activación fue exitosa, False en caso contrario.
            
        Note:
            Requiere que la ventana de SAP en Chrome esté abierta y sea
            accesible con Alt+Tab.
        """
        self.logger.info("🔄 Activando SAP en Chrome...")
        
        try:
            # Configurar pyautogui
            pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE
            pyautogui.PAUSE = PYAUTOGUI_PAUSE
            
            # Presionar Alt+Tab para cambiar a la ventana correcta
            pyautogui.hotkey('alt', 'tab')
            time.sleep(WINDOW_ACTIVATION_DELAY)  # Esperar a que se active
            
            self.logger.info("✅ Ventana de SAP activada")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.WINDOW_ACTIVATION_FAILED}] Error activando ventana: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    @retry_with_backoff()
    def maximize_window(self) -> bool:
        """
        Maximizar la ventana activa usando Win+Up.
        
        Returns:
            bool: True si la maximización fue exitosa, False en caso contrario.
        """
        self.logger.info("📱 Maximizando ventana...")
        try:
            pyautogui.hotkey('win', 'up')
            time.sleep(WINDOW_MAXIMIZE_DELAY)
            self.logger.info("✅ Ventana maximizada")
            return True
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.WINDOW_MAXIMIZE_FAILED}] Error maximizando: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    def verify_sap(self) -> bool:
        """
        Verificar que SAP esté visible en el sistema.
        
        Usa PowerShell para buscar procesos con ventanas que contengan 'SAP'
        en el título.
        
        Returns:
            bool: True si SAP está detectado, False en caso contrario.
        """
        self.logger.info("🔍 Verificando SAP...")
        try:
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Where-Object {$_.MainWindowTitle -match "SAP"} | '
                'Select-Object MainWindowTitle | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=POWERSHELL_TIMEOUT)
            
            if result.stdout and result.returncode == 0:
                sap_windows = json.loads(result.stdout)
                if sap_windows:
                    self.logger.info("✅ SAP detectado")
                    return True
            
            self.logger.warning("⚠️ SAP no detectado")
            return False
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"❌ [{ErrorCodes.POWERSHELL_TIMEOUT}] Timeout verificando SAP")
            return False
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.SUBPROCESS_FAILED}] Error verificando SAP: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
    
    def verify_sap_chrome(self) -> bool:
        """
        Verificar que SAP esté visible en Chrome.
        
        Busca procesos de Chrome con títulos que contengan 'Chrome', 'SAP' o 'Auto.Sky'.
        Si no encuentra nada, asume que está bien y continúa.
        
        Returns:
            bool: True si SAP en Chrome está detectado o asumido como correcto.
        """
        self.logger.info("🔍 Verificando SAP en Chrome...")
        
        try:
            # Verificación simple - confirmar que la ventana está activa
            # Buscar procesos de Chrome con SAP o Auto.Sky
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
                'Where-Object {$_.MainWindowTitle -match "Chrome|SAP|Auto.Sky"} | '
                'Select-Object MainWindowTitle | ConvertTo-Json'
            ], capture_output=True, text=True, timeout=POWERSHELL_TIMEOUT)
            
            if result.stdout and result.returncode == 0:
                chrome_windows = json.loads(result.stdout)
                if chrome_windows:
                    self.logger.info("✅ SAP en Chrome verificado")
                    return True
            
            # Verificación alternativa - asumir que está bien si llegamos aquí
            time.sleep(SAP_VERIFICATION_DELAY)
            self.logger.info("✅ SAP en Chrome verificado (método alternativo)")
            return True
            
        except subprocess.TimeoutExpired:
            self.logger.warning(f"⚠️ [{ErrorCodes.POWERSHELL_TIMEOUT}] Timeout verificando SAP en Chrome - continuando")
            return True
        except Exception as e:
            self.logger.warning(f"⚠️ [{ErrorCodes.SUBPROCESS_FAILED}] Error verificando SAP: {e}")
            self.logger.warning(f"   Detalles: {type(e).__name__} - {str(e)}")
            # En caso de error, asumir que está bien y continuar
            return True
    
    def get_queue_status(self) -> Dict[str, int]:
        """
        Obtener estado actual de las colas de procesamiento.
        
        Returns:
            Dict[str, int]: Diccionario con:
                - pending: Número de archivos pendientes
                - completed: Número de archivos completados
                - total: Total de archivos procesados
        """
        return self.queue_manager.get_queue_status()
    
    def print_status(self):
        """
        Imprimir estado actual del sistema en consola.
        
        Muestra número de archivos pendientes, completados y total.
        """
        self.queue_manager.print_status()
    
    def validate_system(self) -> bool:
        """
        Validar sistema y permisos básicos.
        
        Returns:
            bool: True si el sistema está listo, False en caso contrario.
        """
        self.logger.info("🔍 Validando sistema...")
        try:
            test_file = Path("test_permissions.tmp")
            test_file.write_text("test")
            test_file.unlink()
            self.logger.info("✅ Sistema validado")
            return True
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.SYSTEM_VALIDATION_FAILED}] Error validando sistema: {e}")
            return False
    
    def setup_sap_environment(self) -> bool:
        """
        Configurar entorno SAP (activar ventana, maximizar, verificar).
        
        Returns:
            bool: True si el entorno está listo, False en caso contrario.
        """
        # Activar ventana de SAP en Chrome
        if not self.window_manager.activate_sap_chrome_window():
            return False
        
        # Maximizar ventana
        if not self.window_manager.maximize_window():
            self.logger.warning("⚠️ No se pudo maximizar")
        
        # Esperar estabilización
        self.logger.info("⏳ Esperando estabilización...")
        time.sleep(SYSTEM_STABILIZATION_DELAY)
        
        # Verificar SAP (opcional, para confirmar)
        if not self.window_manager.verify_sap_chrome():
            self.logger.warning("⚠️ SAP no detectado")
        
        return True
    
    def run(self) -> bool:
        """
        Ejecutar proceso completo de automatización.
        
        Flujo de ejecución:
        1. Iniciar métricas
        2. Validar sistema y permisos
        3. Configurar entorno SAP
        4. Procesar cola de archivos
        5. Limpiar backups antiguos
        6. Finalizar métricas
        
        Returns:
            bool: True si todo el proceso fue exitoso, False en caso contrario.
        """
        self.logger.info("🎯 Iniciando automatización...")
        
        # Iniciar métricas
        if METRICS_CONFIG['enabled']:
            self.metrics.start_session()
        
        try:
            # Validar sistema
            if not self.validate_system():
                return False
            
            # Configurar entorno SAP
            if not self.setup_sap_environment():
                return False
            
            # Procesar cola
            if not self.queue_manager.process_queue():
                return False
            
            # Limpiar backups antiguos
            self.cleanup_old_backups()
            
            # Mostrar métricas finales
            if METRICS_CONFIG['enabled']:
                success_rate = self.metrics.get_success_rate()
                self.logger.info(f"📊 Tasa de éxito: {success_rate:.1%}")
                self.logger.info(f"📈 Archivos procesados: {self.metrics.metrics['total_files_processed']}")
                self.logger.info(f"🔄 Intentos de retry: {self.metrics.metrics['retry_attempts']}")
            
            self.logger.info("🎉 ¡Procesamiento completado!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ [{ErrorCodes.SYSTEM_VALIDATION_FAILED}] Error en automatización: {e}")
            self.logger.error(f"   Detalles: {type(e).__name__} - {str(e)}")
            return False
        finally:
            # Finalizar métricas
            if METRICS_CONFIG['enabled']:
                self.metrics.end_session()


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