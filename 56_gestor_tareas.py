"""
Proyecto 56: Gestor de Tareas con Prioridades
Sistema completo de gestión de tareas con categorías, prioridades y fechas límite.
"""

import json
import os
from datetime import datetime, timedelta

class GestorTareas:
    def __init__(self):
        self.archivo_tareas = "tareas.json"
        self.tareas = self.cargar_tareas()
        self.siguiente_id = self.obtener_siguiente_id()
        
        self.prioridades = {
            1: "Baja",
            2: "Media", 
            3: "Alta",
            4: "Urgente"
        }
        
        self.estados = {
            "pendiente": "Pendiente",
            "en_progreso": "En Progreso",
            "completada": "Completada",
            "cancelada": "Cancelada"
        }
    
    def cargar_tareas(self):
        """Carga las tareas desde el archivo JSON"""
        try:
            with open(self.archivo_tareas, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def guardar_tareas(self):
        """Guarda las tareas en el archivo JSON"""
        try:
            with open(self.archivo_tareas, 'w', encoding='utf-8') as f:
                json.dump(self.tareas, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar tareas: {e}")
            return False
    
    def obtener_siguiente_id(self):
        """Obtiene el siguiente ID disponible"""
        if not self.tareas:
            return 1
        return max(tarea['id'] for tarea in self.tareas) + 1
    
    def crear_tarea(self, titulo, descripcion="", categoria="General", prioridad=2, fecha_limite=None):
        """Crea una nueva tarea"""
        tarea = {
            'id': self.siguiente_id,
            'titulo': titulo,
            'descripcion': descripcion,
            'categoria': categoria,
            'prioridad': prioridad,
            'estado': 'pendiente',
            'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'fecha_limite': fecha_limite,
            'fecha_completada': None,
            'tiempo_estimado': None,
            'tiempo_real': None,
            'notas': []
        }
        
        self.tareas.append(tarea)
        self.siguiente_id += 1
        
        if self.guardar_tareas():
            print(f"Tarea '{titulo}' creada con ID {tarea['id']}")
            return tarea['id']
        return None
    
    def buscar_tarea(self, id_tarea):
        """Busca una tarea por ID"""
        for tarea in self.tareas:
            if tarea['id'] == id_tarea:
                return tarea
        return None
    
    def actualizar_estado(self, id_tarea, nuevo_estado):
        """Actualiza el estado de una tarea"""
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            print(f"Tarea con ID {id_tarea} no encontrada.")
            return False
        
        if nuevo_estado not in self.estados:
            print("Estado no válido.")
            return False
        
        tarea['estado'] = nuevo_estado
        
        if nuevo_estado == 'completada':
            tarea['fecha_completada'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.guardar_tareas():
            print(f"Estado de la tarea actualizado a '{self.estados[nuevo_estado]}'")
            return True
        return False
    
    def agregar_nota(self, id_tarea, nota):
        """Agrega una nota a una tarea"""
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            print(f"Tarea con ID {id_tarea} no encontrada.")
            return False
        
        nueva_nota = {
            'texto': nota,
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        tarea['notas'].append(nueva_nota)
        
        if self.guardar_tareas():
            print("Nota agregada exitosamente.")
            return True
        return False
    
    def listar_tareas(self, filtro_estado=None, filtro_categoria=None, filtro_prioridad=None):
        """Lista las tareas con filtros opcionales"""
        tareas_filtradas = self.tareas.copy()
        
        if filtro_estado:
            tareas_filtradas = [t for t in tareas_filtradas if t['estado'] == filtro_estado]
        
        if filtro_categoria:
            tareas_filtradas = [t for t in tareas_filtradas if t['categoria'].lower() == filtro_categoria.lower()]
        
        if filtro_prioridad:
            tareas_filtradas = [t for t in tareas_filtradas if t['prioridad'] == filtro_prioridad]
        
        if not tareas_filtradas:
            print("No se encontraron tareas con los filtros especificados.")
            return
        
        # Ordenar por prioridad (descendente) y fecha de creación
        tareas_filtradas.sort(key=lambda x: (-x['prioridad'], x['fecha_creacion']))
        
        print(f"\n{'='*80}")
        print(f"LISTA DE TAREAS ({len(tareas_filtradas)} encontradas)")
        print(f"{'='*80}")
        
        for tarea in tareas_filtradas:
            self.mostrar_tarea_resumida(tarea)
    
    def mostrar_tarea_resumida(self, tarea):
        """Muestra una tarea en formato resumido"""
        prioridad_texto = self.prioridades.get(tarea['prioridad'], 'Desconocida')
        estado_texto = self.estados.get(tarea['estado'], 'Desconocido')
        
        # Indicador de urgencia
        urgencia = ""
        if tarea['fecha_limite']:
            try:
                fecha_limite = datetime.strptime(tarea['fecha_limite'], "%Y-%m-%d")
                dias_restantes = (fecha_limite - datetime.now()).days
                if dias_restantes < 0:
                    urgencia = " ⚠️ VENCIDA"
                elif dias_restantes <= 1:
                    urgencia = " 🔥 URGENTE"
                elif dias_restantes <= 3:
                    urgencia = " ⏰ PRÓXIMA"
            except:
                pass
        
        print(f"\n[{tarea['id']}] {tarea['titulo']}{urgencia}")
        print(f"    Estado: {estado_texto} | Prioridad: {prioridad_texto} | Categoría: {tarea['categoria']}")
        
        if tarea['fecha_limite']:
            print(f"    Fecha límite: {tarea['fecha_limite']}")
        
        if tarea['descripcion']:
            desc = tarea['descripcion'][:60] + "..." if len(tarea['descripcion']) > 60 else tarea['descripcion']
            print(f"    Descripción: {desc}")
    
    def mostrar_tarea_detallada(self, id_tarea):
        """Muestra una tarea con todos sus detalles"""
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            print(f"Tarea con ID {id_tarea} no encontrada.")
            return
        
        print(f"\n{'='*60}")
        print(f"DETALLES DE LA TAREA #{tarea['id']}")
        print(f"{'='*60}")
        print(f"Título: {tarea['titulo']}")
        print(f"Descripción: {tarea['descripcion'] or 'Sin descripción'}")
        print(f"Categoría: {tarea['categoria']}")
        print(f"Prioridad: {self.prioridades.get(tarea['prioridad'], 'Desconocida')}")
        print(f"Estado: {self.estados.get(tarea['estado'], 'Desconocido')}")
        print(f"Fecha de creación: {tarea['fecha_creacion']}")
        
        if tarea['fecha_limite']:
            print(f"Fecha límite: {tarea['fecha_limite']}")
            try:
                fecha_limite = datetime.strptime(tarea['fecha_limite'], "%Y-%m-%d")
                dias_restantes = (fecha_limite - datetime.now()).days
                if dias_restantes >= 0:
                    print(f"Días restantes: {dias_restantes}")
                else:
                    print(f"Días de retraso: {abs(dias_restantes)}")
            except:
                pass
        
        if tarea['fecha_completada']:
            print(f"Fecha de completada: {tarea['fecha_completada']}")
        
        if tarea['tiempo_estimado']:
            print(f"Tiempo estimado: {tarea['tiempo_estimado']} horas")
        
        if tarea['tiempo_real']:
            print(f"Tiempo real: {tarea['tiempo_real']} horas")
        
        if tarea['notas']:
            print(f"\nNotas ({len(tarea['notas'])}):")
            for i, nota in enumerate(tarea['notas'], 1):
                print(f"  {i}. [{nota['fecha']}] {nota['texto']}")
    
    def eliminar_tarea(self, id_tarea):
        """Elimina una tarea"""
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            print(f"Tarea con ID {id_tarea} no encontrada.")
            return False
        
        self.tareas = [t for t in self.tareas if t['id'] != id_tarea]
        
        if self.guardar_tareas():
            print(f"Tarea '{tarea['titulo']}' eliminada exitosamente.")
            return True
        return False
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas de las tareas"""
        if not self.tareas:
            print("No hay tareas para mostrar estadísticas.")
            return
        
        total = len(self.tareas)
        por_estado = {}
        por_prioridad = {}
        por_categoria = {}
        
        for tarea in self.tareas:
            # Por estado
            estado = tarea['estado']
            por_estado[estado] = por_estado.get(estado, 0) + 1
            
            # Por prioridad
            prioridad = tarea['prioridad']
            por_prioridad[prioridad] = por_prioridad.get(prioridad, 0) + 1
            
            # Por categoría
            categoria = tarea['categoria']
            por_categoria[categoria] = por_categoria.get(categoria, 0) + 1
        
        print(f"\n{'='*50}")
        print(f"ESTADÍSTICAS DE TAREAS")
        print(f"{'='*50}")
        print(f"Total de tareas: {total}")
        
        print(f"\nPor estado:")
        for estado, cantidad in por_estado.items():
            porcentaje = (cantidad / total) * 100
            print(f"  {self.estados.get(estado, estado)}: {cantidad} ({porcentaje:.1f}%)")
        
        print(f"\nPor prioridad:")
        for prioridad in sorted(por_prioridad.keys(), reverse=True):
            cantidad = por_prioridad[prioridad]
            porcentaje = (cantidad / total) * 100
            print(f"  {self.prioridades.get(prioridad, f'Prioridad {prioridad}')}: {cantidad} ({porcentaje:.1f}%)")
        
        print(f"\nPor categoría:")
        for categoria, cantidad in sorted(por_categoria.items()):
            porcentaje = (cantidad / total) * 100
            print(f"  {categoria}: {cantidad} ({porcentaje:.1f}%)")
        
        # Tareas vencidas
        vencidas = 0
        for tarea in self.tareas:
            if tarea['fecha_limite'] and tarea['estado'] != 'completada':
                try:
                    fecha_limite = datetime.strptime(tarea['fecha_limite'], "%Y-%m-%d")
                    if fecha_limite < datetime.now():
                        vencidas += 1
                except:
                    pass
        
        if vencidas > 0:
            print(f"\n⚠️  Tareas vencidas: {vencidas}")

def main():
    gestor = GestorTareas()
    
    while True:
        print("\n=== GESTOR DE TAREAS ===")
        print("1. Crear nueva tarea")
        print("2. Listar todas las tareas")
        print("3. Ver tarea detallada")
        print("4. Actualizar estado de tarea")
        print("5. Agregar nota a tarea")
        print("6. Filtrar tareas")
        print("7. Eliminar tarea")
        print("8. Ver estadísticas")
        print("9. Salir")
        
        opcion = input("\nSelecciona una opción (1-9): ").strip()
        
        if opcion == "1":
            titulo = input("Título de la tarea: ").strip()
            if not titulo:
                print("El título es obligatorio.")
                continue
            
            descripcion = input("Descripción (opcional): ").strip()
            categoria = input("Categoría (opcional, default: General): ").strip() or "General"
            
            print("Prioridades: 1=Baja, 2=Media, 3=Alta, 4=Urgente")
            try:
                prioridad = int(input("Prioridad (1-4, default: 2): ") or "2")
                if prioridad not in [1, 2, 3, 4]:
                    prioridad = 2
            except ValueError:
                prioridad = 2
            
            fecha_limite = input("Fecha límite (YYYY-MM-DD, opcional): ").strip()
            if fecha_limite:
                try:
                    datetime.strptime(fecha_limite, "%Y-%m-%d")
                except ValueError:
                    print("Formato de fecha inválido. Se omitirá la fecha límite.")
                    fecha_limite = None
            else:
                fecha_limite = None
            
            gestor.crear_tarea(titulo, descripcion, categoria, prioridad, fecha_limite)
        
        elif opcion == "2":
            gestor.listar_tareas()
        
        elif opcion == "3":
            try:
                id_tarea = int(input("ID de la tarea: "))
                gestor.mostrar_tarea_detallada(id_tarea)
            except ValueError:
                print("ID inválido.")
        
        elif opcion == "4":
            try:
                id_tarea = int(input("ID de la tarea: "))
                print("Estados disponibles:")
                for key, value in gestor.estados.items():
                    print(f"  {key}: {value}")
                
                nuevo_estado = input("Nuevo estado: ").strip().lower()
                gestor.actualizar_estado(id_tarea, nuevo_estado)
            except ValueError:
                print("ID inválido.")
        
        elif opcion == "5":
            try:
                id_tarea = int(input("ID de la tarea: "))
                nota = input("Nota: ").strip()
                if nota:
                    gestor.agregar_nota(id_tarea, nota)
                else:
                    print("La nota no puede estar vacía.")
            except ValueError:
                print("ID inválido.")
        
        elif opcion == "6":
            print("\nFiltros disponibles:")
            print("1. Por estado")
            print("2. Por categoría")
            print("3. Por prioridad")
            
            filtro = input("Selecciona tipo de filtro (1-3): ").strip()
            
            if filtro == "1":
                print("Estados disponibles:")
                for key, value in gestor.estados.items():
                    print(f"  {key}: {value}")
                estado = input("Estado a filtrar: ").strip().lower()
                gestor.listar_tareas(filtro_estado=estado)
            
            elif filtro == "2":
                categoria = input("Categoría a filtrar: ").strip()
                gestor.listar_tareas(filtro_categoria=categoria)
            
            elif filtro == "3":
                print("Prioridades: 1=Baja, 2=Media, 3=Alta, 4=Urgente")
                try:
                    prioridad = int(input("Prioridad a filtrar (1-4): "))
                    gestor.listar_tareas(filtro_prioridad=prioridad)
                except ValueError:
                    print("Prioridad inválida.")
        
        elif opcion == "7":
            try:
                id_tarea = int(input("ID de la tarea a eliminar: "))
                confirmacion = input(f"¿Estás seguro de eliminar la tarea {id_tarea}? (s/n): ").strip().lower()
                if confirmacion == 's':
                    gestor.eliminar_tarea(id_tarea)
            except ValueError:
                print("ID inválido.")
        
        elif opcion == "8":
            gestor.obtener_estadisticas()
        
        elif opcion == "9":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
