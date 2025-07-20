import psutil
import time
import json
from datetime import datetime, timedelta
import os
import platform

class SystemMonitor:
    def __init__(self):
        self.monitoring = False
        self.data_history = []
        self.alerts = []
        self.thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_percent': 90,
            'temperature': 70
        }
    
    def get_system_info(self):
        """Obtener información básica del sistema"""
        try:
            info = {
                'platform': platform.platform(),
                'system': platform.system(),
                'processor': platform.processor(),
                'architecture': platform.architecture()[0],
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print("\n=== INFORMACIÓN DEL SISTEMA ===")
            for key, value in info.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            
            return info
            
        except Exception as e:
            print(f"Error obteniendo información del sistema: {e}")
            return None
    
    def get_cpu_info(self):
        """Obtener información de CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            print("\n=== INFORMACIÓN DE CPU ===")
            print(f"Uso de CPU: {cpu_percent}%")
            print(f"Núcleos físicos: {cpu_count}")
            print(f"Núcleos lógicos: {cpu_count_logical}")
            
            if cpu_freq:
                print(f"Frecuencia actual: {cpu_freq.current:.2f} MHz")
                print(f"Frecuencia mínima: {cpu_freq.min:.2f} MHz")
                print(f"Frecuencia máxima: {cpu_freq.max:.2f} MHz")
            
            # Uso por núcleo
            cpu_per_core = psutil.cpu_percent(percpu=True, interval=1)
            print("\nUso por núcleo:")
            for i, percent in enumerate(cpu_per_core):
                bar = '█' * int(percent // 5)
                print(f"Core {i}: {percent:5.1f}% {bar}")
            
            # Verificar alerta
            if cpu_percent > self.thresholds['cpu_percent']:
                alert = f"⚠️  ALERTA: CPU al {cpu_percent}% (umbral: {self.thresholds['cpu_percent']}%)"
                print(alert)
                self.alerts.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'CPU',
                    'message': alert,
                    'value': cpu_percent
                })
            
            return {
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'cpu_count_logical': cpu_count_logical,
                'cpu_freq': cpu_freq._asdict() if cpu_freq else None,
                'cpu_per_core': cpu_per_core
            }
            
        except Exception as e:
            print(f"Error obteniendo información de CPU: {e}")
            return None
    
    def get_memory_info(self):
        """Obtener información de memoria"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            print("\n=== INFORMACIÓN DE MEMORIA ===")
            print(f"Memoria total: {self.bytes_to_gb(memory.total):.2f} GB")
            print(f"Memoria disponible: {self.bytes_to_gb(memory.available):.2f} GB")
            print(f"Memoria usada: {self.bytes_to_gb(memory.used):.2f} GB")
            print(f"Porcentaje usado: {memory.percent}%")
            
            # Barra visual
            bar_length = 50
            used_bar = int((memory.percent / 100) * bar_length)
            bar = '█' * used_bar + '░' * (bar_length - used_bar)
            print(f"[{bar}] {memory.percent}%")
            
            print(f"\nSwap total: {self.bytes_to_gb(swap.total):.2f} GB")
            print(f"Swap usado: {self.bytes_to_gb(swap.used):.2f} GB")
            print(f"Swap libre: {self.bytes_to_gb(swap.free):.2f} GB")
            print(f"Porcentaje swap: {swap.percent}%")
            
            # Verificar alerta
            if memory.percent > self.thresholds['memory_percent']:
                alert = f"⚠️  ALERTA: Memoria al {memory.percent}% (umbral: {self.thresholds['memory_percent']}%)"
                print(alert)
                self.alerts.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'MEMORY',
                    'message': alert,
                    'value': memory.percent
                })
            
            return {
                'memory': memory._asdict(),
                'swap': swap._asdict()
            }
            
        except Exception as e:
            print(f"Error obteniendo información de memoria: {e}")
            return None
    
    def get_disk_info(self):
        """Obtener información de discos"""
        try:
            print("\n=== INFORMACIÓN DE DISCOS ===")
            
            partitions = psutil.disk_partitions()
            disk_info = []
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    print(f"\nDispositivo: {partition.device}")
                    print(f"Punto de montaje: {partition.mountpoint}")
                    print(f"Sistema de archivos: {partition.fstype}")
                    print(f"Tamaño total: {self.bytes_to_gb(usage.total):.2f} GB")
                    print(f"Usado: {self.bytes_to_gb(usage.used):.2f} GB")
                    print(f"Libre: {self.bytes_to_gb(usage.free):.2f} GB")
                    print(f"Porcentaje usado: {usage.percent}%")
                    
                    # Barra visual
                    bar_length = 30
                    used_bar = int((usage.percent / 100) * bar_length)
                    bar = '█' * used_bar + '░' * (bar_length - used_bar)
                    print(f"[{bar}] {usage.percent}%")
                    
                    # Verificar alerta
                    if usage.percent > self.thresholds['disk_percent']:
                        alert = f"⚠️  ALERTA: Disco {partition.device} al {usage.percent}% (umbral: {self.thresholds['disk_percent']}%)"
                        print(alert)
                        self.alerts.append({
                            'timestamp': datetime.now().isoformat(),
                            'type': 'DISK',
                            'message': alert,
                            'value': usage.percent,
                            'device': partition.device
                        })
                    
                    disk_info.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'usage': usage._asdict()
                    })
                    
                except PermissionError:
                    print(f"Sin permisos para acceder a {partition.mountpoint}")
                    continue
            
            return disk_info
            
        except Exception as e:
            print(f"Error obteniendo información de discos: {e}")
            return None
    
    def get_network_info(self):
        """Obtener información de red"""
        try:
            print("\n=== INFORMACIÓN DE RED ===")
            
            # Estadísticas de red
            net_io = psutil.net_io_counters()
            print(f"Bytes enviados: {self.bytes_to_gb(net_io.bytes_sent):.2f} GB")
            print(f"Bytes recibidos: {self.bytes_to_gb(net_io.bytes_recv):.2f} GB")
            print(f"Paquetes enviados: {net_io.packets_sent:,}")
            print(f"Paquetes recibidos: {net_io.packets_recv:,}")
            
            # Conexiones de red
            connections = psutil.net_connections()
            established = len([c for c in connections if c.status == 'ESTABLISHED'])
            listening = len([c for c in connections if c.status == 'LISTEN'])
            
            print(f"\nConexiones establecidas: {established}")
            print(f"Puertos en escucha: {listening}")
            print(f"Total de conexiones: {len(connections)}")
            
            # Interfaces de red
            net_if_addrs = psutil.net_if_addrs()
            print(f"\nInterfaces de red:")
            for interface, addresses in net_if_addrs.items():
                print(f"  {interface}:")
                for addr in addresses:
                    if addr.family.name == 'AF_INET':
                        print(f"    IPv4: {addr.address}")
                    elif addr.family.name == 'AF_INET6':
                        print(f"    IPv6: {addr.address}")
            
            return {
                'net_io': net_io._asdict(),
                'connections': {
                    'established': established,
                    'listening': listening,
                    'total': len(connections)
                },
                'interfaces': {iface: [addr._asdict() for addr in addrs] 
                             for iface, addrs in net_if_addrs.items()}
            }
            
        except Exception as e:
            print(f"Error obteniendo información de red: {e}")
            return None
    
    def get_processes_info(self):
        """Obtener información de procesos"""
        try:
            print("\n=== PROCESOS TOP ===")
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Ordenar por uso de CPU
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            print("Top 10 procesos por CPU:")
            print(f"{'PID':<8} {'NOMBRE':<20} {'CPU%':<8} {'MEM%':<8}")
            print("-" * 50)
            
            for proc in processes[:10]:
                pid = proc['pid']
                name = proc['name'][:18] if proc['name'] else 'N/A'
                cpu = proc['cpu_percent'] or 0
                mem = proc['memory_percent'] or 0
                print(f"{pid:<8} {name:<20} {cpu:<8.1f} {mem:<8.1f}")
            
            # Ordenar por uso de memoria
            processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
            
            print(f"\nTop 10 procesos por memoria:")
            print(f"{'PID':<8} {'NOMBRE':<20} {'CPU%':<8} {'MEM%':<8}")
            print("-" * 50)
            
            for proc in processes[:10]:
                pid = proc['pid']
                name = proc['name'][:18] if proc['name'] else 'N/A'
                cpu = proc['cpu_percent'] or 0
                mem = proc['memory_percent'] or 0
                print(f"{pid:<8} {name:<20} {cpu:<8.1f} {mem:<8.1f}")
            
            return processes[:20]  # Retornar top 20
            
        except Exception as e:
            print(f"Error obteniendo información de procesos: {e}")
            return None
    
    def get_temperature_info(self):
        """Obtener información de temperatura (si está disponible)"""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    print("\n=== TEMPERATURAS ===")
                    for name, entries in temps.items():
                        print(f"{name}:")
                        for entry in entries:
                            temp = entry.current
                            print(f"  {entry.label or 'N/A'}: {temp}°C")
                            
                            # Verificar alerta
                            if temp > self.thresholds['temperature']:
                                alert = f"⚠️  ALERTA: Temperatura {name} a {temp}°C (umbral: {self.thresholds['temperature']}°C)"
                                print(alert)
                                self.alerts.append({
                                    'timestamp': datetime.now().isoformat(),
                                    'type': 'TEMPERATURE',
                                    'message': alert,
                                    'value': temp,
                                    'sensor': name
                                })
                    
                    return temps
                else:
                    print("\n=== TEMPERATURAS ===")
                    print("No hay sensores de temperatura disponibles")
            else:
                print("\n=== TEMPERATURAS ===")
                print("Información de temperatura no soportada en este sistema")
            
            return None
            
        except Exception as e:
            print(f"Error obteniendo información de temperatura: {e}")
            return None
    
    def bytes_to_gb(self, bytes_value):
        """Convertir bytes a GB"""
        return bytes_value / (1024**3)
    
    def monitor_continuous(self, interval=5, duration=60):
        """Monitoreo continuo del sistema"""
        print(f"\n=== MONITOREO CONTINUO ===")
        print(f"Intervalo: {interval} segundos")
        print(f"Duración: {duration} segundos")
        print("Presiona Ctrl+C para detener\n")
        
        self.monitoring = True
        start_time = time.time()
        
        try:
            while self.monitoring and (time.time() - start_time) < duration:
                timestamp = datetime.now()
                
                # Recopilar datos
                data = {
                    'timestamp': timestamp.isoformat(),
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_percent': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent
                }
                
                self.data_history.append(data)
                
                # Mostrar datos en tiempo real
                print(f"\r{timestamp.strftime('%H:%M:%S')} - "
                      f"CPU: {data['cpu_percent']:5.1f}% | "
                      f"MEM: {data['memory_percent']:5.1f}% | "
                      f"DISK: {data['disk_percent']:5.1f}%", end='')
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nMonitoreo detenido por el usuario")
        
        self.monitoring = False
        print(f"\nMonitoreo completado. {len(self.data_history)} muestras recopiladas")
    
    def show_alerts(self):
        """Mostrar alertas generadas"""
        if not self.alerts:
            print("No hay alertas generadas")
            return
        
        print(f"\n=== ALERTAS ({len(self.alerts)}) ===")
        for alert in self.alerts[-10:]:  # Mostrar últimas 10
            timestamp = datetime.fromisoformat(alert['timestamp']).strftime('%H:%M:%S')
            print(f"[{timestamp}] {alert['message']}")
    
    def save_report(self, filename="system_report.json"):
        """Guardar reporte del sistema"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'system_info': self.get_system_info(),
                'alerts': self.alerts,
                'monitoring_history': self.data_history[-100:],  # Últimas 100 muestras
                'thresholds': self.thresholds
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"Reporte guardado en {filename}")
            
        except Exception as e:
            print(f"Error guardando reporte: {e}")
    
    def configure_thresholds(self):
        """Configurar umbrales de alerta"""
        print("\n=== CONFIGURAR UMBRALES ===")
        print("Umbrales actuales:")
        for key, value in self.thresholds.items():
            print(f"  {key}: {value}%")
        
        try:
            for key in self.thresholds:
                new_value = input(f"Nuevo umbral para {key} (actual: {self.thresholds[key]}): ")
                if new_value:
                    self.thresholds[key] = float(new_value)
            
            print("Umbrales actualizados")
            
        except ValueError:
            print("Error: Los umbrales deben ser números")

def main():
    monitor = SystemMonitor()
    
    while True:
        print("\n=== MONITOR DEL SISTEMA ===")
        print("1. Información del sistema")
        print("2. Información de CPU")
        print("3. Información de memoria")
        print("4. Información de discos")
        print("5. Información de red")
        print("6. Información de procesos")
        print("7. Información de temperatura")
        print("8. Monitoreo continuo")
        print("9. Ver alertas")
        print("10. Configurar umbrales")
        print("11. Guardar reporte")
        print("12. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            monitor.get_system_info()
        elif opcion == "2":
            monitor.get_cpu_info()
        elif opcion == "3":
            monitor.get_memory_info()
        elif opcion == "4":
            monitor.get_disk_info()
        elif opcion == "5":
            monitor.get_network_info()
        elif opcion == "6":
            monitor.get_processes_info()
        elif opcion == "7":
            monitor.get_temperature_info()
        elif opcion == "8":
            try:
                interval = int(input("Intervalo en segundos (default: 5): ") or "5")
                duration = int(input("Duración en segundos (default: 60): ") or "60")
                monitor.monitor_continuous(interval, duration)
            except ValueError:
                print("Los valores deben ser números")
        elif opcion == "9":
            monitor.show_alerts()
        elif opcion == "10":
            monitor.configure_thresholds()
        elif opcion == "11":
            filename = input("Nombre del archivo (default: system_report.json): ") or "system_report.json"
            monitor.save_report(filename)
        elif opcion == "12":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
