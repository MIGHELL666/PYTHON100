"""
Proyecto 51: Agenda de Contactos
Gestiona una agenda de contactos con funciones CRUD completas.
"""

import json
import os
from datetime import datetime

class AgendaContactos:
    def __init__(self, archivo="contactos.json"):
        self.archivo = archivo
        self.contactos = self.cargar_contactos()
    
    def cargar_contactos(self):
        """Carga los contactos desde el archivo JSON"""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def guardar_contactos(self):
        """Guarda los contactos en el archivo JSON"""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(self.contactos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
    
    def agregar_contacto(self, nombre, telefono, email="", direccion=""):
        """Agrega un nuevo contacto"""
        if nombre in self.contactos:
            print(f"El contacto '{nombre}' ya existe.")
            return False
        
        self.contactos[nombre] = {
            "telefono": telefono,
            "email": email,
            "direccion": direccion,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if self.guardar_contactos():
            print(f"Contacto '{nombre}' agregado exitosamente.")
            return True
        return False
    
    def buscar_contacto(self, nombre):
        """Busca un contacto por nombre"""
        if nombre in self.contactos:
            return self.contactos[nombre]
        return None
    
    def mostrar_contacto(self, nombre):
        """Muestra la información de un contacto"""
        contacto = self.buscar_contacto(nombre)
        if contacto:
            print(f"\n--- Información de {nombre} ---")
            print(f"Teléfono: {contacto['telefono']}")
            print(f"Email: {contacto.get('email', 'No especificado')}")
            print(f"Dirección: {contacto.get('direccion', 'No especificada')}")
            print(f"Fecha de creación: {contacto.get('fecha_creacion', 'No disponible')}")
        else:
            print(f"Contacto '{nombre}' no encontrado.")
    
    def listar_contactos(self):
        """Lista todos los contactos"""
        if not self.contactos:
            print("No hay contactos en la agenda.")
            return
        
        print("\n--- Lista de Contactos ---")
        for nombre, info in sorted(self.contactos.items()):
            print(f"{nombre}: {info['telefono']}")
    
    def eliminar_contacto(self, nombre):
        """Elimina un contacto"""
        if nombre in self.contactos:
            del self.contactos[nombre]
            if self.guardar_contactos():
                print(f"Contacto '{nombre}' eliminado exitosamente.")
                return True
        else:
            print(f"Contacto '{nombre}' no encontrado.")
        return False
    
    def editar_contacto(self, nombre):
        """Edita un contacto existente"""
        if nombre not in self.contactos:
            print(f"Contacto '{nombre}' no encontrado.")
            return False
        
        contacto = self.contactos[nombre]
        print(f"\nEditando contacto: {nombre}")
        print("Presiona Enter para mantener el valor actual")
        
        nuevo_telefono = input(f"Teléfono ({contacto['telefono']}): ").strip()
        if nuevo_telefono:
            contacto['telefono'] = nuevo_telefono
        
        nuevo_email = input(f"Email ({contacto.get('email', '')}): ").strip()
        if nuevo_email:
            contacto['email'] = nuevo_email
        
        nueva_direccion = input(f"Dirección ({contacto.get('direccion', '')}): ").strip()
        if nueva_direccion:
            contacto['direccion'] = nueva_direccion
        
        if self.guardar_contactos():
            print(f"Contacto '{nombre}' actualizado exitosamente.")
            return True
        return False

def main():
    agenda = AgendaContactos()
    
    while True:
        print("\n=== AGENDA DE CONTACTOS ===")
        print("1. Agregar contacto")
        print("2. Buscar contacto")
        print("3. Listar todos los contactos")
        print("4. Editar contacto")
        print("5. Eliminar contacto")
        print("6. Salir")
        
        opcion = input("\nSelecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            nombre = input("Nombre: ").strip()
            if not nombre:
                print("El nombre es obligatorio.")
                continue
            
            telefono = input("Teléfono: ").strip()
            if not telefono:
                print("El teléfono es obligatorio.")
                continue
            
            email = input("Email (opcional): ").strip()
            direccion = input("Dirección (opcional): ").strip()
            
            agenda.agregar_contacto(nombre, telefono, email, direccion)
        
        elif opcion == "2":
            nombre = input("Nombre a buscar: ").strip()
            if nombre:
                agenda.mostrar_contacto(nombre)
        
        elif opcion == "3":
            agenda.listar_contactos()
        
        elif opcion == "4":
            nombre = input("Nombre del contacto a editar: ").strip()
            if nombre:
                agenda.editar_contacto(nombre)
        
        elif opcion == "5":
            nombre = input("Nombre del contacto a eliminar: ").strip()
            if nombre:
                confirmacion = input(f"¿Estás seguro de eliminar '{nombre}'? (s/n): ").strip().lower()
                if confirmacion == 's':
                    agenda.eliminar_contacto(nombre)
        
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
