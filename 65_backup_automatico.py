import os
import shutil
import zipfile
import json
from datetime import datetime, timedelta
import hashlib
import schedule
import time
import threading

class BackupManager:
    def __init__(self):
        self.config_file = "backup_config.json"
        self.backup_log = "backup_log.json"
        self.config = self.load_config()
        self.running = False
        self.scheduler_thread = None
    
    def load_config(self):
        """Cargar configuración de backup"""
        default_config = {
            "backup_sources": [],
            "backup_destination": "./backups",
            "compression": True,
            "schedule": {
                "enabled": False,
                "frequency": "daily",
                "time": "02:00"
            },
            "retention": {
                "keep_daily": 7,
                "keep_weekly": 4,
                "keep_monthly": 12
            },
            "exclude_patterns": [
                "*.tmp", "*.log", "__pycache__", ".git", "node_modules"
            ]
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Combinar con configuración por defecto
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            else:
                self.save_config(default_config)
                return default_config
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return default_config
    
    def save_config(self, config=None):
        """Guardar configuración"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            print("Configuración guardada")
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def add_backup_source(self, path):
        """Agregar directorio/archivo a respaldar"""
        if not os.path.exists(path):
            print(f"Error: La ruta {path} no existe")
            return False
        
        abs_path = os.path.abspath(path)
        if abs_path not in self.config["backup_sources"]:
            self.config["backup_sources"].append(abs_path)
            self.save_config()
            print(f"Agregado: {abs_path}")
            return True
        else:
            print("La ruta ya está en la lista de backup")
            return False
    
    def remove_backup_source(self, path):
        """Remover directorio/archivo de backup"""
        abs_path = os.path.abspath(path)
        if abs_path in self.config["backup_sources"]:
            self.config["backup_sources"].remove(abs_path)
            self.save_config()
            print(f"Removido: {abs_path}")
            return True
        else:
            print("La ruta no está en la lista de backup")
            return False
    
    def should_exclude(self, file_path):
        """Verificar si un archivo debe ser excluido"""
        import fnmatch
        
        file_name = os.path.basename(file_path)
        
        for pattern in self.config["exclude_patterns"]:
            if fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(file_path, pattern):
                return True
        
        return False
    
    def calculate_file_hash(self, file_path):
        """Calcular hash MD5 de un archivo"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None
    
    def create_backup(self, backup_name=None):
        """Crear backup completo"""
        if not self.config["backup_sources"]:
            print("No hay fuentes de backup configuradas")
            return False
        
        # Crear nombre de backup
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
        
        # Crear directorio de destino
        backup_dest = self.config["backup_destination"]
        os.makedirs(backup_dest, exist_ok=True)
        
        if self.config["compression"]:
            backup_path = os.path.join(backup_dest, f"{backup_name}.zip")
            return self._create_compressed_backup(backup_path, backup_name)
        else:
            backup_path = os.path.join(backup_dest, backup_name)
            return self._create_folder_backup(backup_path, backup_name)
    
    def _create_compressed_backup(self, backup_path, backup_name):
        """Crear backup comprimido"""
        try:
            print(f"Creando backup comprimido: {backup_path}")
            
            backup_info = {
                "name": backup_name,
                "timestamp": datetime.now().isoformat(),
                "type": "compressed",
                "files": [],
                "total_size": 0,
                "compressed_size": 0
            }
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for source in self.config["backup_sources"]:
                    if os.path.isfile(source):
                        if not self.should_exclude(source):
                            file_size = os.path.getsize(source)
                            file_hash = self.calculate_file_hash(source)
                            
                            arcname = os.path.relpath(source)
                            zipf.write(source, arcname)
                            
                            backup_info["files"].append({
                                "path": source,
                                "size": file_size,
                                "hash": file_hash,
                                "arcname": arcname
                            })
                            backup_info["total_size"] += file_size
                            
                            print(f"  Agregado: {source}")
                    
                    elif os.path.isdir(source):
                        for root, dirs, files in os.walk(source):
                            # Filtrar directorios excluidos
                            dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]
                            
                            for file in files:
                                file_path = os.path.join(root, file)
                                
                                if not self.should_exclude(file_path):
                                    try:
                                        file_size = os.path.getsize(file_path)
                                        file_hash = self.calculate_file_hash(file_path)
                                        
                                        arcname = os.path.relpath(file_path, os.path.dirname(source))
                                        zipf.write(file_path, arcname)
                                        
                                        backup_info["files"].append({
                                            "path": file_path,
                                            "size": file_size,
                                            "hash": file_hash,
                                            "arcname": arcname
                                        })
                                        backup_info["total_size"] += file_size
                                        
                                        print(f"  Agregado: {file_path}")
                                        
                                    except Exception as e:
                                        print(f"  Error procesando {file_path}: {e}")
            
            # Obtener tamaño del archivo comprimido
            backup_info["compressed_size"] = os.path.getsize(backup_path)
            compression_ratio = (1 - backup_info["compressed_size"] / backup_info["total_size"]) * 100
            
            print(f"\n✅ Backup completado:")
            print(f"  Archivos: {len(backup_info['files'])}")
            print(f"  Tamaño original: {self.format_size(backup_info['total_size'])}")
            print(f"  Tamaño comprimido: {self.format_size(backup_info['compressed_size'])}")
            print(f"  Compresión: {compression_ratio:.1f}%")
            
            # Guardar información del backup
            self.log_backup(backup_info)
            
            return True
            
        except Exception as e:
            print(f"Error creando backup: {e}")
            return False
    
    def _create_folder_backup(self, backup_path, backup_name):
        """Crear backup en carpeta"""
        try:
            print(f"Creando backup en carpeta: {backup_path}")
            os.makedirs(backup_path, exist_ok=True)
            
            backup_info = {
                "name": backup_name,
                "timestamp": datetime.now().isoformat(),
                "type": "folder",
                "files": [],
                "total_size": 0
            }
            
            for source in self.config["backup_sources"]:
                if os.path.isfile(source):
                    if not self.should_exclude(source):
                        dest_file = os.path.join(backup_path, os.path.basename(source))
                        shutil.copy2(source, dest_file)
                        
                        file_size = os.path.getsize(source)
                        file_hash = self.calculate_file_hash(source)
                        
                        backup_info["files"].append({
                            "path": source,
                            "size": file_size,
                            "hash": file_hash
                        })
                        backup_info["total_size"] += file_size
                        
                        print(f"  Copiado: {source}")
                
                elif os.path.isdir(source):
                    dest_dir = os.path.join(backup_path, os.path.basename(source))
                    
                    def ignore_patterns(dir, files):
                        ignored = []
                        for file in files:
                            file_path = os.path.join(dir, file)
                            if self.should_exclude(file_path):
                                ignored.append(file)
                        return ignored
                    
                    shutil.copytree(source, dest_dir, ignore=ignore_patterns)
                    
                    # Contar archivos copiados
                    for root, dirs, files in os.walk(dest_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            original_path = file_path.replace(dest_dir, source)
                            
                            file_size = os.path.getsize(file_path)
                            file_hash = self.calculate_file_hash(file_path)
                            
                            backup_info["files"].append({
                                "path": original_path,
                                "size": file_size,
                                "hash": file_hash
                            })
                            backup_info["total_size"] += file_size
                    
                    print(f"  Copiado directorio: {source}")
            
            print(f"\n✅ Backup completado:")
            print(f"  Archivos: {len(backup_info['files'])}")
            print(f"  Tamaño total: {self.format_size(backup_info['total_size'])}")
            
            # Guardar información del backup
            self.log_backup(backup_info)
            
            return True
            
        except Exception as e:
            print(f"Error creando backup: {e}")
            return False
    
    def log_backup(self, backup_info):
        """Registrar información del backup"""
        try:
            log_data = []
            if os.path.exists(self.backup_log):
                with open(self.backup_log, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
            
            log_data.append(backup_info)
            
            with open(self.backup_log, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error guardando log: {e}")
    
    def list_backups(self):
        """Listar backups existentes"""
        try:
            if not os.path.exists(self.backup_log):
                print("No hay backups registrados")
                return []
            
            with open(self.backup_log, 'r', encoding='utf-8') as f:
                backups = json.load(f)
            
            if not backups:
                print("No hay backups registrados")
                return []
            
            print(f"\n=== BACKUPS EXISTENTES ({len(backups)}) ===")
            for i, backup in enumerate(backups, 1):
                timestamp = datetime.fromisoformat(backup['timestamp'])
                size_str = self.format_size(backup.get('compressed_size', backup.get('total_size', 0)))
                
                print(f"{i:2d}. {backup['name']}")
                print(f"    Fecha: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"    Tipo: {backup['type']}")
                print(f"    Archivos: {len(backup['files'])}")
                print(f"    Tamaño: {size_str}")
                print()
            
            return backups
            
        except Exception as e:
            print(f"Error listando backups: {e}")
            return []
    
    def restore_backup(self, backup_name, restore_path=None):
        """Restaurar un backup"""
        try:
            # Buscar backup en el log
            if not os.path.exists(self.backup_log):
                print("No hay backups registrados")
                return False
            
            with open(self.backup_log, 'r', encoding='utf-8') as f:
                backups = json.load(f)
            
            backup_info = None
            for backup in backups:
                if backup['name'] == backup_name:
                    backup_info = backup
                    break
            
            if not backup_info:
                print(f"Backup '{backup_name}' no encontrado")
                return False
            
            # Determinar ruta de restauración
            if not restore_path:
                restore_path = f"./restored_{backup_name}"
            
            os.makedirs(restore_path, exist_ok=True)
            
            if backup_info['type'] == 'compressed':
                backup_file = os.path.join(self.config["backup_destination"], f"{backup_name}.zip")
                return self._restore_compressed_backup(backup_file, restore_path)
            else:
                backup_folder = os.path.join(self.config["backup_destination"], backup_name)
                return self._restore_folder_backup(backup_folder, restore_path)
                
        except Exception as e:
            print(f"Error restaurando backup: {e}")
            return False
    
    def _restore_compressed_backup(self, backup_file, restore_path):
        """Restaurar backup comprimido"""
        try:
            if not os.path.exists(backup_file):
                print(f"Archivo de backup no encontrado: {backup_file}")
                return False
            
            print(f"Restaurando desde: {backup_file}")
            print(f"Destino: {restore_path}")
            
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(restore_path)
            
            print("✅ Backup restaurado exitosamente")
            return True
            
        except Exception as e:
            print(f"Error restaurando backup comprimido: {e}")
            return False
    
    def _restore_folder_backup(self, backup_folder, restore_path):
        """Restaurar backup de carpeta"""
        try:
            if not os.path.exists(backup_folder):
                print(f"Carpeta de backup no encontrada: {backup_folder}")
                return False
            
            print(f"Restaurando desde: {backup_folder}")
            print(f"Destino: {restore_path}")
            
            shutil.copytree(backup_folder, restore_path, dirs_exist_ok=True)
            
            print("✅ Backup restaurado exitosamente")
            return True
            
        except Exception as e:
            print(f"Error restaurando backup de carpeta: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Limpiar backups antiguos según política de retención"""
        try:
            if not os.path.exists(self.backup_log):
                print("No hay backups para limpiar")
                return
            
            with open(self.backup_log, 'r', encoding='utf-8') as f:
                backups = json.load(f)
            
            if not backups:
                print("No hay backups para limpiar")
                return
            
            # Ordenar por fecha
            backups.sort(key=lambda x: x['timestamp'], reverse=True)
            
            retention = self.config["retention"]
            now = datetime.now()
            
            backups_to_keep = []
            backups_to_delete = []
            
            daily_count = 0
            weekly_count = 0
            monthly_count = 0
            
            for backup in backups:
                backup_date = datetime.fromisoformat(backup['timestamp'])
                age_days = (now - backup_date).days
                
                keep = False
                
                # Mantener backups diarios
                if age_days < retention["keep_daily"] and daily_count < retention["keep_daily"]:
                    keep = True
                    daily_count += 1
                
                # Mantener backups semanales
                elif age_days < retention["keep_weekly"] * 7 and weekly_count < retention["keep_weekly"]:
                    if backup_date.weekday() == 0:  # Lunes
                        keep = True
                        weekly_count += 1
                
                # Mantener backups mensuales
                elif age_days < retention["keep_monthly"] * 30 and monthly_count < retention["keep_monthly"]:
                    if backup_date.day == 1:  # Primer día del mes
                        keep = True
                        monthly_count += 1
                
                if keep:
                    backups_to_keep.append(backup)
                else:
                    backups_to_delete.append(backup)
            
            # Eliminar backups antiguos
            for backup in backups_to_delete:
                backup_name = backup['name']
                
                if backup['type'] == 'compressed':
                    backup_file = os.path.join(self.config["backup_destination"], f"{backup_name}.zip")
                    if os.path.exists(backup_file):
                        os.remove(backup_file)
                        print(f"Eliminado: {backup_file}")
                else:
                    backup_folder = os.path.join(self.config["backup_destination"], backup_name)
                    if os.path.exists(backup_folder):
                        shutil.rmtree(backup_folder)
                        print(f"Eliminado: {backup_folder}")
            
            # Actualizar log
            with open(self.backup_log, 'w', encoding='utf-8') as f:
                json.dump(backups_to_keep, f, indent=2, ensure_ascii=False)
            
            print(f"Limpieza completada: {len(backups_to_delete)} backups eliminados")
            
        except Exception as e:
            print(f"Error limpiando backups: {e}")
    
    def format_size(self, size_bytes):
        """Formatear tamaño en bytes a formato legible"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def setup_schedule(self):
        """Configurar programación automática"""
        print("\n=== CONFIGURAR PROGRAMACIÓN ===")
        
        enabled = input("¿Habilitar backup automático? (s/n): ").lower() == 's'
        self.config["schedule"]["enabled"] = enabled
        
        if enabled:
            print("Frecuencias disponibles:")
            print("1. Diario")
            print("2. Semanal")
            print("3. Mensual")
            
            freq_choice = input("Selecciona frecuencia (1-3): ")
            frequencies = {"1": "daily", "2": "weekly", "3": "monthly"}
            
            if freq_choice in frequencies:
                self.config["schedule"]["frequency"] = frequencies[freq_choice]
                
                time_input = input("Hora de ejecución (HH:MM, ej: 02:00): ")
                if len(time_input) == 5 and ':' in time_input:
                    self.config["schedule"]["time"] = time_input
                
                self.save_config()
                print("Programación configurada")
                
                # Iniciar scheduler
                self.start_scheduler()
            else:
                print("Opción no válida")
        else:
            self.save_config()
            self.stop_scheduler()
    
    def start_scheduler(self):
        """Iniciar programador de backups"""
        if not self.config["schedule"]["enabled"]:
            print("Programación no habilitada")
            return
        
        schedule.clear()
        
        frequency = self.config["schedule"]["frequency"]
        time_str = self.config["schedule"]["time"]
        
        if frequency == "daily":
            schedule.every().day.at(time_str).do(self.scheduled_backup)
        elif frequency == "weekly":
            schedule.every().monday.at(time_str).do(self.scheduled_backup)
        elif frequency == "monthly":
            schedule.every().month.at(time_str).do(self.scheduled_backup)
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print(f"Programador iniciado: {frequency} a las {time_str}")
    
    def stop_scheduler(self):
        """Detener programador"""
        self.running = False
        schedule.clear()
        print("Programador detenido")
    
    def _run_scheduler(self):
        """Ejecutar programador en hilo separado"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
    
    def scheduled_backup(self):
        """Ejecutar backup programado"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ejecutando backup programado...")
        success = self.create_backup()
        
        if success:
            print("Backup programado completado exitosamente")
            # Limpiar backups antiguos después del backup
            self.cleanup_old_backups()
        else:
            print("Error en backup programado")

def main():
    backup_manager = BackupManager()
    
    while True:
        print("\n=== GESTOR DE BACKUPS ===")
        print("1. Agregar fuente de backup")
        print("2. Remover fuente de backup")
        print("3. Ver configuración")
        print("4. Crear backup ahora")
        print("5. Listar backups")
        print("6. Restaurar backup")
        print("7. Limpiar backups antiguos")
        print("8. Configurar programación")
        print("9. Iniciar/Detener programador")
        print("10. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            path = input("Ruta del directorio/archivo a respaldar: ")
            backup_manager.add_backup_source(path)
            
        elif opcion == "2":
            path = input("Ruta a remover: ")
            backup_manager.remove_backup_source(path)
            
        elif opcion == "3":
            print("\n=== CONFIGURACIÓN ACTUAL ===")
            print(f"Fuentes de backup: {len(backup_manager.config['backup_sources'])}")
            for source in backup_manager.config['backup_sources']:
                print(f"  - {source}")
            print(f"Destino: {backup_manager.config['backup_destination']}")
            print(f"Compresión: {'Sí' if backup_manager.config['compression'] else 'No'}")
            print(f"Programación: {'Habilitada' if backup_manager.config['schedule']['enabled'] else 'Deshabilitada'}")
            
        elif opcion == "4":
            name = input("Nombre del backup (opcional): ") or None
            backup_manager.create_backup(name)
            
        elif opcion == "5":
            backup_manager.list_backups()
            
        elif opcion == "6":
            backups = backup_manager.list_backups()
            if backups:
                backup_name = input("Nombre del backup a restaurar: ")
                restore_path = input("Ruta de restauración (opcional): ") or None
                backup_manager.restore_backup(backup_name, restore_path)
                
        elif opcion == "7":
            backup_manager.cleanup_old_backups()
            
        elif opcion == "8":
            backup_manager.setup_schedule()
            
        elif opcion == "9":
            if backup_manager.running:
                backup_manager.stop_scheduler()
            else:
                backup_manager.start_scheduler()
                
        elif opcion == "10":
            backup_manager.stop_scheduler()
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
