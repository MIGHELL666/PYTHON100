import socket
import threading
import json
from datetime import datetime
import time

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = {}
        self.rooms = {'general': []}
        self.server_socket = None
        self.running = False
        self.message_history = []
    
    def start_server(self):
        """Iniciar servidor de chat"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            print(f"🚀 Servidor de chat iniciado en {self.host}:{self.port}")
            print("Esperando conexiones...")
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"Nueva conexión desde {address}")
                    
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error:
                    if self.running:
                        print("Error aceptando conexión")
                    break
                    
        except Exception as e:
            print(f"Error iniciando servidor: {e}")
        finally:
            self.stop_server()
    
    def handle_client(self, client_socket, address):
        """Manejar cliente conectado"""
        username = None
        current_room = 'general'
        
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    msg_type = message.get('type')
                    
                    if msg_type == 'join':
                        username = message.get('username')
                        if username:
                            self.clients[username] = {
                                'socket': client_socket,
                                'address': address,
                                'room': current_room,
                                'joined_at': datetime.now().isoformat()
                            }
                            
                            if username not in self.rooms[current_room]:
                                self.rooms[current_room].append(username)
                            
                            # Enviar mensaje de bienvenida
                            welcome_msg = {
                                'type': 'system',
                                'message': f'Bienvenido al chat, {username}!',
                                'timestamp': datetime.now().isoformat()
                            }
                            client_socket.send(json.dumps(welcome_msg).encode('utf-8'))
                            
                            # Notificar a otros usuarios
                            self.broadcast_message({
                                'type': 'user_joined',
                                'username': username,
                                'message': f'{username} se ha unido al chat',
                                'timestamp': datetime.now().isoformat()
                            }, current_room, exclude=username)
                            
                            # Enviar lista de usuarios conectados
                            self.send_user_list(username, current_room)
                            
                            print(f"Usuario {username} se unió desde {address}")
                    
                    elif msg_type == 'message':
                        if username:
                            chat_message = {
                                'type': 'message',
                                'username': username,
                                'message': message.get('message'),
                                'room': current_room,
                                'timestamp': datetime.now().isoformat()
                            }
                            
                            # Guardar en historial
                            self.message_history.append(chat_message)
                            
                            # Retransmitir mensaje
                            self.broadcast_message(chat_message, current_room)
                            
                            print(f"[{current_room}] {username}: {message.get('message')}")
                    
                    elif msg_type == 'private_message':
                        if username:
                            target_user = message.get('target')
                            if target_user in self.clients:
                                private_msg = {
                                    'type': 'private_message',
                                    'from': username,
                                    'message': message.get('message'),
                                    'timestamp': datetime.now().isoformat()
                                }
                                
                                target_socket = self.clients[target_user]['socket']
                                target_socket.send(json.dumps(private_msg).encode('utf-8'))
                                
                                # Confirmar al remitente
                                confirm_msg = {
                                    'type': 'system',
                                    'message': f'Mensaje privado enviado a {target_user}',
                                    'timestamp': datetime.now().isoformat()
                                }
                                client_socket.send(json.dumps(confirm_msg).encode('utf-8'))
                    
                    elif msg_type == 'change_room':
                        new_room = message.get('room', 'general')
                        if username:
                            # Remover de sala actual
                            if username in self.rooms[current_room]:
                                self.rooms[current_room].remove(username)
                            
                            # Agregar a nueva sala
                            if new_room not in self.rooms:
                                self.rooms[new_room] = []
                            
                            if username not in self.rooms[new_room]:
                                self.rooms[new_room].append(username)
                            
                            # Actualizar información del cliente
                            self.clients[username]['room'] = new_room
                            old_room = current_room
                            current_room = new_room
                            
                            # Notificar cambio de sala
                            room_change_msg = {
                                'type': 'system',
                                'message': f'Te has cambiado a la sala: {new_room}',
                                'timestamp': datetime.now().isoformat()
                            }
                            client_socket.send(json.dumps(room_change_msg).encode('utf-8'))
                            
                            # Notificar a usuarios de ambas salas
                            self.broadcast_message({
                                'type': 'user_left',
                                'username': username,
                                'message': f'{username} ha dejado la sala',
                                'timestamp': datetime.now().isoformat()
                            }, old_room, exclude=username)
                            
                            self.broadcast_message({
                                'type': 'user_joined',
                                'username': username,
                                'message': f'{username} se ha unido a la sala',
                                'timestamp': datetime.now().isoformat()
                            }, new_room, exclude=username)
                            
                            # Enviar nueva lista de usuarios
                            self.send_user_list(username, new_room)
                    
                    elif msg_type == 'list_rooms':
                        if username:
                            rooms_msg = {
                                'type': 'room_list',
                                'rooms': list(self.rooms.keys()),
                                'current_room': current_room,
                                'timestamp': datetime.now().isoformat()
                            }
                            client_socket.send(json.dumps(rooms_msg).encode('utf-8'))
                    
                except json.JSONDecodeError:
                    print(f"Mensaje inválido de {address}: {data}")
                    
        except Exception as e:
            print(f"Error manejando cliente {address}: {e}")
        finally:
            # Limpiar al desconectar
            if username:
                if username in self.clients:
                    del self.clients[username]
                
                if username in self.rooms[current_room]:
                    self.rooms[current_room].remove(username)
                
                # Notificar desconexión
                self.broadcast_message({
                    'type': 'user_left',
                    'username': username,
                    'message': f'{username} ha dejado el chat',
                    'timestamp': datetime.now().isoformat()
                }, current_room, exclude=username)
                
                print(f"Usuario {username} desconectado")
            
            client_socket.close()
    
    def broadcast_message(self, message, room='general', exclude=None):
        """Retransmitir mensaje a todos los usuarios de una sala"""
        if room not in self.rooms:
            return
        
        message_json = json.dumps(message)
        
        for username in self.rooms[room]:
            if username != exclude and username in self.clients:
                try:
                    client_socket = self.clients[username]['socket']
                    client_socket.send(message_json.encode('utf-8'))
                except:
                    # Cliente desconectado, remover
                    if username in self.clients:
                        del self.clients[username]
                    if username in self.rooms[room]:
                        self.rooms[room].remove(username)
    
    def send_user_list(self, username, room):
        """Enviar lista de usuarios conectados"""
        if room in self.rooms:
            user_list_msg = {
                'type': 'user_list',
                'users': self.rooms[room],
                'room': room,
                'timestamp': datetime.now().isoformat()
            }
            
            if username in self.clients:
                client_socket = self.clients[username]['socket']
                client_socket.send(json.dumps(user_list_msg).encode('utf-8'))
    
    def stop_server(self):
        """Detener servidor"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Servidor detenido")
    
    def get_stats(self):
        """Obtener estadísticas del servidor"""
        print(f"\n=== ESTADÍSTICAS DEL SERVIDOR ===")
        print(f"Usuarios conectados: {len(self.clients)}")
        print(f"Salas activas: {len(self.rooms)}")
        print(f"Mensajes enviados: {len(self.message_history)}")
        
        if self.clients:
            print("\nUsuarios conectados:")
            for username, info in self.clients.items():
                print(f"  - {username} (Sala: {info['room']}, IP: {info['address'][0]})")
        
        if self.rooms:
            print("\nSalas:")
            for room, users in self.rooms.items():
                print(f"  - {room}: {len(users)} usuarios")

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.username = None
        self.connected = False
        self.current_room = 'general'
    
    def connect(self, username):
        """Conectar al servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            self.username = username
            self.connected = True
            
            # Enviar mensaje de unión
            join_message = {
                'type': 'join',
                'username': username
            }
            self.socket.send(json.dumps(join_message).encode('utf-8'))
            
            # Iniciar hilo para recibir mensajes
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            print(f"✅ Conectado al servidor como {username}")
            return True
            
        except Exception as e:
            print(f"❌ Error conectando al servidor: {e}")
            return False
    
    def receive_messages(self):
        """Recibir mensajes del servidor"""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                msg_type = message.get('type')
                
                if msg_type == 'message':
                    timestamp = datetime.fromisoformat(message['timestamp']).strftime('%H:%M:%S')
                    print(f"[{timestamp}] {message['username']}: {message['message']}")
                
                elif msg_type == 'private_message':
                    timestamp = datetime.fromisoformat(message['timestamp']).strftime('%H:%M:%S')
                    print(f"[{timestamp}] 💬 {message['from']} (privado): {message['message']}")
                
                elif msg_type == 'system':
                    timestamp = datetime.fromisoformat(message['timestamp']).strftime('%H:%M:%S')
                    print(f"[{timestamp}] 🔔 {message['message']}")
                
                elif msg_type == 'user_joined':
                    timestamp = datetime.fromisoformat(message['timestamp']).strftime('%H:%M:%S')
                    print(f"[{timestamp}] ➕ {message['message']}")
                
                elif msg_type == 'user_left':
                    timestamp = datetime.fromisoformat(message['timestamp']).strftime('%H:%M:%S')
                    print(f"[{timestamp}] ➖ {message['message']}")
                
                elif msg_type == 'user_list':
                    print(f"\n👥 Usuarios en {message['room']}: {', '.join(message['users'])}")
                
                elif msg_type == 'room_list':
                    print(f"\n🏠 Salas disponibles: {', '.join(message['rooms'])}")
                    print(f"📍 Sala actual: {message['current_room']}")
                
            except Exception as e:
                if self.connected:
                    print(f"Error recibiendo mensaje: {e}")
                break
    
    def send_message(self, message):
        """Enviar mensaje público"""
        if self.connected:
            try:
                msg = {
                    'type': 'message',
                    'message': message
                }
                self.socket.send(json.dumps(msg).encode('utf-8'))
            except Exception as e:
                print(f"Error enviando mensaje: {e}")
    
    def send_private_message(self, target_user, message):
        """Enviar mensaje privado"""
        if self.connected:
            try:
                msg = {
                    'type': 'private_message',
                    'target': target_user,
                    'message': message
                }
                self.socket.send(json.dumps(msg).encode('utf-8'))
            except Exception as e:
                print(f"Error enviando mensaje privado: {e}")
    
    def change_room(self, room_name):
        """Cambiar de sala"""
        if self.connected:
            try:
                msg = {
                    'type': 'change_room',
                    'room': room_name
                }
                self.socket.send(json.dumps(msg).encode('utf-8'))
                self.current_room = room_name
            except Exception as e:
                print(f"Error cambiando de sala: {e}")
    
    def list_rooms(self):
        """Listar salas disponibles"""
        if self.connected:
            try:
                msg = {'type': 'list_rooms'}
                self.socket.send(json.dumps(msg).encode('utf-8'))
            except Exception as e:
                print(f"Error listando salas: {e}")
    
    def disconnect(self):
        """Desconectar del servidor"""
        self.connected = False
        if self.socket:
            self.socket.close()
        print("Desconectado del servidor")

def run_server():
    """Ejecutar servidor de chat"""
    server = ChatServer()
    
    try:
        server_thread = threading.Thread(target=server.start_server)
        server_thread.daemon = True
        server_thread.start()
        
        while server.running:
            command = input("\nComandos del servidor (stats/stop): ").strip().lower()
            
            if command == 'stats':
                server.get_stats()
            elif command == 'stop':
                server.stop_server()
                break
            elif command == 'help':
                print("Comandos disponibles:")
                print("  stats - Mostrar estadísticas")
                print("  stop  - Detener servidor")
                print("  help  - Mostrar esta ayuda")
            
    except KeyboardInterrupt:
        server.stop_server()

def run_client():
    """Ejecutar cliente de chat"""
    print("=== CLIENTE DE CHAT ===")
    
    # Configuración de conexión
    host = input("Host del servidor (default: localhost): ") or 'localhost'
    try:
        port = int(input("Puerto (default: 12345): ") or "12345")
    except ValueError:
        port = 12345
    
    username = input("Tu nombre de usuario: ").strip()
    if not username:
        print("Nombre de usuario requerido")
        return
    
    client = ChatClient(host, port)
    
    if not client.connect(username):
        return
    
    print("\n=== COMANDOS DISPONIBLES ===")
    print("/pm <usuario> <mensaje> - Mensaje privado")
    print("/room <nombre> - Cambiar de sala")
    print("/rooms - Listar salas")
    print("/quit - Salir del chat")
    print("================================\n")
    
    try:
        while client.connected:
            message = input()
            
            if message.startswith('/pm '):
                parts = message[4:].split(' ', 1)
                if len(parts) >= 2:
                    target_user, private_msg = parts
                    client.send_private_message(target_user, private_msg)
                else:
                    print("Uso: /pm <usuario> <mensaje>")
            
            elif message.startswith('/room '):
                room_name = message[6:].strip()
                if room_name:
                    client.change_room(room_name)
                else:
                    print("Uso: /room <nombre>")
            
            elif message == '/rooms':
                client.list_rooms()
            
            elif message == '/quit':
                break
            
            elif message.strip():
                client.send_message(message)
                
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()

def main():
    while True:
        print("\n=== SISTEMA DE CHAT ===")
        print("1. Ejecutar servidor")
        print("2. Ejecutar cliente")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            print("Iniciando servidor de chat...")
            run_server()
        elif opcion == "2":
            run_client()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
