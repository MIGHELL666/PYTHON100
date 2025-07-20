"""
Proyecto 28: Verificar si un archivo existe
"""

import os
from pathlib import Path

def verificar_archivo_existe(ruta_archivo):
    """Verifica si un archivo existe usando diferentes métodos"""
    resultados = {}
    
    # Método 1: os.path.exists()
    resultados['os_path_exists'] = os.path.exists(ruta_archivo)
    
    # Método 2: os.path.isfile()
    resultados['os_path_isfile'] = os.path.isfile(ruta_archivo)
    
    # Método 3: pathlib.Path
    path_obj = Path(ruta_archivo)
    resultados['pathlib_exists'] = path_obj.exists()
    resultados['pathlib_is_file'] = path_obj.is_file()
    
    # Método 4: try/except con open()
    try:
        with open(ruta_archivo, 'r'):
            resultados['open_method'] = True
    except FileNotFoundError:
        resultados['open_method'] = False
    except PermissionError:
        resultados['open_method'] = "Sin permisos"
    
    return resultados

def obtener_info_archivo(ruta_archivo):
    """Obtiene información detallada del archivo"""
    if not os.path.exists(ruta_archivo):
        return None
    
    stats = os.stat(ruta_archivo)
    path_obj = Path(ruta_archivo)
    
    info = {
        'nombre': path_obj.name,
        'ruta_completa': path_obj.absolute(),
        'directorio': path_obj.parent,
        'extension': path_obj.suffix,
        'tamaño_bytes': stats.st_size,
        'tamaño_kb': round(stats.st_size / 1024, 2),
        'es_archivo': path_obj.is_file(),
        'es_directorio': path_obj.is_dir(),
        'permisos_lectura': os.access(ruta_archivo, os.R_OK),
        'permisos_escritura': os.access(ruta_archivo, os.W_OK),
        'permisos_ejecucion': os.access(ruta_archivo, os.X_OK)
    }
    
    return info

def listar_archivos_directorio(directorio="."):
    """Lista archivos en un directorio"""
    try:
        archivos = []
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isfile(ruta_completa):
                archivos.append(item)
        return archivos
    except PermissionError:
        return None

def crear_archivo_prueba():
    """Crea un archivo de prueba"""
    with open('archivo_prueba.txt', 'w', encoding='utf-8') as archivo:
        archivo.write("Este es un archivo de prueba para verificar existencia.")
    print("Archivo 'archivo_prueba.txt' creado")

def main():
    print("=== VERIFICADOR DE EXISTENCIA DE ARCHIVOS ===")
    
    while True:
        print("\n1. Verificar archivo específico")
        print("2. Crear archivo de prueba")
        print("3. Listar archivos del directorio actual")
        print("4. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                ruta_archivo = input("Ingresa la ruta del archivo: ")
                
                # Verificar existencia
                resultados = verificar_archivo_existe(ruta_archivo)
                
                print(f"\n=== VERIFICACIÓN DE: {ruta_archivo} ===")
                print(f"os.path.exists(): {resultados['os_path_exists']}")
                print(f"os.path.isfile(): {resultados['os_path_isfile']}")
                print(f"pathlib.exists(): {resultados['pathlib_exists']}")
                print(f"pathlib.is_file(): {resultados['pathlib_is_file']}")
                print(f"método open(): {resultados['open_method']}")
                
                # Si existe, mostrar información detallada
                if resultados['os_path_exists']:
                    info = obtener_info_archivo(ruta_archivo)
                    if info:
                        print(f"\n=== INFORMACIÓN DEL ARCHIVO ===")
                        print(f"Nombre: {info['nombre']}")
                        print(f"Ruta completa: {info['ruta_completa']}")
                        print(f"Directorio: {info['directorio']}")
                        print(f"Extensión: {info['extension']}")
                        print(f"Tamaño: {info['tamaño_bytes']} bytes ({info['tamaño_kb']} KB)")
                        print(f"Es archivo: {info['es_archivo']}")
                        print(f"Es directorio: {info['es_directorio']}")
                        print(f"Permisos - Lectura: {info['permisos_lectura']}, Escritura: {info['permisos_escritura']}, Ejecución: {info['permisos_ejecucion']}")
                else:
                    print("❌ El archivo NO existe")
            
            elif opcion == 2:
                crear_archivo_prueba()
            
            elif opcion == 3:
                archivos = listar_archivos_directorio()
                if archivos is not None:
                    print(f"\n=== ARCHIVOS EN EL DIRECTORIO ACTUAL ===")
                    if archivos:
                        for i, archivo in enumerate(archivos, 1):
                            print(f"{i:2d}. {archivo}")
                    else:
                        print("No hay archivos en el directorio actual")
                else:
                    print("Error: Sin permisos para listar el directorio")
            
            elif opcion == 4:
                print("¡Hasta luego!")
                break
            
            else:
                print("Opción no válida")
                
        except ValueError:
            print("Error: Ingresa un número válido")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
