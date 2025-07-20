import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_name="mi_base_datos.db"):
        self.db_name = db_name
        self.conn = None
        self.create_connection()
        self.create_tables()
    
    def create_connection(self):
        """Crear conexión a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
            print(f"Conexión exitosa a {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error conectando a la base de datos: {e}")
    
    def create_tables(self):
        """Crear tablas iniciales"""
        try:
            cursor = self.conn.cursor()
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    edad INTEGER,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de productos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT,
                    stock INTEGER DEFAULT 0,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de ventas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    producto_id INTEGER,
                    cantidad INTEGER NOT NULL,
                    total REAL NOT NULL,
                    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                    FOREIGN KEY (producto_id) REFERENCES productos (id)
                )
            ''')
            
            self.conn.commit()
            print("Tablas creadas exitosamente")
            
        except sqlite3.Error as e:
            print(f"Error creando tablas: {e}")
    
    def insertar_usuario(self, nombre, email, edad):
        """Insertar nuevo usuario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, edad) VALUES (?, ?, ?)",
                (nombre, email, edad)
            )
            self.conn.commit()
            print(f"Usuario {nombre} insertado exitosamente")
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print("Error: El email ya existe")
            return None
        except sqlite3.Error as e:
            print(f"Error insertando usuario: {e}")
            return None
    
    def insertar_producto(self, nombre, precio, categoria, stock):
        """Insertar nuevo producto"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, categoria, stock) VALUES (?, ?, ?, ?)",
                (nombre, precio, categoria, stock)
            )
            self.conn.commit()
            print(f"Producto {nombre} insertado exitosamente")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error insertando producto: {e}")
            return None
    
    def registrar_venta(self, usuario_id, producto_id, cantidad):
        """Registrar una venta"""
        try:
            cursor = self.conn.cursor()
            
            # Verificar stock
            cursor.execute("SELECT stock, precio FROM productos WHERE id = ?", (producto_id,))
            producto = cursor.fetchone()
            
            if not producto:
                print("Producto no encontrado")
                return False
            
            if producto['stock'] < cantidad:
                print(f"Stock insuficiente. Disponible: {producto['stock']}")
                return False
            
            # Calcular total
            total = producto['precio'] * cantidad
            
            # Registrar venta
            cursor.execute(
                "INSERT INTO ventas (usuario_id, producto_id, cantidad, total) VALUES (?, ?, ?, ?)",
                (usuario_id, producto_id, cantidad, total)
            )
            
            # Actualizar stock
            cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (cantidad, producto_id)
            )
            
            self.conn.commit()
            print(f"Venta registrada exitosamente. Total: ${total:.2f}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error registrando venta: {e}")
            return False
    
    def consultar_usuarios(self):
        """Consultar todos los usuarios"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM usuarios ORDER BY fecha_registro DESC")
            usuarios = cursor.fetchall()
            
            if usuarios:
                print("\n=== USUARIOS ===")
                for usuario in usuarios:
                    print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}, "
                          f"Email: {usuario['email']}, Edad: {usuario['edad']}")
            else:
                print("No hay usuarios registrados")
                
        except sqlite3.Error as e:
            print(f"Error consultando usuarios: {e}")
    
    def consultar_productos(self):
        """Consultar todos los productos"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY nombre")
            productos = cursor.fetchall()
            
            if productos:
                print("\n=== PRODUCTOS ===")
                for producto in productos:
                    print(f"ID: {producto['id']}, Nombre: {producto['nombre']}, "
                          f"Precio: ${producto['precio']:.2f}, Stock: {producto['stock']}")
            else:
                print("No hay productos registrados")
                
        except sqlite3.Error as e:
            print(f"Error consultando productos: {e}")
    
    def reporte_ventas(self):
        """Generar reporte de ventas"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT v.id, u.nombre as usuario, p.nombre as producto, 
                       v.cantidad, v.total, v.fecha_venta
                FROM ventas v
                JOIN usuarios u ON v.usuario_id = u.id
                JOIN productos p ON v.producto_id = p.id
                ORDER BY v.fecha_venta DESC
            ''')
            ventas = cursor.fetchall()
            
            if ventas:
                print("\n=== REPORTE DE VENTAS ===")
                total_general = 0
                for venta in ventas:
                    print(f"Venta #{venta['id']}: {venta['usuario']} compró "
                          f"{venta['cantidad']} {venta['producto']} - Total: ${venta['total']:.2f}")
                    total_general += venta['total']
                
                print(f"\nTotal general de ventas: ${total_general:.2f}")
            else:
                print("No hay ventas registradas")
                
        except sqlite3.Error as e:
            print(f"Error generando reporte: {e}")
    
    def exportar_datos(self, tabla, filename):
        """Exportar datos a JSON"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {tabla}")
            datos = cursor.fetchall()
            
            # Convertir a lista de diccionarios
            datos_json = [dict(row) for row in datos]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"Datos de {tabla} exportados a {filename}")
            
        except Exception as e:
            print(f"Error exportando datos: {e}")
    
    def cerrar_conexion(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            print("Conexión cerrada")

def main():
    db = DatabaseManager()
    
    while True:
        print("\n=== GESTOR DE BASE DE DATOS ===")
        print("1. Insertar usuario")
        print("2. Insertar producto")
        print("3. Registrar venta")
        print("4. Consultar usuarios")
        print("5. Consultar productos")
        print("6. Reporte de ventas")
        print("7. Exportar datos")
        print("8. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre: ")
            email = input("Email: ")
            try:
                edad = int(input("Edad: "))
                db.insertar_usuario(nombre, email, edad)
            except ValueError:
                print("Edad debe ser un número")
                
        elif opcion == "2":
            nombre = input("Nombre del producto: ")
            try:
                precio = float(input("Precio: "))
                categoria = input("Categoría: ")
                stock = int(input("Stock inicial: "))
                db.insertar_producto(nombre, precio, categoria, stock)
            except ValueError:
                print("Precio y stock deben ser números")
                
        elif opcion == "3":
            try:
                usuario_id = int(input("ID del usuario: "))
                producto_id = int(input("ID del producto: "))
                cantidad = int(input("Cantidad: "))
                db.registrar_venta(usuario_id, producto_id, cantidad)
            except ValueError:
                print("Los IDs y cantidad deben ser números")
                
        elif opcion == "4":
            db.consultar_usuarios()
        elif opcion == "5":
            db.consultar_productos()
        elif opcion == "6":
            db.reporte_ventas()
        elif opcion == "7":
            tabla = input("Tabla a exportar (usuarios/productos/ventas): ")
            filename = input("Nombre del archivo: ") + ".json"
            db.exportar_datos(tabla, filename)
        elif opcion == "8":
            db.cerrar_conexion()
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
