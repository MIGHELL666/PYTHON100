"""
Proyecto 29: Copiar el contenido de un archivo a otro
"""

import shutil
import os
from datetime import datetime

def copiar_archivo_simple(origen, destino):
    """Copia un archivo usando lectura/escritura básica"""
    try:
        with open(origen, 'r', encoding='utf-8') as archivo_origen:
            contenido = archivo_origen.read()
        
        with open(destino, 'w', encoding='utf-8') as archivo_destino:
            archivo_destino.write(contenido)
        
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def copiar_archivo_shutil(origen, destino):
    """Copia un archivo usando shutil (más eficiente)"""
    try:
        shutil.copy2(origen, destino)  # copy2 preserva metadatos
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def copiar_archivo_con_progreso(origen, destino, tamaño_chunk=1024):
    """Copia un archivo mostrando progreso"""
    try:
        tamaño_total = os.path.getsize(origen)
        bytes_copiados = 0
        
        with open(origen, 'rb') as archivo_origen:
            with open(destino, 'wb') as archivo_destino:
                while True:
                    chunk = archivo_origen.read(tamaño_chunk)
                    if not chunk:
                        break
                    
                    archivo_destino.write(chunk)
                    bytes_copiados += len(chunk)
                    
                    # Mostrar progreso
                    progreso = (bytes_copiados / tamaño_total) * 100
                    print(f"\rProgreso: {progreso:.1f}% ({bytes_copiados}/{tamaño_total} bytes)", end='')
        
        print()  # Nueva línea
        return True
        
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def verificar_copia(origen, destino):
    """Verifica que la copia sea idéntica al original"""
    try:
        # Comparar tamaños
        tamaño_origen = os.path.getsize(origen)
        tamaño_destino = os.path.getsize(destino)
        
        if tamaño_origen != tamaño_destino:
            return False, "Tamaños diferentes"
        
        # Comparar contenido
        with open(origen, 'rb') as f1, open(destino, 'rb') as f2:
            while True:
                chunk1 = f1.read(1024)
                chunk2 = f2.read(1024)
                
                if chunk1 != chunk2:
                    return False, "Contenido diferente"
                
                if not chunk1:  # Fin de archivo
                    break
        
        return True, "Archivos idénticos"
        
    except Exception as e:
        return False, f"Error en verificación: {e}"

def crear_archivo_origen():
    """Crea un archivo de origen para pruebas"""
    contenido = f"""Archivo de prueba para copia
Creado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Este archivo contiene varias líneas de texto
para probar la funcionalidad de copia.

Línea con números: 1234567890
Línea con símbolos: !@#$%^&*()_+
Línea con acentos: áéíóú ñÑ

Final del archivo de prueba."""
    
    with open('archivo_origen.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'archivo_origen.txt' creado")

def main():
    print("=== COPIADOR DE ARCHIVOS ===")
    
    while True:
        print("\n1. Copiar archivo (método simple)")
        print("2. Copiar archivo (método shutil)")
        print("3. Copiar archivo (con progreso)")
        print("4. Crear archivo de prueba")
        print("5. Verificar copia")
        print("6. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion in [1, 2, 3]:
                origen = input("Archivo origen: ")
                destino = input("Archivo destino: ")
                
                if not os.path.exists(origen):
                    print(f"Error: El archivo '{origen}' no existe")
                    continue
                
                # Confirmar si el destino existe
                if os.path.exists(destino):
                    confirmar = input(f"El archivo '{destino}' ya existe. ¿Sobrescribir? (s/n): ")
                    if confirmar.lower() != 's':
                        continue
                
                print(f"Copiando '{origen}' a '{destino}'...")
                
                if opcion == 1:
                    exito = copiar_archivo_simple(origen, destino)
                    metodo = "simple"
                elif opcion == 2:
                    exito = copiar_archivo_shutil(origen, destino)
                    metodo = "shutil"
                else:  # opcion == 3
                    exito = copiar_archivo_con_progreso(origen, destino)
                    metodo = "con progreso"
                
                if exito:
                    print(f"✅ Archivo copiado exitosamente usando método {metodo}")
                    
                    # Verificar automáticamente
                    es_identico, mensaje = verificar_copia(origen, destino)
                    print(f"Verificación: {mensaje}")
                else:
                    print("❌ Error al copiar el archivo")
            
            elif opcion == 4:
                crear_archivo_origen()
            
            elif opcion == 5:
                origen = input("Archivo original: ")
                copia = input("Archivo copia: ")
                
                if not os.path.exists(origen) or not os.path.exists(copia):
                    print("Error: Uno o ambos archivos no existen")
                    continue
                
                es_identico, mensaje = verificar_copia(origen, copia)
                print(f"Resultado de verificación: {mensaje}")
                
                if es_identico:
                    print("✅ Los archivos son idénticos")
                else:
                    print("❌ Los archivos son diferentes")
            
            elif opcion == 6:
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
