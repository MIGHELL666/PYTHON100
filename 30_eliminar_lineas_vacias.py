"""
Proyecto 30: Eliminar líneas vacías de un archivo
"""

def eliminar_lineas_vacias(archivo_entrada, archivo_salida=None, crear_backup=True):
    """Elimina líneas vacías de un archivo"""
    try:
        # Leer archivo original
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        # Crear backup si se solicita
        if crear_backup:
            backup_nombre = f"{archivo_entrada}.backup"
            with open(backup_nombre, 'w', encoding='utf-8') as backup:
                backup.writelines(lineas)
            print(f"Backup creado: {backup_nombre}")
        
        # Filtrar líneas vacías
        lineas_filtradas = []
        lineas_eliminadas = 0
        
        for linea in lineas:
            if linea.strip():  # Si la línea no está vacía (después de quitar espacios)
                lineas_filtradas.append(linea)
            else:
                lineas_eliminadas += 1
        
        # Determinar archivo de salida
        if archivo_salida is None:
            archivo_salida = archivo_entrada
        
        # Escribir archivo limpio
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.writelines(lineas_filtradas)
        
        return {
            'lineas_originales': len(lineas),
            'lineas_eliminadas': lineas_eliminadas,
            'lineas_restantes': len(lineas_filtradas),
            'archivo_salida': archivo_salida
        }
        
    except FileNotFoundError:
        return None

def limpiar_espacios_extra(archivo_entrada, archivo_salida=None):
    """Elimina espacios extra al inicio y final de cada línea"""
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        lineas_limpias = []
        for linea in lineas:
            linea_limpia = linea.strip() + '\n' if linea.strip() else '\n'
            lineas_limpias.append(linea_limpia)
        
        if archivo_salida is None:
            archivo_salida = f"limpio_{archivo_entrada}"
        
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.writelines(lineas_limpias)
        
        return archivo_salida
        
    except FileNotFoundError:
        return None

def mostrar_preview_limpieza(archivo_entrada):
    """Muestra un preview de qué líneas se eliminarían"""
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        print(f"=== PREVIEW DE LIMPIEZA: {archivo_entrada} ===")
        lineas_vacias = []
        
        for i, linea in enumerate(lineas, 1):
            if not linea.strip():
                lineas_vacias.append(i)
        
        if lineas_vacias:
            print(f"Líneas vacías encontradas: {len(lineas_vacias)}")
            print(f"Números de línea: {lineas_vacias}")
            
            # Mostrar contexto de algunas líneas vacías
            print("\nContexto (líneas alrededor de las vacías):")
            for num_linea in lineas_vacias[:5]:  # Mostrar solo las primeras 5
                inicio = max(0, num_linea - 2)
                fin = min(len(lineas), num_linea + 2)
                
                print(f"\nAlrededor de línea {num_linea}:")
                for j in range(inicio, fin):
                    marcador = ">>> " if j + 1 == num_linea else "    "
                    contenido = lineas[j].rstrip() if lineas[j].strip() else "[LÍNEA VACÍA]"
                    print(f"{marcador}{j+1:3d}: {contenido}")
        else:
            print("No se encontraron líneas vacías")
        
        return len(lineas_vacias)
        
    except FileNotFoundError:
        return None

def crear_archivo_con_lineas_vacias():
    """Crea un archivo con líneas vacías para pruebas"""
    contenido = """Primera línea con contenido

Segunda línea después de una vacía
   
Línea después de una con solo espacios


Dos líneas vacías arriba
Línea normal
    
Final con espacios"""
    
    with open('archivo_con_vacias.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'archivo_con_vacias.txt' creado con líneas vacías")

def main():
    print("=== ELIMINADOR DE LÍNEAS VACÍAS ===")
    
    while True:
        print("\n1. Eliminar líneas vacías")
        print("2. Preview de limpieza")
        print("3. Limpiar espacios extra")
        print("4. Crear archivo de prueba")
        print("5. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                archivo_entrada = input("Archivo a limpiar: ")
                
                if not os.path.exists(archivo_entrada):
                    print(f"Error: El archivo '{archivo_entrada}' no existe")
                    continue
                
                archivo_salida = input("Archivo de salida (Enter para sobrescribir original): ").strip()
                if not archivo_salida:
                    archivo_salida = None
                
                crear_backup = input("¿Crear backup? (s/n): ").lower() != 'n'
                
                resultado = eliminar_lineas_vacias(archivo_entrada, archivo_salida, crear_backup)
                
                if resultado:
                    print(f"\n✅ Limpieza completada:")
                    print(f"Líneas originales: {resultado['lineas_originales']}")
                    print(f"Líneas eliminadas: {resultado['lineas_eliminadas']}")
                    print(f"Líneas restantes: {resultado['lineas_restantes']}")
                    print(f"Archivo resultado: {resultado['archivo_salida']}")
                else:
                    print("❌ Error al procesar el archivo")
            
            elif opcion == 2:
                archivo = input("Archivo a analizar: ")
                num_vacias = mostrar_preview_limpieza(archivo)
                
                if num_vacias is None:
                    print(f"Error: No se encontró el archivo '{archivo}'")
                elif num_vacias == 0:
                    print("✅ El archivo no tiene líneas vacías")
                else:
                    print(f"Se encontraron {num_vacias} líneas vacías")
            
            elif opcion == 3:
                archivo_entrada = input("Archivo a limpiar espacios: ")
                
                if not os.path.exists(archivo_entrada):
                    print(f"Error: El archivo '{archivo_entrada}' no existe")
                    continue
                
                archivo_salida = input("Archivo de salida (Enter para auto-generar): ").strip()
                if not archivo_salida:
                    archivo_salida = None
                
                resultado = limpiar_espacios_extra(archivo_entrada, archivo_salida)
                
                if resultado:
                    print(f"✅ Espacios extra eliminados. Archivo guardado como: {resultado}")
                else:
                    print("❌ Error al procesar el archivo")
            
            elif opcion == 4:
                crear_archivo_con_lineas_vacias()
            
            elif opcion == 5:
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
    import os
    main()
