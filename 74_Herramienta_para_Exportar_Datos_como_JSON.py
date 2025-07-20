"""
Herramienta para Exportar Datos como JSON
Autor: Tu nombre
Descripción: Utilidad completa para convertir diferentes tipos de datos a JSON
"""

import json
import csv
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, date
from pathlib import Path
import requests
from typing import Any, Dict, List, Union

class JSONExporter:
    """Clase principal para exportar diferentes tipos de datos a JSON"""
    
    def __init__(self):
        self.exported_files = []
    
    def export_dict_to_json(self, data: Dict, filename: str = None, indent: int = 2) -> str:
        """Exporta un diccionario a archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dict_export_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
            
            print(f"✅ Diccionario exportado: {filename}")
            self.exported_files.append(filename)
            return filename
        except Exception as e:
            print(f"❌ Error exportando diccionario: {e}")
            return None
    
    def csv_to_json(self, csv_file: str, json_file: str = None) -> str:
        """Convierte un archivo CSV a JSON"""
        if not json_file:
            json_file = Path(csv_file).stem + ".json"
        
        try:
            data = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    data.append(row)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ CSV convertido a JSON: {csv_file} → {json_file}")
            self.exported_files.append(json_file)
            return json_file
        except Exception as e:
            print(f"❌ Error convirtiendo CSV: {e}")
            return None
    
    def sqlite_to_json(self, db_file: str, table_name: str, json_file: str = None) -> str:
        """Exporta una tabla de SQLite a JSON"""
        if not json_file:
            json_file = f"{table_name}_export.json"
        
        try:
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            data = [dict(row) for row in rows]
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            conn.close()
            print(f"✅ Tabla SQLite exportada: {table_name} → {json_file}")
            self.exported_files.append(json_file)
            return json_file
        except Exception as e:
            print(f"❌ Error exportando SQLite: {e}")
            return None
    
    def xml_to_json(self, xml_file: str, json_file: str = None) -> str:
        """Convierte un archivo XML a JSON"""
        if not json_file:
            json_file = Path(xml_file).stem + ".json"
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            def xml_element_to_dict(element):
                """Convierte un elemento XML a diccionario recursivamente"""
                result = {}
                
                # Atributos del elemento
                if element.attrib:
                    result['@attributes'] = element.attrib
                
                # Texto del elemento
                if element.text and element.text.strip():
                    if len(element) == 0:
                        return element.text.strip()
                    else:
                        result['#text'] = element.text.strip()
                
                # Elementos hijos
                children = {}
                for child in element:
                    child_data = xml_element_to_dict(child)
                    if child.tag in children:
                        if not isinstance(children[child.tag], list):
                            children[child.tag] = [children[child.tag]]
                        children[child.tag].append(child_data)
                    else:
                        children[child.tag] = child_data
                
                result.update(children)
                return result if result else None
            
            data = {root.tag: xml_element_to_dict(root)}
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ XML convertido a JSON: {xml_file} → {json_file}")
            self.exported_files.append(json_file)
            return json_file
        except Exception as e:
            print(f"❌ Error convirtiendo XML: {e}")
            return None
    
    def api_to_json(self, url: str, json_file: str = None, headers: Dict = None) -> str:
        """Obtiene datos de una API y los guarda como JSON"""
        if not json_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_file = f"api_data_{timestamp}.json"
        
        try:
            response = requests.get(url, headers=headers or {})
            response.raise_for_status()
            
            data = {
                'metadata': {
                    'url': url,
                    'timestamp': datetime.now().isoformat(),
                    'status_code': response.status_code,
                    'headers': dict(response.headers)
                },
                'data': response.json()
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos de API exportados: {url} → {json_file}")
            self.exported_files.append(json_file)
            return json_file
        except Exception as e:
            print(f"❌ Error obteniendo datos de API: {e}")
            return None
    
    def create_sample_data(self) -> Dict:
        """Crea datos de ejemplo para demostración"""
        return {
            'usuarios': [
                {
                    'id': 1,
                    'nombre': 'Juan Pérez',
                    'email': 'juan@email.com',
                    'edad': 28,
                    'activo': True,
                    'fecha_registro': '2024-01-15',
                    'hobbies': ['programación', 'música', 'deportes']
                },
                {
                    'id': 2,
                    'nombre': 'María García',
                    'email': 'maria@email.com',
                    'edad': 32,
                    'activo': True,
                    'fecha_registro': '2024-02-20',
                    'hobbies': ['lectura', 'viajes', 'cocina']
                },
                {
                    'id': 3,
                    'nombre': 'Carlos López',
                    'email': 'carlos@email.com',
                    'edad': 25,
                    'activo': False,
                    'fecha_registro': '2024-03-10',
                    'hobbies': ['gaming', 'tecnología']
                }
            ],
            'configuracion': {
                'version': '1.0.0',
                'debug': False,
                'database_url': 'postgresql://localhost:5432/myapp',
                'features': {
                    'notifications': True,
                    'analytics': True,
                    'beta_features': False
                }
            },
            'estadisticas': {
                'total_usuarios': 3,
                'usuarios_activos': 2,
                'ultima_actualizacion': datetime.now().isoformat(),
                'metricas': {
                    'sesiones_diarias': 150,
                    'tiempo_promedio': 25.5,
                    'tasa_conversion': 0.15
                }
            }
        }
    
    def validate_json(self, json_file: str) -> bool:
        """Valida si un archivo JSON es válido"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"✅ JSON válido: {json_file}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ JSON inválido: {e}")
            return False
        except Exception as e:
            print(f"❌ Error validando JSON: {e}")
            return False
    
    def pretty_print_json(self, json_file: str):
        """Muestra el contenido JSON de forma legible"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n📄 Contenido de {json_file}:")
            print("=" * 50)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print("=" * 50)
        except Exception as e:
            print(f"❌ Error mostrando JSON: {e}")
    
    def merge_json_files(self, json_files: List[str], output_file: str = None) -> str:
        """Combina múltiples archivos JSON en uno solo"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"merged_json_{timestamp}.json"
        
        try:
            merged_data = {}
            
            for i, json_file in enumerate(json_files):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    merged_data[f'file_{i+1}_{Path(json_file).stem}'] = data
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"✅ {len(json_files)} archivos JSON combinados: {output_file}")
            self.exported_files.append(output_file)
            return output_file
        except Exception as e:
            print(f"❌ Error combinando archivos JSON: {e}")
            return None
    
    def json_to_csv(self, json_file: str, csv_file: str = None) -> str:
        """Convierte JSON a CSV (solo para estructuras planas)"""
        if not csv_file:
            csv_file = Path(json_file).stem + ".csv"
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Intentar aplanar datos si es necesario
            if isinstance(data, dict) and len(data) == 1:
                key = list(data.keys())[0]
                if isinstance(data[key], list):
                    data = data[key]
            
            if isinstance(data, list) and data:
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    if isinstance(data[0], dict):
                        fieldnames = data[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(data)
                    else:
                        writer = csv.writer(f)
                        for item in data:
                            writer.writerow([item])
                
                print(f"✅ JSON convertido a CSV: {json_file} → {csv_file}")
                return csv_file
            else:
                print("❌ Los datos JSON no son compatibles con formato CSV")
                return None
        except Exception as e:
            print(f"❌ Error convirtiendo JSON a CSV: {e}")
            return None
    
    def get_export_summary(self):
        """Muestra un resumen de todos los archivos exportados"""
        if not self.exported_files:
            print("📝 No se han exportado archivos en esta sesión")
            return
        
        print(f"\n📊 Resumen de Exportaciones")
        print("=" * 40)
        print(f"Total de archivos exportados: {len(self.exported_files)}")
        for i, file in enumerate(self.exported_files, 1):
            size = Path(file).stat().st_size if Path(file).exists() else 0
            print(f"{i}. {file} ({size} bytes)")

def show_menu():
    """Muestra el menú principal"""
    print("\n📤 EXPORTADOR DE DATOS JSON")
    print("=" * 35)
    print("1. 📝 Crear y exportar datos de ejemplo")
    print("2. 📊 CSV a JSON")
    print("3. 🗃️  SQLite a JSON")
    print("4. 🏷️  XML a JSON")
    print("5. 🌐 API a JSON")
    print("6. ✅ Validar archivo JSON")
    print("7. 👀 Mostrar contenido JSON")
    print("8. 🔗 Combinar archivos JSON")
    print("9. 📋 JSON a CSV")
    print("10. 📊 Resumen de exportaciones")
    print("0. 👋 Salir")

def main():
    """Función principal"""
    exporter = JSONExporter()
    
    while True:
        show_menu()
        choice = input("\n🎯 Selecciona una opción: ").strip()
        
        try:
            if choice == "1":
                # Crear datos de ejemplo
                sample_data = exporter.create_sample_data()
                filename = input("📁 Nombre del archivo (opcional): ").strip()
                exporter.export_dict_to_json(sample_data, filename or None)
            
            elif choice == "2":
                # CSV a JSON
                csv_file = input("📄 Ruta del archivo CSV: ").strip()
                if Path(csv_file).exists():
                    json_file = input("📁 Nombre del archivo JSON (opcional): ").strip()
                    exporter.csv_to_json(csv_file, json_file or None)
                else:
                    print("❌ El archivo CSV no existe")
            
            elif choice == "3":
                # SQLite a JSON
                db_file = input("🗃️ Ruta de la base de datos SQLite: ").strip()
                if Path(db_file).exists():
                    table_name = input("📋 Nombre de la tabla: ").strip()
                    json_file = input("📁 Nombre del archivo JSON (opcional): ").strip()
                    exporter.sqlite_to_json(db_file, table_name, json_file or None)
                else:
                    print("❌ La base de datos no existe")
            
            elif choice == "4":
                # XML a JSON
                xml_file = input("🏷️ Ruta del archivo XML: ").strip()
                if Path(xml_file).exists():
                    json_file = input("📁 Nombre del archivo JSON (opcional): ").strip()
                    exporter.xml_to_json(xml_file, json_file or None)
                else:
                    print("❌ El archivo XML no existe")
            
            elif choice == "5":
                # API a JSON
                url = input("🌐 URL de la API: ").strip()
                json_file = input("📁 Nombre del archivo JSON (opcional): ").strip()
                headers_input = input("🔑 Headers adicionales (formato: key1=value1,key2=value2): ").strip()
                
                headers = {}
                if headers_input:
                    for header in headers_input.split(','):
                        if '=' in header:
                            key, value = header.split('=', 1)
                            headers[key.strip()] = value.strip()
                
                exporter.api_to_json(url, json_file or None, headers)
            
            elif choice == "6":
                # Validar JSON
                json_file = input("📄 Ruta del archivo JSON: ").strip()
                if Path(json_file).exists():
                    exporter.validate_json(json_file)
                else:
                    print("❌ El archivo no existe")
            
            elif choice == "7":
                # Mostrar JSON
                json_file = input("📄 Ruta del archivo JSON: ").strip()
                if Path(json_file).exists():
                    exporter.pretty_print_json(json_file)
                else:
                    print("❌ El archivo no existe")
            
            elif choice == "8":
                # Combinar JSONs
                files_input = input("📁 Rutas de archivos JSON (separados por coma): ").strip()
                json_files = [f.strip() for f in files_input.split(',')]
                existing_files = [f for f in json_files if Path(f).exists()]
                
                if existing_files:
                    output_file = input("📁 Nombre del archivo combinado (opcional): ").strip()
                    exporter.merge_json_files(existing_files, output_file or None)
                else:
                    print("❌ No se encontraron archivos válidos")
            
            elif choice == "9":
                # JSON a CSV
                json_file = input("📄 Ruta del archivo JSON: ").strip()
                if Path(json_file).exists():
                    csv_file = input("📁 Nombre del archivo CSV (opcional): ").strip()
                    exporter.json_to_csv(json_file, csv_file or None)
                else:
                    print("❌ El archivo no existe")
            
            elif choice == "10":
                # Resumen
                exporter.get_export_summary()
            
            elif choice == "0":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción no válida")
        
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    # Ejemplo de uso directo
    print("🚀 Ejemplo de uso del JSONExporter")
    
    exporter = JSONExporter()
    
    # Crear y exportar datos de ejemplo
    sample_data = exporter.create_sample_data()
    exporter.export_dict_to_json(sample_data, "ejemplo_datos.json")
    
    # Validar el archivo creado
    exporter.validate_json("ejemplo_datos.json")
    
    # Ejecutar interfaz interactiva
    main()

# Dependencias requeridas:
# pip install requests