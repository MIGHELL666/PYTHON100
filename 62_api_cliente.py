import requests
import json
from datetime import datetime
import time

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_urls = {
            'jsonplaceholder': 'https://jsonplaceholder.typicode.com',
            'httpbin': 'https://httpbin.org',
            'reqres': 'https://reqres.in/api'
        }
        self.timeout = 10
    
    def test_connection(self, url):
        """Probar conexión a una API"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            print(f"✅ Conexión exitosa a {url}")
            print(f"Status: {response.status_code}")
            print(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando a {url}: {e}")
            return False
    
    def get_posts(self):
        """Obtener posts de JSONPlaceholder"""
        try:
            url = f"{self.base_urls['jsonplaceholder']}/posts"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            posts = response.json()
            print(f"\n=== POSTS OBTENIDOS ({len(posts)}) ===")
            
            for post in posts[:5]:  # Mostrar solo los primeros 5
                print(f"\nID: {post['id']}")
                print(f"Título: {post['title']}")
                print(f"Contenido: {post['body'][:100]}...")
            
            return posts
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo posts: {e}")
            return None
    
    def get_users(self):
        """Obtener usuarios de JSONPlaceholder"""
        try:
            url = f"{self.base_urls['jsonplaceholder']}/users"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            users = response.json()
            print(f"\n=== USUARIOS OBTENIDOS ({len(users)}) ===")
            
            for user in users:
                print(f"\nID: {user['id']}")
                print(f"Nombre: {user['name']}")
                print(f"Email: {user['email']}")
                print(f"Ciudad: {user['address']['city']}")
            
            return users
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo usuarios: {e}")
            return None
    
    def create_post(self, title, body, user_id=1):
        """Crear un nuevo post"""
        try:
            url = f"{self.base_urls['jsonplaceholder']}/posts"
            data = {
                'title': title,
                'body': body,
                'userId': user_id
            }
            
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            
            new_post = response.json()
            print(f"\n✅ Post creado exitosamente!")
            print(f"ID: {new_post['id']}")
            print(f"Título: {new_post['title']}")
            
            return new_post
            
        except requests.exceptions.RequestException as e:
            print(f"Error creando post: {e}")
            return None
    
    def update_post(self, post_id, title, body, user_id=1):
        """Actualizar un post existente"""
        try:
            url = f"{self.base_urls['jsonplaceholder']}/posts/{post_id}"
            data = {
                'id': post_id,
                'title': title,
                'body': body,
                'userId': user_id
            }
            
            response = self.session.put(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            
            updated_post = response.json()
            print(f"\n✅ Post actualizado exitosamente!")
            print(f"ID: {updated_post['id']}")
            print(f"Título: {updated_post['title']}")
            
            return updated_post
            
        except requests.exceptions.RequestException as e:
            print(f"Error actualizando post: {e}")
            return None
    
    def delete_post(self, post_id):
        """Eliminar un post"""
        try:
            url = f"{self.base_urls['jsonplaceholder']}/posts/{post_id}"
            response = self.session.delete(url, timeout=self.timeout)
            response.raise_for_status()
            
            print(f"\n✅ Post {post_id} eliminado exitosamente!")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error eliminando post: {e}")
            return False
    
    def test_http_methods(self):
        """Probar diferentes métodos HTTP con httpbin"""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        
        print("\n=== PROBANDO MÉTODOS HTTP ===")
        
        for method in methods:
            try:
                url = f"{self.base_urls['httpbin']}/{method.lower()}"
                
                if method == 'GET':
                    response = self.session.get(url, timeout=self.timeout)
                elif method == 'POST':
                    response = self.session.post(url, json={'test': 'data'}, timeout=self.timeout)
                elif method == 'PUT':
                    response = self.session.put(url, json={'test': 'data'}, timeout=self.timeout)
                elif method == 'DELETE':
                    response = self.session.delete(url, timeout=self.timeout)
                elif method == 'PATCH':
                    response = self.session.patch(url, json={'test': 'data'}, timeout=self.timeout)
                
                print(f"✅ {method}: {response.status_code}")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ {method}: Error - {e}")
    
    def get_ip_info(self):
        """Obtener información de IP"""
        try:
            url = f"{self.base_urls['httpbin']}/ip"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            ip_info = response.json()
            print(f"\n=== INFORMACIÓN DE IP ===")
            print(f"Tu IP: {ip_info['origin']}")
            
            # Obtener headers
            url_headers = f"{self.base_urls['httpbin']}/headers"
            response = self.session.get(url_headers, timeout=self.timeout)
            headers_info = response.json()
            
            print(f"\n=== HEADERS ===")
            for header, value in headers_info['headers'].items():
                print(f"{header}: {value}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo información de IP: {e}")
    
    def test_authentication(self):
        """Probar autenticación básica"""
        try:
            username = "user"
            password = "pass"
            url = f"{self.base_urls['httpbin']}/basic-auth/{username}/{password}"
            
            # Sin autenticación
            response = self.session.get(url, timeout=self.timeout)
            print(f"Sin auth: {response.status_code}")
            
            # Con autenticación
            response = self.session.get(url, auth=(username, password), timeout=self.timeout)
            print(f"Con auth: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Autenticación exitosa")
                print(response.json())
            
        except requests.exceptions.RequestException as e:
            print(f"Error probando autenticación: {e}")
    
    def save_response(self, data, filename):
        """Guardar respuesta en archivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Datos guardados en {filename}")
        except Exception as e:
            print(f"Error guardando datos: {e}")

def main():
    client = APIClient()
    
    while True:
        print("\n=== CLIENTE API ===")
        print("1. Probar conexiones")
        print("2. Obtener posts")
        print("3. Obtener usuarios")
        print("4. Crear post")
        print("5. Actualizar post")
        print("6. Eliminar post")
        print("7. Probar métodos HTTP")
        print("8. Información de IP")
        print("9. Probar autenticación")
        print("10. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            for name, url in client.base_urls.items():
                print(f"\nProbando {name}...")
                client.test_connection(url)
                
        elif opcion == "2":
            posts = client.get_posts()
            if posts:
                save = input("¿Guardar en archivo? (s/n): ")
                if save.lower() == 's':
                    client.save_response(posts, "posts.json")
                    
        elif opcion == "3":
            users = client.get_users()
            if users:
                save = input("¿Guardar en archivo? (s/n): ")
                if save.lower() == 's':
                    client.save_response(users, "users.json")
                    
        elif opcion == "4":
            title = input("Título del post: ")
            body = input("Contenido del post: ")
            client.create_post(title, body)
            
        elif opcion == "5":
            try:
                post_id = int(input("ID del post a actualizar: "))
                title = input("Nuevo título: ")
                body = input("Nuevo contenido: ")
                client.update_post(post_id, title, body)
            except ValueError:
                print("ID debe ser un número")
                
        elif opcion == "6":
            try:
                post_id = int(input("ID del post a eliminar: "))
                client.delete_post(post_id)
            except ValueError:
                print("ID debe ser un número")
                
        elif opcion == "7":
            client.test_http_methods()
        elif opcion == "8":
            client.get_ip_info()
        elif opcion == "9":
            client.test_authentication()
        elif opcion == "10":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
