"""
Aplicación de Lista de Tareas en Consola
Autor: Tu nombre
Descripción: Gestor completo de tareas con persistencia en archivo JSON
"""

import json
import os
from datetime import datetime, date
from enum import Enum

class Priority(Enum):
    """Enum para niveles de prioridad"""
    BAJA = "🟢 Baja"
    MEDIA = "🟡 Media" 
    ALTA = "🔴 Alta"

class Task:
    """Clase para representar una tarea individual"""
    
    def __init__(self, title, description="", priority=Priority.MEDIA, due_date=None):
        self.id = None  # Se asigna automáticamente por el TaskManager
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None
    
    def mark_completed(self):
        """Marca la tarea como completada"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def mark_pending(self):
        """Marca la tarea como pendiente"""
        self.completed = False
        self.completed_at = None
    
    def is_overdue(self):
        """Verifica si la tarea está vencida"""
        if not self.due_date or self.completed:
            return False
        return datetime.strptime(self.due_date, "%Y-%m-%d").date() < date.today()
    
    def to_dict(self):
        """Convierte la tarea a diccionario para JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.name,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea una tarea desde un diccionario"""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority[data.get('priority', 'MEDIA')],
            due_date=data.get('due_date')
        )
        task.id = data.get('id')
        task.completed = data.get('completed', False)
        task.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('completed_at'):
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        return task

class TaskManager:
    """Gestor principal de tareas"""
    
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Carga las tareas desde el archivo JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for task_data in data.get('tasks', []):
                        task = Task.from_dict(task_data)
                        self.tasks.append(task)
                    self.next_id = data.get('next_id', 1)
                print(f"✅ Cargadas {len(self.tasks)} tareas desde {self.filename}")
            except Exception as e:
                print(f"⚠️  Error al cargar tareas: {e}")
    
    def save_tasks(self):
        """Guarda las tareas en el archivo JSON"""
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks],
                'next_id': self.next_id,
                'last_saved': datetime.now().isoformat()
            }
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Tareas guardadas en {self.filename}")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
    
    def add_task(self, title, description="", priority=Priority.MEDIA, due_date=None):
        """Añade una nueva tarea"""
        task = Task(title, description, priority, due_date)
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Tarea agregada: '{title}'")
        return task
    
    def list_tasks(self, filter_type="all"):
        """Lista las tareas con filtros opcionales"""
        filtered_tasks = self.tasks
        
        if filter_type == "pending":
            filtered_tasks = [t for t in self.tasks if not t.completed]
        elif filter_type == "completed":
            filtered_tasks = [t for t in self.tasks if t.completed]
        elif filter_type == "overdue":
            filtered_tasks = [t for t in self.tasks if not t.completed and t.is_overdue()]
        
        if not filtered_tasks:
            print("📝 No hay tareas para mostrar")
            return
        
        print(f"\n📋 Lista de Tareas ({filter_type})")
        print("=" * 60)
        
        for task in filtered_tasks:
            status = "✅" if task.completed else "⏳"
            overdue = "🚨 VENCIDA" if task.is_overdue() else ""
            due_info = f"Vence: {task.due_date}" if task.due_date else ""
            
            print(f"{status} ID: {task.id} | {task.priority.value}")
            print(f"   📌 {task.title}")
            if task.description:
                print(f"   💭 {task.description}")
            if due_info:
                print(f"   📅 {due_info} {overdue}")
            print(f"   🕒 Creada: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
            if task.completed_at:
                print(f"   ✅ Completada: {task.completed_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 60)
    
    def complete_task(self, task_id):
        """Marca una tarea como completada"""
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            self.save_tasks()
            print(f"✅ Tarea completada: '{task.title}'")
        else:
            print(f"❌ No se encontró la tarea con ID {task_id}")
    
    def delete_task(self, task_id):
        """Elimina una tarea"""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"🗑️  Tarea eliminada: '{task.title}'")
        else:
            print(f"❌ No se encontró la tarea con ID {task_id}")
    
    def get_task_by_id(self, task_id):
        """Busca una tarea por su ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def search_tasks(self, query):
        """Busca tareas por título o descripción"""
        query = query.lower()
        results = [
            task for task in self.tasks 
            if query in task.title.lower() or query in task.description.lower()
        ]
        
        if results:
            print(f"\n🔍 Resultados de búsqueda para '{query}':")
            for task in results:
                status = "✅" if task.completed else "⏳"
                print(f"{status} ID: {task.id} - {task.title}")
        else:
            print(f"❌ No se encontraron tareas con '{query}'")
    
    def get_stats(self):
        """Obtiene estadísticas de las tareas"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        pending = total - completed
        overdue = len([t for t in self.tasks if not t.completed and t.is_overdue()])
        
        print(f"\n📊 Estadísticas de Tareas")
        print("=" * 30)
        print(f"Total de tareas:     {total}")
        print(f"Completadas:         {completed}")
        print(f"Pendientes:          {pending}")
        print(f"Vencidas:           {overdue}")
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"Tasa de completado:  {completion_rate:.1f}%")

def show_menu():
    """Muestra el menú principal"""
    print("\n📝 GESTOR DE TAREAS")
    print("=" * 30)
    print("1. ➕ Agregar tarea")
    print("2. 📋 Listar todas las tareas")
    print("3. ⏳ Listar tareas pendientes")
    print("4. ✅ Listar tareas completadas")
    print("5. 🚨 Listar tareas vencidas")
    print("6. ✅ Completar tarea")
    print("7. 🗑️  Eliminar tarea")
    print("8. 🔍 Buscar tareas")
    print("9. 📊 Ver estadísticas")
    print("0. 👋 Salir")

def main():
    """Función principal del programa"""
    task_manager = TaskManager()
    
    while True:
        show_menu()
        choice = input("\n🎯 Selecciona una opción: ").strip()
        
        try:
            if choice == "1":
                # Agregar tarea
                title = input("📌 Título de la tarea: ").strip()
                if not title:
                    print("❌ El título no puede estar vacío")
                    continue
                
                description = input("💭 Descripción (opcional): ").strip()
                
                print("🎯 Prioridad:")
                print("1. Baja")
                print("2. Media")
                print("3. Alta")
                priority_choice = input("Selecciona prioridad (default: 2): ").strip() or "2"
                priorities = {"1": Priority.BAJA, "2": Priority.MEDIA, "3": Priority.ALTA}
                priority = priorities.get(priority_choice, Priority.MEDIA)
                
                due_date = input("📅 Fecha de vencimiento (YYYY-MM-DD, opcional): ").strip()
                if due_date:
                    try:
                        datetime.strptime(due_date, "%Y-%m-%d")
                    except ValueError:
                        print("❌ Formato de fecha inválido")
                        due_date = None
                
                task_manager.add_task(title, description, priority, due_date)
            
            elif choice == "2":
                task_manager.list_tasks("all")
            elif choice == "3":
                task_manager.list_tasks("pending")
            elif choice == "4":
                task_manager.list_tasks("completed")
            elif choice == "5":
                task_manager.list_tasks("overdue")
            
            elif choice == "6":
                task_id = int(input("🎯 ID de la tarea a completar: "))
                task_manager.complete_task(task_id)
            
            elif choice == "7":
                task_id = int(input("🎯 ID de la tarea a eliminar: "))
                confirm = input("⚠️  ¿Estás seguro? (s/N): ").lower()
                if confirm == 's':
                    task_manager.delete_task(task_id)
            
            elif choice == "8":
                query = input("🔍 Término de búsqueda: ").strip()
                if query:
                    task_manager.search_tasks(query)
            
            elif choice == "9":
                task_manager.get_stats()
            
            elif choice == "0":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción no válida")
        
        except ValueError:
            print("❌ Por favor ingresa un número válido")
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()