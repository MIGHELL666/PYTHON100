import http.server
import socketserver
import json
import urllib.parse
import os
import mimetypes
from datetime import datetime
import threading
import webbrowser

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.api_routes = {
            '/api/time': self.api_time,
            '/api/files': self.api_files,
            '/api/upload': self.api_upload,
            '/api/system': self.api_system
        }
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Manejar peticiones GET"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Rutas de API
        if parsed_path.path in self.api_routes:
            self.api_routes[parsed_path.path]()
            return
        
        # Ruta especial para la página principal
        if parsed_path.path == '/':
            self.serve_index()
            return
        
        # Servir archivos estáticos
        super().do_GET()
    
    def do_POST(self):
        """Manejar peticiones POST"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/upload':
            self.api_upload()
        elif parsed_path.path == '/api/message':
            self.api_message()
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_index(self):
        """Servir página principal personalizada"""
        html_content = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Servidor HTTP Python</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; text-align: center; }
                .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
                button:hover { background: #0056b3; }
                .result { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px; white-space: pre-wrap; }
                input[type="file"], input[type="text"] { margin: 10px 0; padding: 8px; width: 100%; box-sizing: border-box; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐍 Servidor HTTP Python</h1>
                
                <div class="section">
                    <h3>📊 APIs Disponibles</h3>
                    <button onclick="fetchAPI('/api/time')">Obtener Hora</button>
                    <button onclick="fetchAPI('/api/system')">Info del Sistema</button>
                    <button onclick="fetchAPI('/api/files')">Listar Archivos</button>
                    <div id="api-result" class="result" style="display:none;"></div>
                </div>
                
                <div class="section">
                    <h3>📤 Subir Archivo</h3>
                    <input type="file" id="fileInput" />
                    <button onclick="uploadFile()">Subir Archivo</button>
                    <div id="upload-result" class="result" style="display:none;"></div>
                </div>
                
                <div class="section">
                    <h3>💬 Enviar Mensaje</h3>
                    <input type="text" id="messageInput" placeholder="Escribe tu mensaje..." />
                    <button onclick="sendMessage()">Enviar Mensaje</button>
                    <div id="message-result" class="result" style="display:none;"></div>
                </div>
                
                <div class="section">
                    <h3>📁 Explorador de Archivos</h3>
                    <div id="file-explorer"></div>
                </div>
            </div>
            
            <script>
                async function fetchAPI(endpoint) {
                    try {
                        const response = await fetch(endpoint);
                        const data = await response.json();
                        const resultDiv = document.getElementById('api-result');
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = JSON.stringify(data, null, 2);
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Error al obtener datos de la API');
                    }
                }
                
                async function uploadFile() {
                    const fileInput = document.getElementById('fileInput');
                    const file = fileInput.files[0];
                    
                    if (!file) {
                        alert('Por favor selecciona un archivo');
                        return;
                    }
                    
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    try {
                        const response = await fetch('/api/upload', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();
                        const resultDiv = document.getElementById('upload-result');
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = JSON.stringify(result, null, 2);
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Error al subir archivo');
                    }
                }
                
                async function sendMessage() {
                    const messageInput = document.getElementById('messageInput');
                    const message = messageInput.value.trim();
                    
                    if (!message) {
                        alert('Por favor escribe un mensaje');
                        return;
                    }
                    
                    try {
                        const response = await fetch('/api/message', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ message: message })
                        });
                        const result = await response.json();
                        const resultDiv = document.getElementById('message-result');
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = JSON.stringify(result, null, 2);
                        messageInput.value = '';
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Error al enviar mensaje');
                    }
                }
                
                // Cargar explorador de archivos al inicio
                window.onload = function() {
                    fetchAPI('/api/files').then(() => {
                        const apiResult = document.getElementById('api-result').textContent;
                        const files = JSON.parse(apiResult);
                        displayFiles(files.files);
                    });
                };
                
                function displayFiles(files) {
                    const explorer = document.getElementById('file-explorer');
                    explorer.innerHTML = '<h4>Archivos en el servidor:</h4>';
                    
                    files.forEach(file => {
                        const fileDiv = document.createElement('div');
                        fileDiv.style.padding = '5px';
                        fileDiv.style.borderBottom = '1px solid #eee';
                        fileDiv.innerHTML = `
                            <strong>${file.name}</strong> 
                            <span style="color: #666;">(${file.size} bytes, ${file.modified})</span>
                        `;
                        explorer.appendChild(fileDiv);
                    });
                }
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def api_time(self):
        """API para obtener la hora actual"""
        response_data = {
            'timestamp': datetime.now().isoformat(),
            'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'timezone': 'Local'
        }
        self.send_json_response(response_data)
    
    def api_files(self):
        """API para listar archivos del directorio actual"""
        try:
            files = []
            for filename in os.listdir('.'):
                if os.path.isfile(filename):
                    stat = os.stat(filename)
                    files.append({
                        'name': filename,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            response_data = {
                'directory': os.getcwd(),
                'file_count': len(files),
                'files': files
            }
            self.send_json_response(response_data)
            
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def api_system(self):
        """API para información del sistema"""
        import platform
        import psutil
        
        try:
            response_data = {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'cpu_count': os.cpu_count(),
                'memory_usage': dict(psutil.virtual_memory()._asdict()) if 'psutil' in globals() else 'N/A',
                'current_directory': os.getcwd(),
                'server_time': datetime.now().isoformat()
            }
            self.send_json_response(response_data)
            
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def api_upload(self):
        """API para subir archivos"""
        if self.command == 'POST':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Crear directorio de uploads si no existe
                upload_dir = 'uploads'
                os.makedirs(upload_dir, exist_ok=True)
                
                # Parsear datos multipart (simplificado)
                boundary = self.headers['Content-Type'].split('boundary=')[1]
                parts = post_data.split(f'--{boundary}'.encode())
                
                for part in parts:
                    if b'filename=' in part:
                        # Extraer nombre del archivo
                        filename_start = part.find(b'filename="') + 10
                        filename_end = part.find(b'"', filename_start)
                        filename = part[filename_start:filename_end].decode('utf-8')
                        
                        if filename:
                            # Extraer contenido del archivo
                            content_start = part.find(b'\r\n\r\n') + 4
                            content_end = part.rfind(b'\r\n')
                            file_content = part[content_start:content_end]
                            
                            # Guardar archivo
                            filepath = os.path.join(upload_dir, filename)
                            with open(filepath, 'wb') as f:
                                f.write(file_content)
                            
                            response_data = {
                                'success': True,
                                'filename': filename,
                                'size': len(file_content),
                                'path': filepath,
                                'uploaded_at': datetime.now().isoformat()
                            }
                            self.send_json_response(response_data)
                            return
                
                self.send_json_response({'error': 'No file found in request'}, 400)
                
            except Exception as e:
                self.send_json_response({'error': str(e)}, 500)
        else:
            self.send_json_response({'error': 'Method not allowed'}, 405)
    
    def api_message(self):
        """API para recibir mensajes"""
        if self.command == 'POST':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                message_data = json.loads(post_data.decode('utf-8'))
                
                # Guardar mensaje en archivo log
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'message': message_data.get('message', ''),
                    'client_ip': self.client_address[0]
                }
                
                with open('messages.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
                response_data = {
                    'success': True,
                    'received_message': message_data.get('message', ''),
                    'processed_at': datetime.now().isoformat(),
                    'response': f"Mensaje recibido: {message_data.get('message', '')}"
                }
                self.send_json_response(response_data)
                
            except Exception as e:
                self.send_json_response({'error': str(e)}, 500)
        else:
            self.send_json_response({'error': 'Method not allowed'}, 405)
    
    def send_json_response(self, data, status_code=200):
        """Enviar respuesta JSON"""
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Personalizar logging"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

class HTTPServer:
    def __init__(self, port=8000, directory=None):
        self.port = port
        self.directory = directory or os.getcwd()
        self.server = None
        self.server_thread = None
        self.running = False
    
    def start_server(self):
        """Iniciar servidor HTTP"""
        try:
            # Cambiar al directorio especificado
            original_dir = os.getcwd()
            os.chdir(self.directory)
            
            # Crear servidor
            handler = CustomHTTPRequestHandler
            self.server = socketserver.TCPServer(("", self.port), handler)
            
            print(f"🚀 Servidor HTTP iniciado en puerto {self.port}")
            print(f"📁 Sirviendo archivos desde: {self.directory}")
            print(f"🌐 URL: http://localhost:{self.port}")
            print(f"⏹️  Presiona Ctrl+C para detener el servidor\n")
            
            # Abrir navegador automáticamente
            try:
                webbrowser.open(f'http://localhost:{self.port}')
            except:
                pass
            
            self.running = True
            
            # Ejecutar servidor en hilo separado
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            return True
            
        except OSError as e:
            if e.errno == 98:  # Puerto en uso
                print(f"❌ Error: El puerto {self.port} ya está en uso")
                print("Intenta con otro puerto o detén el proceso que lo está usando")
            else:
                print(f"❌ Error iniciando servidor: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def stop_server(self):
        """Detener servidor HTTP"""
        if self.server:
            print("\n🛑 Deteniendo servidor...")
            self.server.shutdown()
            self.server.server_close()
            self.running = False
            print("✅ Servidor detenido")
    
    def get_server_stats(self):
        """Obtener estadísticas del servidor"""
        if not self.running:
            print("El servidor no está ejecutándose")
            return
        
        print(f"\n=== ESTADÍSTICAS DEL SERVIDOR ===")
        print(f"Puerto: {self.port}")
        print(f"Directorio: {self.directory}")
        print(f"Estado: {'Ejecutándose' if self.running else 'Detenido'}")
        print(f"URL: http://localhost:{self.port}")
        
        # Mostrar archivos en el directorio
        try:
            files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
            print(f"Archivos servidos: {len(files)}")
            
            if files:
                print("Archivos disponibles:")
                for file in files[:10]:  # Mostrar solo los primeros 10
                    file_path = os.path.join(self.directory, file)
                    size = os.path.getsize(file_path)
                    print(f"  - {file} ({size} bytes)")
                
                if len(files) > 10:
                    print(f"  ... y {len(files) - 10} archivos más")
                    
        except Exception as e:
            print(f"Error listando archivos: {e}")

def create_sample_files():
    """Crear archivos de ejemplo para el servidor"""
    try:
        # Crear directorio de ejemplo
        os.makedirs('sample_files', exist_ok=True)
        
        # Archivo HTML de ejemplo
        with open('sample_files/ejemplo.html', 'w', encoding='utf-8') as f:
            f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Archivo de Ejemplo</title>
                <style>body { font-family: Arial; margin: 40px; }</style>
            </head>
            <body>
                <h1>¡Hola desde el servidor HTTP!</h1>
                <p>Este es un archivo de ejemplo servido por el servidor HTTP de Python.</p>
                <p>Fecha de creación: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </body>
            </html>
            """)
        
        # Archivo JSON de ejemplo
        sample_data = {
            "mensaje": "Datos de ejemplo",
            "timestamp": datetime.now().isoformat(),
            "datos": [1, 2, 3, 4, 5],
            "configuracion": {
                "activo": True,
                "version": "1.0"
            }
        }
        
        with open('sample_files/datos.json', 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        # Archivo de texto de ejemplo
        with open('sample_files/readme.txt', 'w', encoding='utf-8') as f:
            f.write("""
Servidor HTTP Python - Archivos de Ejemplo
==========================================

Este directorio contiene archivos de ejemplo para probar el servidor HTTP.

Archivos incluidos:
- ejemplo.html: Página web de ejemplo
- datos.json: Datos en formato JSON
- readme.txt: Este archivo

Para acceder a estos archivos, visita:
http://localhost:8000/sample_files/[nombre_archivo]

Creado el: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        print("✅ Archivos de ejemplo creados en 'sample_files/'")
        
    except Exception as e:
        print(f"Error creando archivos de ejemplo: {e}")

def main():
    server = None
    
    while True:
        print("\n=== SERVIDOR HTTP PYTHON ===")
        print("1. Iniciar servidor")
        print("2. Detener servidor")
        print("3. Estadísticas del servidor")
        print("4. Cambiar puerto")
        print("5. Cambiar directorio")
        print("6. Crear archivos de ejemplo")
        print("7. Abrir en navegador")
        print("8. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            if server and server.running:
                print("El servidor ya está ejecutándose")
            else:
                port = int(input("Puerto (default: 8000): ") or "8000")
                directory = input("Directorio a servir (default: actual): ") or os.getcwd()
                
                server = HTTPServer(port, directory)
                if server.start_server():
                    try:
                        # Mantener el servidor ejecutándose
                        while server.running:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        server.stop_server()
                        
        elif opcion == "2":
            if server and server.running:
                server.stop_server()
            else:
                print("El servidor no está ejecutándose")
                
        elif opcion == "3":
            if server:
                server.get_server_stats()
            else:
                print("No hay servidor configurado")
                
        elif opcion == "4":
            try:
                new_port = int(input("Nuevo puerto: "))
                if server:
                    server.port = new_port
                print(f"Puerto cambiado a {new_port}")
            except ValueError:
                print("Puerto debe ser un número")
                
        elif opcion == "5":
            new_directory = input("Nuevo directorio: ")
            if os.path.exists(new_directory):
                if server:
                    server.directory = new_directory
                print(f"Directorio cambiado a {new_directory}")
            else:
                print("El directorio no existe")
                
        elif opcion == "6":
            create_sample_files()
            
        elif opcion == "7":
            if server and server.running:
                try:
                    webbrowser.open(f'http://localhost:{server.port}')
                    print("Navegador abierto")
                except:
                    print("No se pudo abrir el navegador automáticamente")
                    print(f"Visita manualmente: http://localhost:{server.port}")
            else:
                print("El servidor no está ejecutándose")
                
        elif opcion == "8":
            if server and server.running:
                server.stop_server()
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
