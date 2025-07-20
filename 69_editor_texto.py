import os
import json
from datetime import datetime
import re

class TextEditor:
    def __init__(self):
        self.content = ""
        self.filename = None
        self.modified = False
        self.cursor_line = 0
        self.cursor_col = 0
        self.clipboard = ""
        self.undo_stack = []
        self.redo_stack = []
        self.search_history = []
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Cargar configuración del editor"""
        default_settings = {
            "tab_size": 4,
            "show_line_numbers": True,
            "word_wrap": True,
            "auto_save": False,
            "theme": "default",
            "font_size": 12,
            "recent_files": []
        }
        
        try:
            if os.path.exists('editor_settings.json'):
                with open('editor_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                # Combinar con configuración por defecto
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
            else:
                self.save_settings(default_settings)
                return default_settings
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return default_settings
    
    def save_settings(self, settings=None):
        """Guardar configuración"""
        try:
            settings_to_save = settings or self.settings
            with open('editor_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def new_file(self):
        """Crear nuevo archivo"""
        if self.modified:
            save = input("¿Guardar cambios antes de crear nuevo archivo? (s/n): ")
            if save.lower().startswith('s'):
                self.save_file()
        
        self.content = ""
        self.filename = None
        self.modified = False
        self.cursor_line = 0
        self.cursor_col = 0
        self.undo_stack = []
        self.redo_stack = []
        print("Nuevo archivo creado")
    
    def open_file(self, filename=None):
        """Abrir archivo"""
        if not filename:
            filename = input("Nombre del archivo a abrir: ")
        
        if not os.path.exists(filename):
            print(f"El archivo '{filename}' no existe")
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            self.filename = filename
            self.modified = False
            self.cursor_line = 0
            self.cursor_col = 0
            
            # Agregar a archivos recientes
            if filename not in self.settings["recent_files"]:
                self.settings["recent_files"].insert(0, filename)
                self.settings["recent_files"] = self.settings["recent_files"][:10]  # Mantener solo 10
                self.save_settings()
            
            print(f"Archivo '{filename}' abierto exitosamente")
            return True
            
        except Exception as e:
            print(f"Error abriendo archivo: {e}")
            return False
    
    def save_file(self, filename=None):
        """Guardar archivo"""
        if not filename and not self.filename:
            filename = input("Nombre del archivo: ")
        
        save_filename = filename or self.filename
        
        try:
            with open(save_filename, 'w', encoding='utf-8') as f:
                f.write(self.content)
            
            self.filename = save_filename
            self.modified = False
            print(f"Archivo guardado como '{save_filename}'")
            return True
            
        except Exception as e:
            print(f"Error guardando archivo: {e}")
            return False
    
    def save_as(self):
        """Guardar como nuevo archivo"""
        filename = input("Nuevo nombre del archivo: ")
        return self.save_file(filename)
    
    def display_content(self, start_line=0, num_lines=20):
        """Mostrar contenido del editor"""
        lines = self.content.split('\n')
        
        print(f"\n=== EDITOR DE TEXTO ===")
        if self.filename:
            status = " (modificado)" if self.modified else ""
            print(f"Archivo: {self.filename}{status}")
        else:
            status = " (modificado)" if self.modified else ""
            print(f"Nuevo archivo{status}")
        
        print(f"Líneas: {len(lines)} | Caracteres: {len(self.content)}")
        print(f"Cursor: Línea {self.cursor_line + 1}, Columna {self.cursor_col + 1}")
        print("-" * 50)
        
        end_line = min(start_line + num_lines, len(lines))
        
        for i in range(start_line, end_line):
            line_num = i + 1
            line_content = lines[i] if i < len(lines) else ""
            
            # Mostrar números de línea si está habilitado
            if self.settings["show_line_numbers"]:
                prefix = f"{line_num:4d} | "
            else:
                prefix = ""
            
            # Marcar línea del cursor
            if i == self.cursor_line:
                cursor_marker = " <-- CURSOR"
            else:
                cursor_marker = ""
            
            print(f"{prefix}{line_content}{cursor_marker}")
        
        if end_line < len(lines):
            print(f"... y {len(lines) - end_line} líneas más")
        
        print("-" * 50)
    
    def insert_text(self, text, position=None):
        """Insertar texto en posición específica"""
        # Guardar estado para deshacer
        self.save_state()
        
        if position is None:
            # Insertar en posición del cursor
            lines = self.content.split('\n')
            if self.cursor_line < len(lines):
                line = lines[self.cursor_line]
                new_line = line[:self.cursor_col] + text + line[self.cursor_col:]
                lines[self.cursor_line] = new_line
                self.content = '\n'.join(lines)
                self.cursor_col += len(text)
            else:
                self.content += text
        else:
            # Insertar en posición específica
            self.content = self.content[:position] + text + self.content[position:]
        
        self.modified = True
    
    def delete_text(self, start_pos, end_pos):
        """Eliminar texto entre posiciones"""
        self.save_state()
        self.content = self.content[:start_pos] + self.content[end_pos:]
        self.modified = True
    
    def goto_line(self, line_number):
        """Ir a línea específica"""
        lines = self.content.split('\n')
        if 1 <= line_number <= len(lines):
            self.cursor_line = line_number - 1
            self.cursor_col = 0
            print(f"Cursor movido a línea {line_number}")
        else:
            print(f"Línea {line_number} no existe (total: {len(lines)} líneas)")
    
    def find_text(self, search_term, case_sensitive=False):
        """Buscar texto"""
        if not search_term:
            search_term = input("Texto a buscar: ")
        
        if not search_term:
            return []
        
        # Agregar a historial de búsqueda
        if search_term not in self.search_history:
            self.search_history.insert(0, search_term)
            self.search_history = self.search_history[:20]  # Mantener solo 20
        
        content_to_search = self.content if case_sensitive else self.content.lower()
        search_term_to_use = search_term if case_sensitive else search_term.lower()
        
        matches = []
        start = 0
        
        while True:
            pos = content_to_search.find(search_term_to_use, start)
            if pos == -1:
                break
            
            # Calcular línea y columna
            lines_before = self.content[:pos].count('\n')
            line_start = self.content.rfind('\n', 0, pos) + 1
            column = pos - line_start
            
            matches.append({
                'position': pos,
                'line': lines_before + 1,
                'column': column + 1,
                'text': self.content[pos:pos + len(search_term)]
            })
            
            start = pos + 1
        
        if matches:
            print(f"Encontradas {len(matches)} coincidencias:")
            for i, match in enumerate(matches[:10]):  # Mostrar solo las primeras 10
                print(f"  {i+1}. Línea {match['line']}, Columna {match['column']}: {match['text']}")
            
            if len(matches) > 10:
                print(f"  ... y {len(matches) - 10} coincidencias más")
        else:
            print(f"No se encontró '{search_term}'")
        
        return matches
    
    def replace_text(self, search_term, replace_term, replace_all=False):
        """Reemplazar texto"""
        if not search_term:
            search_term = input("Texto a buscar: ")
        if not replace_term:
            replace_term = input("Reemplazar con: ")
        
        if not search_term:
            return 0
        
        self.save_state()
        
        if replace_all:
            count = self.content.count(search_term)
            self.content = self.content.replace(search_term, replace_term)
            self.modified = True
            print(f"Reemplazadas {count} coincidencias")
            return count
        else:
            # Reemplazar una por una
            matches = self.find_text(search_term)
            if not matches:
                return 0
            
            count = 0
            for match in matches:
                print(f"\nLínea {match['line']}: {match['text']}")
                choice = input("¿Reemplazar? (s/n/a=todas/q=salir): ").lower()
                
                if choice == 'q':
                    break
                elif choice == 'a':
                    remaining = self.content[match['position']:].replace(search_term, replace_term, -1)
                    self.content = self.content[:match['position']] + remaining
                    count += remaining.count(replace_term) - self.content[match['position']:].count(replace_term)
                    self.modified = True
                    break
                elif choice == 's':
                    start = match['position']
                    end = start + len(search_term)
                    self.content = self.content[:start] + replace_term + self.content[end:]
                    count += 1
                    self.modified = True
            
            print(f"Reemplazadas {count} coincidencias")
            return count
    
    def save_state(self):
        """Guardar estado para deshacer"""
        state = {
            'content': self.content,
            'cursor_line': self.cursor_line,
            'cursor_col': self.cursor_col
        }
        self.undo_stack.append(state)
        
        # Limitar tamaño del stack
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)
        
        # Limpiar redo stack
        self.redo_stack = []
    
    def undo(self):
        """Deshacer última acción"""
        if not self.undo_stack:
            print("No hay acciones para deshacer")
            return
        
        # Guardar estado actual en redo stack
        current_state = {
            'content': self.content,
            'cursor_line': self.cursor_line,
            'cursor_col': self.cursor_col
        }
        self.redo_stack.append(current_state)
        
        # Restaurar estado anterior
        previous_state = self.undo_stack.pop()
        self.content = previous_state['content']
        self.cursor_line = previous_state['cursor_line']
        self.cursor_col = previous_state['cursor_col']
        self.modified = True
        
        print("Acción deshecha")
    
    def redo(self):
        """Rehacer última acción deshecha"""
        if not self.redo_stack:
            print("No hay acciones para rehacer")
            return
        
        # Guardar estado actual en undo stack
        current_state = {
            'content': self.content,
            'cursor_line': self.cursor_line,
            'cursor_col': self.cursor_col
        }
        self.undo_stack.append(current_state)
        
        # Restaurar estado
        next_state = self.redo_stack.pop()
        self.content = next_state['content']
        self.cursor_line = next_state['cursor_line']
        self.cursor_col = next_state['cursor_col']
        self.modified = True
        
        print("Acción rehecha")
    
    def copy_line(self, line_number=None):
        """Copiar línea al portapapeles"""
        if line_number is None:
            line_number = self.cursor_line + 1
        
        lines = self.content.split('\n')
        if 1 <= line_number <= len(lines):
            self.clipboard = lines[line_number - 1]
            print(f"Línea {line_number} copiada al portapapeles")
        else:
            print(f"Línea {line_number} no existe")
    
    def paste_text(self):
        """Pegar texto del portapapeles"""
        if not self.clipboard:
            print("Portapapeles vacío")
            return
        
        self.insert_text(self.clipboard)
        print("Texto pegado")
    
    def get_statistics(self):
        """Obtener estadísticas del texto"""
        lines = self.content.split('\n')
        words = len(self.content.split())
        chars = len(self.content)
        chars_no_spaces = len(self.content.replace(' ', '').replace('\n', '').replace('\t', ''))
        
        # Contar párrafos (líneas no vacías)
        paragraphs = len([line for line in lines if line.strip()])
        
        stats = {
            'lines': len(lines),
            'words': words,
            'characters': chars,
            'characters_no_spaces': chars_no_spaces,
            'paragraphs': paragraphs
        }
        
        print(f"\n=== ESTADÍSTICAS ===")
        print(f"Líneas: {stats['lines']}")
        print(f"Párrafos: {stats['paragraphs']}")
        print(f"Palabras: {stats['words']}")
        print(f"Caracteres: {stats['characters']}")
        print(f"Caracteres (sin espacios): {stats['characters_no_spaces']}")
        
        return stats
    
    def format_text(self):
        """Formatear texto"""
        print("\n=== OPCIONES DE FORMATO ===")
        print("1. Convertir a mayúsculas")
        print("2. Convertir a minúsculas")
        print("3. Capitalizar palabras")
        print("4. Eliminar líneas vacías")
        print("5. Eliminar espacios extra")
        print("6. Numerar líneas")
        
        choice = input("Selecciona opción (1-6): ")
        
        self.save_state()
        
        if choice == "1":
            self.content = self.content.upper()
            print("Texto convertido a mayúsculas")
        elif choice == "2":
            self.content = self.content.lower()
            print("Texto convertido a minúsculas")
        elif choice == "3":
            self.content = self.content.title()
            print("Palabras capitalizadas")
        elif choice == "4":
            lines = [line for line in self.content.split('\n') if line.strip()]
            self.content = '\n'.join(lines)
            print("Líneas vacías eliminadas")
        elif choice == "5":
            # Eliminar espacios múltiples
            self.content = re.sub(r' +', ' ', self.content)
            # Eliminar espacios al inicio y final de líneas
            lines = [line.strip() for line in self.content.split('\n')]
            self.content = '\n'.join(lines)
            print("Espacios extra eliminados")
        elif choice == "6":
            lines = self.content.split('\n')
            numbered_lines = [f"{i+1:4d}. {line}" for i, line in enumerate(lines)]
            self.content = '\n'.join(numbered_lines)
            print("Líneas numeradas")
        else:
            print("Opción no válida")
            return
        
        self.modified = True
    
    def show_recent_files(self):
        """Mostrar archivos recientes"""
        if not self.settings["recent_files"]:
            print("No hay archivos recientes")
            return
        
        print("\n=== ARCHIVOS RECIENTES ===")
        for i, filename in enumerate(self.settings["recent_files"], 1):
            exists = "✓" if os.path.exists(filename) else "✗"
            print(f"{i:2d}. {exists} {filename}")
        
        try:
            choice = int(input("\nSelecciona archivo (0 para cancelar): "))
            if 1 <= choice <= len(self.settings["recent_files"]):
                filename = self.settings["recent_files"][choice - 1]
                self.open_file(filename)
        except ValueError:
            pass
    
    def configure_editor(self):
        """Configurar editor"""
        print("\n=== CONFIGURACIÓN ===")
        print(f"1. Tamaño de tab: {self.settings['tab_size']}")
        print(f"2. Mostrar números de línea: {'Sí' if self.settings['show_line_numbers'] else 'No'}")
        print(f"3. Ajuste de línea: {'Sí' if self.settings['word_wrap'] else 'No'}")
        print(f"4. Guardado automático: {'Sí' if self.settings['auto_save'] else 'No'}")
        print(f"5. Tema: {self.settings['theme']}")
        
        try:
            choice = int(input("\n¿Qué configurar? (1-5, 0 para salir): "))
            
            if choice == 1:
                new_tab_size = int(input(f"Nuevo tamaño de tab (actual: {self.settings['tab_size']}): "))
                self.settings['tab_size'] = max(1, min(8, new_tab_size))
            elif choice == 2:
                self.settings['show_line_numbers'] = not self.settings['show_line_numbers']
            elif choice == 3:
                self.settings['word_wrap'] = not self.settings['word_wrap']
            elif choice == 4:
                self.settings['auto_save'] = not self.settings['auto_save']
            elif choice == 5:
                themes = ['default', 'dark', 'light', 'blue']
                print(f"Temas disponibles: {', '.join(themes)}")
                new_theme = input("Nuevo tema: ")
                if new_theme in themes:
                    self.settings['theme'] = new_theme
            
            if choice > 0:
                self.save_settings()
                print("Configuración guardada")
                
        except ValueError:
            print("Entrada no válida")

def main():
    editor = TextEditor()
    
    print("🖊️  Bienvenido al Editor de Texto")
    print("Escribe 'help' para ver los comandos disponibles")
    
    while True:
        print("\n" + "="*50)
        command = input("Editor> ").strip().lower()
        
        if command == 'help':
            print("\n=== COMANDOS DISPONIBLES ===")
            print("new          - Nuevo archivo")
            print("open         - Abrir archivo")
            print("save         - Guardar archivo")
            print("saveas       - Guardar como...")
            print("recent       - Archivos recientes")
            print("show [n]     - Mostrar contenido (n líneas)")
            print("edit         - Editar texto")
            print("insert       - Insertar texto")
            print("goto <n>     - Ir a línea n")
            print("find         - Buscar texto")
            print("replace      - Reemplazar texto")
            print("copy <n>     - Copiar línea n")
            print("paste        - Pegar texto")
            print("undo         - Deshacer")
            print("redo         - Rehacer")
            print("stats        - Estadísticas")
            print("format       - Formatear texto")
            print("config       - Configuración")
            print("quit         - Salir")
            
        elif command == 'new':
            editor.new_file()
            
        elif command == 'open':
            editor.open_file()
            
        elif command == 'save':
            editor.save_file()
            
        elif command == 'saveas':
            editor.save_as()
            
        elif command == 'recent':
            editor.show_recent_files()
            
        elif command.startswith('show'):
            parts = command.split()
            num_lines = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 20
            editor.display_content(num_lines=num_lines)
            
        elif command == 'edit':
            print("Modo de edición simple:")
            print("Escribe el texto (línea vacía para terminar):")
            
            new_content = []
            while True:
                line = input()
                if line == "":
                    break
                new_content.append(line)
            
            if new_content:
                editor.save_state()
                editor.content = '\n'.join(new_content)
                editor.modified = True
                print("Contenido actualizado")
            
        elif command == 'insert':
            text = input("Texto a insertar: ")
            if text:
                editor.insert_text(text)
                
        elif command.startswith('goto'):
            parts = command.split()
            if len(parts) > 1 and parts[1].isdigit():
                line_num = int(parts[1])
                editor.goto_line(line_num)
            else:
                try:
                    line_num = int(input("Número de línea: "))
                    editor.goto_line(line_num)
                except ValueError:
                    print("Número de línea no válido")
                    
        elif command == 'find':
            search_term = input("Buscar: ")
            case_sensitive = input("¿Sensible a mayúsculas? (s/n): ").lower().startswith('s')
            editor.find_text(search_term, case_sensitive)
            
        elif command == 'replace':
            search_term = input("Buscar: ")
            replace_term = input("Reemplazar con: ")
            replace_all = input("¿Reemplazar todas? (s/n): ").lower().startswith('s')
            editor.replace_text(search_term, replace_term, replace_all)
            
        elif command.startswith('copy'):
            parts = command.split()
            if len(parts) > 1 and parts[1].isdigit():
                line_num = int(parts[1])
                editor.copy_line(line_num)
            else:
                editor.copy_line()
                
        elif command == 'paste':
            editor.paste_text()
            
        elif command == 'undo':
            editor.undo()
            
        elif command == 'redo':
            editor.redo()
            
        elif command == 'stats':
            editor.get_statistics()
            
        elif command == 'format':
            editor.format_text()
            
        elif command == 'config':
            editor.configure_editor()
            
        elif command in ['quit', 'exit', 'q']:
            if editor.modified:
                save = input("¿Guardar cambios antes de salir? (s/n): ")
                if save.lower().startswith('s'):
                    editor.save_file()
            print("¡Hasta luego!")
            break
            
        else:
            print("Comando no reconocido. Escribe 'help' para ver los comandos disponibles.")

if __name__ == "__main__":
    main()
