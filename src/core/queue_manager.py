#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Colas Simple - OrderLoader 2.0
Maneja el procesamiento secuencial de archivos en cola
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)

class QueueManager:
    """Gestor simple de colas para procesamiento de archivos"""
    
    def __init__(self, base_path: str = "queues"):
        self.base_path = Path(base_path)
        self.pending_dir = self.base_path / "pending"
        self.completed_dir = self.base_path / "completed"
        
        # Crear directorios si no existen
        self._create_directories()
        
    def _create_directories(self):
        """Crea los directorios necesarios"""
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.completed_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear archivos .gitkeep para mantener las carpetas en git
        (self.pending_dir / ".gitkeep").touch(exist_ok=True)
        (self.completed_dir / ".gitkeep").touch(exist_ok=True)
        
        logger.info(f"Directorios de cola creados: {self.base_path}")
    
    def get_pending_files(self) -> List[Path]:
        """Obtiene lista de archivos pendientes en orden FIFO"""
        if not self.pending_dir.exists():
            return []
        
        # Obtener archivos (excluyendo .gitkeep)
        files = [f for f in self.pending_dir.iterdir() 
                if f.is_file() and f.name != ".gitkeep"]
        
        # Ordenar por fecha de creación (FIFO)
        files.sort(key=lambda x: x.stat().st_ctime)
        
        return files
    
    def has_pending_files(self) -> bool:
        """Verifica si hay archivos pendientes"""
        return len(self.get_pending_files()) > 0
    
    def get_next_file(self) -> Optional[Path]:
        """Obtiene el siguiente archivo a procesar"""
        files = self.get_pending_files()
        return files[0] if files else None
    
    def move_to_completed(self, file_path: Path) -> bool:
        """Mueve archivo procesado a carpeta completed"""
        try:
            if not file_path.exists():
                logger.error(f"Archivo no encontrado: {file_path}")
                return False
            
            # Crear nombre único para evitar conflictos
            filename = file_path.name
            counter = 1
            while (self.completed_dir / filename).exists():
                name, ext = os.path.splitext(file_path.name)
                filename = f"{name}_{counter}{ext}"
                counter += 1
            
            destination = self.completed_dir / filename
            shutil.move(str(file_path), str(destination))
            
            logger.info(f"✅ Archivo movido a completados: {file_path.name} → {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al mover archivo a completados: {e}")
            return False
    
    def get_queue_status(self) -> dict:
        """Obtiene estado actual de las colas"""
        pending_count = len(self.get_pending_files())
        completed_count = len([f for f in self.completed_dir.iterdir() 
                             if f.is_file() and f.name != ".gitkeep"])
        
        return {
            'pending': pending_count,
            'completed': completed_count,
            'total_processed': completed_count
        }
    
    def print_queue_status(self):
        """Imprime estado de las colas"""
        status = self.get_queue_status()
        print(f"\n📊 Estado de Colas:")
        print(f"   📁 Pendientes: {status['pending']}")
        print(f"   ✅ Completados: {status['completed']}")
        print(f"   📈 Total procesados: {status['total_processed']}")
