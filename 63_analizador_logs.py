import re
import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import os
import gzip

class LogAnalyzer:
    def __init__(self):
        self.logs = []
        self.patterns = {
            'apache': r'(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+|-)',
            'nginx': r'(\S+) - - \[(.*?)\] "(\w+) (.*?) HTTP/\d\.\d" (\d{3}) (\d+) "(.*?)" "(.*?)"',
            'custom': r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)',
            'error': r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR (.+)',
            'access': r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(\w+) (.*?) HTTP/\d\.\d" (\d{3}) (\d+)'
        }
        self.stats = {}
    
    def load_log_file(self, filename):
        """Cargar archivo de log"""
        try:
            self.logs = []
            
            # Detectar si es archivo comprimido
            if filename.endswith('.gz'):
                with gzip.open(filename, 'rt', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            else:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            
            print(f"Cargadas {len(lines)} líneas del archivo {filename}")
            
            # Detectar tipo de log automáticamente
            log_type = self.detect_log_type(lines[:10])
            print(f"Tipo de log detectado: {log_type}")
            
            # Parsear líneas
            for line_num, line in enumerate(lines, 1):
                parsed = self.parse_log_line(line.strip(), log_type)
                if parsed:
                    parsed['line_number'] = line_num
                    parsed['raw_line'] = line.strip()
                    self.logs.append(parsed)
            
            print(f"Parseadas exitosamente {len(self.logs)} líneas")
            return True
            
        except Exception as e:
            print(f"Error cargando archivo: {e}")
            return False
    
    def detect_log_type(self, sample_lines):
        """Detectar tipo de log automáticamente"""
        for log_type, pattern in self.patterns.items():
            matches = 0
            for line in sample_lines:
                if re.match(pattern, line.strip()):
                    matches += 1
            
            if matches >= len(sample_lines) * 0.5:  # 50% de coincidencias
                return log_type
        
        return 'custom'
    
    def parse_log_line(self, line, log_type='apache'):
        """Parsear una línea de log"""
        try:
            pattern = self.patterns.get(log_type, self.patterns['custom'])
            match = re.match(pattern, line)
            
            if not match:
                return None
            
            if log_type == 'apache':
                return {
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'method': match.group(3),
                    'url': match.group(4),
                    'protocol': match.group(5),
                    'status': int(match.group(6)),
                    'size': match.group(7) if match.group(7) != '-' else 0,
                    'type': 'apache'
                }
            elif log_type == 'nginx':
                return {
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'method': match.group(3),
                    'url': match.group(4),
                    'status': int(match.group(5)),
                    'size': int(match.group(6)) if match.group(6).isdigit() else 0,
                    'referer': match.group(7),
                    'user_agent': match.group(8),
                    'type': 'nginx'
                }
            elif log_type == 'custom':
                return {
                    'timestamp': match.group(1),
                    'level': match.group(2),
                    'message': match.group(3),
                    'type': 'custom'
                }
            elif log_type == 'error':
                return {
                    'timestamp': match.group(1),
                    'level': 'ERROR',
                    'message': match.group(2),
                    'type': 'error'
                }
            elif log_type == 'access':
                return {
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'method': match.group(3),
                    'url': match.group(4),
                    'status': int(match.group(5)),
                    'size': int(match.group(6)) if match.group(6).isdigit() else 0,
                    'type': 'access'
                }
                
        except Exception as e:
            print(f"Error parseando línea: {e}")
            return None
    
    def analyze_ips(self):
        """Analizar direcciones IP"""
        if not self.logs:
            print("No hay logs cargados")
            return
        
        ip_counter = Counter()
        ip_requests = defaultdict(list)
        
        for log in self.logs:
            if 'ip' in log:
                ip_counter[log['ip']] += 1
                ip_requests[log['ip']].append(log)
        
        print("\n=== ANÁLISIS DE IPs ===")
        print("Top 10 IPs más activas:")
        for ip, count in ip_counter.most_common(10):
            print(f"{ip}: {count} requests")
        
        # Detectar posibles ataques (muchas requests de la misma IP)
        suspicious_ips = [(ip, count) for ip, count in ip_counter.items() if count > 100]
        if suspicious_ips:
            print("\n⚠️  IPs sospechosas (>100 requests):")
            for ip, count in suspicious_ips:
                print(f"{ip}: {count} requests")
        
        self.stats['ips'] = dict(ip_counter)
    
    def analyze_status_codes(self):
        """Analizar códigos de estado HTTP"""
        if not self.logs:
            print("No hay logs cargados")
            return
        
        status_counter = Counter()
        error_logs = []
        
        for log in self.logs:
            if 'status' in log:
                status_counter[log['status']] += 1
                if log['status'] >= 400:
                    error_logs.append(log)
        
        print("\n=== ANÁLISIS DE CÓDIGOS DE ESTADO ===")
        for status, count in sorted(status_counter.items()):
            status_name = self.get_status_name(status)
            print(f"{status} ({status_name}): {count}")
        
        if error_logs:
            print(f"\n❌ Errores encontrados: {len(error_logs)}")
            print("Primeros 5 errores:")
            for error in error_logs[:5]:
                print(f"  {error['status']} - {error.get('url', 'N/A')} - IP: {error.get('ip', 'N/A')}")
        
        self.stats['status_codes'] = dict(status_counter)
    
    def get_status_name(self, code):
        """Obtener nombre del código de estado"""
        status_names = {
            200: "OK", 201: "Created", 204: "No Content",
            301: "Moved Permanently", 302: "Found", 304: "Not Modified",
            400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
            404: "Not Found", 405: "Method Not Allowed",
            500: "Internal Server Error", 502: "Bad Gateway", 503: "Service Unavailable"
        }
        return status_names.get(code, "Unknown")
    
    def analyze_urls(self):
        """Analizar URLs más visitadas"""
        if not self.logs:
            print("No hay logs cargados")
            return
        
        url_counter = Counter()
        
        for log in self.logs:
            if 'url' in log:
                url_counter[log['url']] += 1
        
        print("\n=== ANÁLISIS DE URLs ===")
        print("Top 15 URLs más visitadas:")
        for url, count in url_counter.most_common(15):
            print(f"{count:4d} - {url}")
        
        self.stats['urls'] = dict(url_counter.most_common(50))
    
    def analyze_time_patterns(self):
        """Analizar patrones temporales"""
        if not self.logs:
            print("No hay logs cargados")
            return
        
        hourly_traffic = defaultdict(int)
        daily_traffic = defaultdict(int)
        
        for log in self.logs:
            if 'timestamp' in log:
                try:
                    # Intentar diferentes formatos de fecha
                    timestamp_str = log['timestamp']
                    
                    # Formato Apache: [25/Dec/2023:10:00:00 +0000]
                    if '[' in timestamp_str:
                        timestamp_str = timestamp_str.strip('[]')
                        dt = datetime.strptime(timestamp_str.split()[0], '%d/%b/%Y:%H:%M:%S')
                    else:
                        # Formato estándar: 2023-12-25 10:00:00
                        dt = datetime.strptime(timestamp_str[:19], '%Y-%m-%d %H:%M:%S')
                    
                    hourly_traffic[dt.hour] += 1
                    daily_traffic[dt.strftime('%Y-%m-%d')] += 1
                    
                except Exception:
                    continue
        
        print("\n=== ANÁLISIS TEMPORAL ===")
        print("Tráfico por hora:")
        for hour in range(24):
            count = hourly_traffic[hour]
            bar = '█' * (count // 10) if count > 0 else ''
            print(f"{hour:2d}:00 - {count:4d} {bar}")
        
        print("\nTráfico por día (últimos 7 días):")
        for day, count in sorted(daily_traffic.items())[-7:]:
            print(f"{day}: {count}")
        
        self.stats['hourly_traffic'] = dict(hourly_traffic)
        self.stats['daily_traffic'] = dict(daily_traffic)
    
    def analyze_user_agents(self):
        """Analizar User Agents"""
        if not self.logs:
            print("No hay logs cargados")
            return
        
        ua_counter = Counter()
        bot_counter = Counter()
        
        bot_patterns = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
        
        for log in self.logs:
            if 'user_agent' in log:
                ua = log['user_agent']
                ua_counter[ua] += 1
                
                # Detectar bots
                if any(pattern in ua.lower() for pattern in bot_patterns):
                    bot_counter[ua] += 1
        
        print("\n=== ANÁLISIS DE USER AGENTS ===")
        print("Top 10 User Agents:")
        for ua, count in ua_counter.most_common(10):
            ua_short = ua[:80] + "..." if len(ua) > 80 else ua
            print(f"{count:4d} - {ua_short}")
        
        if bot_counter:
            print(f"\n🤖 Bots detectados: {sum(bot_counter.values())} requests")
            for bot, count in bot_counter.most_common(5):
                bot_short = bot[:60] + "..." if len(bot) > 60 else bot
                print(f"  {count:4d} - {bot_short}")
        
        self.stats['user_agents'] = dict(ua_counter.most_common(20))
    
    def generate_report(self):
        """Generar reporte completo"""
        if not self.logs:
            print("No hay logs cargados")
            return
        
        print("\n" + "="*50)
        print("REPORTE COMPLETO DE ANÁLISIS DE LOGS")
        print("="*50)
        
        print(f"\nTotal de líneas procesadas: {len(self.logs)}")
        print(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.analyze_ips()
        self.analyze_status_codes()
        self.analyze_urls()
        self.analyze_time_patterns()
        self.analyze_user_agents()
        
        # Guardar estadísticas
        self.save_stats()
    
    def save_stats(self, filename="log_analysis.json"):
        """Guardar estadísticas en archivo JSON"""
        try:
            self.stats['analysis_date'] = datetime.now().isoformat()
            self.stats['total_logs'] = len(self.logs)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
            
            print(f"\n📊 Estadísticas guardadas en {filename}")
            
        except Exception as e:
            print(f"Error guardando estadísticas: {e}")
    
    def create_sample_log(self, filename="sample.log", lines=100):
        """Crear archivo de log de ejemplo"""
        try:
            import random
            
            ips = ['192.168.1.1', '10.0.0.1', '203.0.113.1', '198.51.100.1', '172.16.0.1']
            methods = ['GET', 'POST', 'PUT', 'DELETE']
            urls = ['/', '/index.html', '/api/users', '/login', '/dashboard', '/static/css/style.css']
            statuses = [200, 200, 200, 404, 500, 301, 302]
            
            with open(filename, 'w') as f:
                for i in range(lines):
                    ip = random.choice(ips)
                    timestamp = datetime.now().strftime('%d/%b/%Y:%H:%M:%S +0000')
                    method = random.choice(methods)
                    url = random.choice(urls)
                    status = random.choice(statuses)
                    size = random.randint(100, 5000)
                    
                    log_line = f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size}\n'
                    f.write(log_line)
            
            print(f"Archivo de ejemplo creado: {filename}")
            
        except Exception as e:
            print(f"Error creando archivo de ejemplo: {e}")

def main():
    analyzer = LogAnalyzer()
    
    while True:
        print("\n=== ANALIZADOR DE LOGS ===")
        print("1. Cargar archivo de log")
        print("2. Crear archivo de ejemplo")
        print("3. Analizar IPs")
        print("4. Analizar códigos de estado")
        print("5. Analizar URLs")
        print("6. Analizar patrones temporales")
        print("7. Analizar User Agents")
        print("8. Generar reporte completo")
        print("9. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            filename = input("Nombre del archivo de log: ")
            if os.path.exists(filename):
                analyzer.load_log_file(filename)
            else:
                print("Archivo no encontrado")
                
        elif opcion == "2":
            filename = input("Nombre del archivo a crear (default: sample.log): ") or "sample.log"
            try:
                lines = int(input("Número de líneas (default: 100): ") or "100")
                analyzer.create_sample_log(filename, lines)
            except ValueError:
                print("Número de líneas debe ser un entero")
                
        elif opcion == "3":
            analyzer.analyze_ips()
        elif opcion == "4":
            analyzer.analyze_status_codes()
        elif opcion == "5":
            analyzer.analyze_urls()
        elif opcion == "6":
            analyzer.analyze_time_patterns()
        elif opcion == "7":
            analyzer.analyze_user_agents()
        elif opcion == "8":
            analyzer.generate_report()
        elif opcion == "9":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
